"""
database.py — قاعدة بيانات بدون قائمة طلاب مسبقة
"""
import sqlite3, json, random
from typing import Optional

class Database:
    def __init__(self, path: str):
        self.path = path
        self._init()

    def _connect(self):
        c = sqlite3.connect(self.path, check_same_thread=False)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys = ON")
        return c

    def _init(self):
        with self._connect() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS sections (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT NOT NULL UNIQUE,
                    description TEXT,
                    emoji       TEXT DEFAULT '📖',
                    sort_order  INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS questions (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_id     INTEGER NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
                    question_text  TEXT NOT NULL,
                    option_a       TEXT NOT NULL,
                    option_b       TEXT NOT NULL,
                    option_c       TEXT NOT NULL,
                    option_d       TEXT NOT NULL,
                    correct_answer TEXT NOT NULL CHECK(correct_answer IN ('A','B','C','D')),
                    explanation    TEXT
                );

                CREATE TABLE IF NOT EXISTS students (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name     TEXT NOT NULL,
                    telegram_id   INTEGER NOT NULL UNIQUE,
                    registered_at TEXT DEFAULT (datetime('now')),
                    assessed      INTEGER DEFAULT 0,
                    score         INTEGER DEFAULT 0,
                    total_q       INTEGER DEFAULT 0,
                    pct           INTEGER DEFAULT 0,
                    assessed_at   TEXT
                );

                CREATE TABLE IF NOT EXISTS active_sessions (
                    user_id        INTEGER PRIMARY KEY,
                    mode           TEXT DEFAULT 'training',
                    sec_id         INTEGER,
                    questions_json TEXT NOT NULL,
                    current_idx    INTEGER DEFAULT 0,
                    score          INTEGER DEFAULT 0,
                    total          INTEGER NOT NULL,
                    updated_at     TEXT DEFAULT (datetime('now'))
                );
            """)

    # ── STUDENTS ──────────────────────────────────────────────────

    def register_new_student(self, full_name: str, telegram_id: int):
        """تسجيل طالب جديد — يُضاف مباشرة بلا قائمة مسبقة"""
        with self._connect() as c:
            c.execute(
                "INSERT OR IGNORE INTO students (full_name, telegram_id) VALUES (?,?)",
                (full_name.strip(), telegram_id)
            )

    def get_student_by_telegram(self, telegram_id: int):
        with self._connect() as c:
            return c.execute(
                "SELECT * FROM students WHERE telegram_id=?", (telegram_id,)
            ).fetchone()

    def save_assessment_result(self, student_id: int, score: int, total: int):
        pct = round((score / total) * 100) if total else 0
        with self._connect() as c:
            c.execute("""
                UPDATE students
                SET assessed=1, score=?, total_q=?, pct=?, assessed_at=datetime('now')
                WHERE id=?
            """, (score, total, pct, student_id))

    def get_all_students(self):
        with self._connect() as c:
            return c.execute(
                "SELECT * FROM students ORDER BY pct DESC"
            ).fetchall()

    # ── SECTIONS ──────────────────────────────────────────────────

    def get_sections(self):
        with self._connect() as c:
            return c.execute(
                "SELECT * FROM sections ORDER BY sort_order, id"
            ).fetchall()

    def get_section(self, sec_id: int):
        with self._connect() as c:
            return c.execute(
                "SELECT * FROM sections WHERE id=?", (sec_id,)
            ).fetchone()

    def count_q(self, sec_id: int) -> int:
        with self._connect() as c:
            return c.execute(
                "SELECT COUNT(*) FROM questions WHERE section_id=?", (sec_id,)
            ).fetchone()[0]

    # ── QUESTIONS ─────────────────────────────────────────────────

    def get_all_questions_shuffled(self):
        with self._connect() as c:
            return list(c.execute(
                "SELECT * FROM questions ORDER BY RANDOM()"
            ).fetchall())

    def get_questions(self, sec_id: int, limit: Optional[int] = None):
        with self._connect() as c:
            rows = list(c.execute(
                "SELECT * FROM questions WHERE section_id=? ORDER BY RANDOM()", (sec_id,)
            ).fetchall())
        return rows[:limit] if limit else rows

    def import_questions(self, data: list):
        with self._connect() as c:
            cache = {}
            for item in data:
                sname = item["section"].strip()
                if sname not in cache:
                    row = c.execute(
                        "SELECT id FROM sections WHERE name=?", (sname,)
                    ).fetchone()
                    if row:
                        cache[sname] = row["id"]
                    else:
                        cur = c.execute(
                            "INSERT INTO sections (name, description, emoji) VALUES (?,?,?)",
                            (sname, item.get("section_description",""),
                             item.get("section_emoji","📖"))
                        )
                        cache[sname] = cur.lastrowid
                c.execute(
                    """INSERT INTO questions
                       (section_id,question_text,option_a,option_b,option_c,option_d,
                        correct_answer,explanation)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (cache[sname], item["question"],
                     item["a"], item["b"], item["c"], item["d"],
                     item["answer"].upper(), item.get("explanation",""))
                )

    # ── ACTIVE SESSION ─────────────────────────────────────────────

    def save_session(self, user_id: int, mode: str, sec_id,
                     questions: list, idx: int, score: int, total: int):
        qs = [dict(q) for q in questions]
        with self._connect() as c:
            c.execute("""
                INSERT OR REPLACE INTO active_sessions
                (user_id,mode,sec_id,questions_json,current_idx,score,total,updated_at)
                VALUES (?,?,?,?,?,?,?,datetime('now'))
            """, (user_id, mode, sec_id,
                  json.dumps(qs, ensure_ascii=False), idx, score, total))

    def get_session(self, user_id: int):
        with self._connect() as c:
            row = c.execute(
                "SELECT * FROM active_sessions WHERE user_id=?", (user_id,)
            ).fetchone()
        if not row:
            return None
        return {
            "mode":   row["mode"],
            "sec_id": row["sec_id"],
            "qs":     json.loads(row["questions_json"]),
            "idx":    row["current_idx"],
            "score":  row["score"],
            "total":  row["total"],
        }

    def update_session(self, user_id: int, idx: int, score: int):
        with self._connect() as c:
            c.execute("""
                UPDATE active_sessions
                SET current_idx=?, score=?, updated_at=datetime('now')
                WHERE user_id=?
            """, (idx, score, user_id))

    def delete_session(self, user_id: int):
        with self._connect() as c:
            c.execute(
                "DELETE FROM active_sessions WHERE user_id=?", (user_id,)
            )

    # ── STATS ─────────────────────────────────────────────────────

    def stats(self):
        with self._connect() as c:
            return {
                "sections":  c.execute("SELECT COUNT(*) FROM sections").fetchone()[0],
                "questions": c.execute("SELECT COUNT(*) FROM questions").fetchone()[0],
                "students":  c.execute("SELECT COUNT(*) FROM students").fetchone()[0],
                "assessed":  c.execute(
                    "SELECT COUNT(*) FROM students WHERE assessed=1"
                ).fetchone()[0],
            }
