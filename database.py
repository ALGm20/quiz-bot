"""
database.py — قاعدة بيانات بوت الاختبارات (نموذج السكشنات)
"""
import sqlite3
import random
from typing import Optional


class Database:
    def __init__(self, path: str):
        self.path = path
        self._init()

    def _connect(self):
        c = sqlite3.connect(self.path)
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

                CREATE TABLE IF NOT EXISTS students (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name   TEXT NOT NULL UNIQUE,
                    telegram_id INTEGER UNIQUE,
                    registered_at TEXT
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
                    explanation    TEXT,
                    difficulty     INTEGER DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS sessions (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id     INTEGER NOT NULL REFERENCES students(id),
                    section_id     INTEGER REFERENCES sections(id),
                    total_questions INTEGER NOT NULL,
                    score          INTEGER DEFAULT 0,
                    completed      INTEGER DEFAULT 0,
                    is_daily       INTEGER DEFAULT 0,
                    daily_date     TEXT,
                    started_at     TEXT DEFAULT (datetime('now')),
                    completed_at   TEXT
                );

                CREATE TABLE IF NOT EXISTS answers (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id  INTEGER NOT NULL REFERENCES sessions(id),
                    question_id INTEGER NOT NULL REFERENCES questions(id),
                    user_answer TEXT,
                    is_correct  INTEGER DEFAULT 0
                );
            """)

    # ── STUDENTS ─────────────────────────────────────────────────

    def get_student(self, telegram_id: int):
        with self._connect() as c:
            return c.execute("SELECT * FROM students WHERE telegram_id=?", (telegram_id,)).fetchone()

    def register_student(self, full_name: str, telegram_id: int) -> str:
        """Returns: 'ok' | 'not_found' | 'taken'"""
        from datetime import datetime
        with self._connect() as c:
            row = c.execute("SELECT * FROM students WHERE TRIM(full_name)=TRIM(?)", (full_name,)).fetchone()
            if not row:
                return "not_found"
            if row["telegram_id"] and row["telegram_id"] != telegram_id:
                return "taken"
            c.execute("UPDATE students SET telegram_id=?, registered_at=? WHERE id=?",
                      (telegram_id, datetime.now().isoformat(), row["id"]))
        return "ok"

    def add_student(self, full_name: str):
        with self._connect() as c:
            c.execute("INSERT OR IGNORE INTO students (full_name) VALUES (?)", (full_name.strip(),))

    def import_students(self, names: list):
        with self._connect() as c:
            c.executemany("INSERT OR IGNORE INTO students (full_name) VALUES (?)",
                          [(n.strip(),) for n in names if n.strip()])

    # ── SECTIONS ─────────────────────────────────────────────────

    def get_sections(self):
        with self._connect() as c:
            return c.execute("SELECT * FROM sections ORDER BY sort_order, id").fetchall()

    def get_section(self, sec_id: int):
        with self._connect() as c:
            return c.execute("SELECT * FROM sections WHERE id=?", (sec_id,)).fetchone()

    def add_section(self, name: str, description: str = "", emoji: str = "📖", order: int = 0):
        with self._connect() as c:
            c.execute("INSERT OR IGNORE INTO sections (name, description, emoji, sort_order) VALUES (?,?,?,?)",
                      (name, description, emoji, order))

    def count_q(self, sec_id: int) -> int:
        with self._connect() as c:
            return c.execute("SELECT COUNT(*) FROM questions WHERE section_id=?", (sec_id,)).fetchone()[0]

    # ── QUESTIONS ────────────────────────────────────────────────

    def get_questions(self, sec_id: int, limit: Optional[int] = None):
        with self._connect() as c:
            rows = c.execute(
                "SELECT * FROM questions WHERE section_id=? ORDER BY RANDOM()", (sec_id,)
            ).fetchall()
        rows = list(rows)
        return rows[:limit] if limit else rows

    def daily_questions(self, today: str, count: int = 10):
        with self._connect() as c:
            ids = [r[0] for r in c.execute("SELECT id FROM questions").fetchall()]
        if not ids:
            return []
        rng = random.Random(today)
        chosen = rng.sample(ids, min(count, len(ids)))
        with self._connect() as c:
            ph = ",".join("?" * len(chosen))
            return c.execute(f"SELECT * FROM questions WHERE id IN ({ph})", chosen).fetchall()

    def import_questions(self, data: list):
        """
        كل عنصر في data يجب أن يحتوي:
        {
          "section": "اسم السكشن",
          "section_description": "...",   ← اختياري
          "section_emoji": "🦠",          ← اختياري
          "question": "نص السؤال",
          "a": "...", "b": "...", "c": "...", "d": "...",
          "answer": "A",
          "explanation": "..."            ← اختياري
        }
        """
        with self._connect() as c:
            cache = {}
            for item in data:
                sname = item["section"].strip()
                if sname not in cache:
                    row = c.execute("SELECT id FROM sections WHERE name=?", (sname,)).fetchone()
                    if row:
                        cache[sname] = row["id"]
                    else:
                        cur = c.execute(
                            "INSERT INTO sections (name, description, emoji) VALUES (?,?,?)",
                            (sname,
                             item.get("section_description", ""),
                             item.get("section_emoji", "📖"))
                        )
                        cache[sname] = cur.lastrowid

                c.execute(
                    """INSERT INTO questions
                       (section_id, question_text, option_a, option_b, option_c, option_d,
                        correct_answer, explanation)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (cache[sname], item["question"],
                     item["a"], item["b"], item["c"], item["d"],
                     item["answer"].upper(), item.get("explanation", ""))
                )

    # ── SESSIONS ─────────────────────────────────────────────────

    def new_session(self, student_id, sec_id, total, is_daily=False, daily_date=None) -> int:
        with self._connect() as c:
            cur = c.execute(
                "INSERT INTO sessions (student_id, section_id, total_questions, is_daily, daily_date) VALUES (?,?,?,?,?)",
                (student_id, sec_id, total, int(is_daily), daily_date)
            )
            return cur.lastrowid

    def save_answer(self, session_id, question_id, answer, correct):
        with self._connect() as c:
            c.execute("INSERT INTO answers (session_id, question_id, user_answer, is_correct) VALUES (?,?,?,?)",
                      (session_id, question_id, answer, int(correct)))

    def complete_session(self, session_id, score):
        from datetime import datetime
        with self._connect() as c:
            c.execute("UPDATE sessions SET score=?, completed=1, completed_at=? WHERE id=?",
                      (score, datetime.now().isoformat(), session_id))

    def check_daily(self, student_id, today: str):
        """Returns (done: bool, score: int, total: int)"""
        with self._connect() as c:
            row = c.execute(
                "SELECT score, total_questions FROM sessions WHERE student_id=? AND is_daily=1 AND daily_date=? AND completed=1",
                (student_id, today)
            ).fetchone()
        if row:
            return True, row["score"], row["total_questions"]
        return False, 0, 0

    def student_sessions(self, student_id, limit=10):
        with self._connect() as c:
            return c.execute(
                """SELECT s.*, sec.name as section_name
                   FROM sessions s LEFT JOIN sections sec ON s.section_id = sec.id
                   WHERE s.student_id=? AND s.completed=1
                   ORDER BY s.started_at DESC LIMIT ?""",
                (student_id, limit)
            ).fetchall()

    # ── LEADERBOARD ──────────────────────────────────────────────

    def leaderboard(self, limit=10):
        with self._connect() as c:
            return c.execute(
                """SELECT st.full_name,
                          COUNT(s.id) as total,
                          ROUND(AVG(CAST(s.score AS FLOAT)/s.total_questions)*100) as avg_pct
                   FROM sessions s JOIN students st ON s.student_id=st.id
                   WHERE s.completed=1 AND s.total_questions>0
                   GROUP BY st.id ORDER BY avg_pct DESC LIMIT ?""",
                (limit,)
            ).fetchall()

    # ── STATS ────────────────────────────────────────────────────

    def stats(self):
        with self._connect() as c:
            return {
                "total_students": c.execute("SELECT COUNT(*) FROM students").fetchone()[0],
                "registered":     c.execute("SELECT COUNT(*) FROM students WHERE telegram_id IS NOT NULL").fetchone()[0],
                "sections":       c.execute("SELECT COUNT(*) FROM sections").fetchone()[0],
                "questions":      c.execute("SELECT COUNT(*) FROM questions").fetchone()[0],
                "sessions":       c.execute("SELECT COUNT(*) FROM sessions WHERE completed=1").fetchone()[0],
            }
