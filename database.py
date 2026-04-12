import json
import sqlite3
from typing import Optional


class Database:
    def __init__(self, path: str):
        self.path = path
        self._init()

    def _connect(self):
        conn = sqlite3.connect(self.path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init(self):
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS sections (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT NOT NULL UNIQUE,
                    description TEXT,
                    emoji       TEXT DEFAULT '🌿',
                    sort_order  INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS questions (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_id     INTEGER NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
                    display_order  INTEGER NOT NULL DEFAULT 0,
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
                    registered_at TEXT DEFAULT (datetime('now'))
                );

                CREATE TABLE IF NOT EXISTS section_progress (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id  INTEGER NOT NULL REFERENCES students(id),
                    section_id  INTEGER NOT NULL REFERENCES sections(id),
                    assessed    INTEGER DEFAULT 0,
                    score       INTEGER DEFAULT 0,
                    total_q     INTEGER DEFAULT 0,
                    pct         INTEGER DEFAULT 0,
                    assessed_at TEXT,
                    UNIQUE(student_id, section_id)
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
                """
            )

            columns = {
                row["name"]
                for row in conn.execute("PRAGMA table_info(questions)").fetchall()
            }
            if "display_order" not in columns:
                conn.execute(
                    "ALTER TABLE questions ADD COLUMN display_order INTEGER NOT NULL DEFAULT 0"
                )
                conn.execute(
                    """
                    UPDATE questions
                    SET display_order = id
                    WHERE display_order = 0
                    """
                )

    def register_new_student(self, full_name: str, telegram_id: int):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO students (full_name, telegram_id) VALUES (?, ?)",
                (full_name.strip(), telegram_id),
            )

    def get_student_by_telegram(self, telegram_id: int):
        with self._connect() as conn:
            return conn.execute(
                "SELECT * FROM students WHERE telegram_id=?",
                (telegram_id,),
            ).fetchone()

    def get_section_progress(self, student_id: int, section_id: int):
        with self._connect() as conn:
            return conn.execute(
                """
                SELECT * FROM section_progress
                WHERE student_id=? AND section_id=?
                """,
                (student_id, section_id),
            ).fetchone()

    def save_section_assessment(self, student_id: int, section_id: int, score: int, total: int):
        pct = round((score / total) * 100) if total else 0
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO section_progress
                    (student_id, section_id, assessed, score, total_q, pct, assessed_at)
                VALUES (?, ?, 1, ?, ?, ?, datetime('now'))
                ON CONFLICT(student_id, section_id) DO UPDATE SET
                    assessed=1,
                    score=?,
                    total_q=?,
                    pct=?,
                    assessed_at=datetime('now')
                """,
                (student_id, section_id, score, total, pct, score, total, pct),
            )

    def can_reassess(self, student_id: int, section_id: int, days: int = 4):
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT CAST(julianday('now') - julianday(assessed_at) AS INTEGER) AS dp
                FROM section_progress
                WHERE student_id=? AND section_id=? AND assessed=1
                """,
                (student_id, section_id),
            ).fetchone()

        if not row:
            return True, 0

        days_passed = row["dp"] or 0
        if days_passed >= days:
            return True, 0
        return False, days - days_passed

    def get_sections(self):
        with self._connect() as conn:
            return conn.execute(
                "SELECT * FROM sections ORDER BY sort_order ASC, id ASC"
            ).fetchall()

    def get_section(self, sec_id: int):
        with self._connect() as conn:
            return conn.execute(
                "SELECT * FROM sections WHERE id=?",
                (sec_id,),
            ).fetchone()

    def count_q(self, sec_id: int) -> int:
        with self._connect() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM questions WHERE section_id=?",
                (sec_id,),
            ).fetchone()[0]

    def get_questions(self, sec_id: int, limit: Optional[int] = None):
        return self.get_questions_ordered(sec_id, limit)

    def get_questions_ordered(self, sec_id: int, limit: Optional[int] = None):
        with self._connect() as conn:
            rows = list(
                conn.execute(
                    """
                    SELECT * FROM questions
                    WHERE section_id=?
                    ORDER BY display_order ASC, id ASC
                    """,
                    (sec_id,),
                ).fetchall()
            )
        return rows[:limit] if limit else rows

    def import_questions(self, data: list):
        with self._connect() as conn:
            section_cache = {}
            order_cache = {}

            for item in data:
                section_name = item["section"].strip()
                if section_name not in section_cache:
                    row = conn.execute(
                        "SELECT id FROM sections WHERE name=?",
                        (section_name,),
                    ).fetchone()
                    if row:
                        section_cache[section_name] = row["id"]
                    else:
                        section_cache[section_name] = conn.execute(
                            """
                            INSERT INTO sections (name, description, emoji, sort_order)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                section_name,
                                item.get("section_description", ""),
                                item.get("section_emoji", "🌿"),
                                item.get("section_order", 0),
                            ),
                        ).lastrowid

                order_cache[section_name] = order_cache.get(section_name, 0) + 1
                display_order = item.get("order", order_cache[section_name])

                conn.execute(
                    """
                    INSERT INTO questions (
                        section_id,
                        display_order,
                        question_text,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer,
                        explanation
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        section_cache[section_name],
                        display_order,
                        item["question"],
                        item["a"],
                        item["b"],
                        item["c"],
                        item["d"],
                        item["answer"].upper(),
                        item.get("explanation", ""),
                    ),
                )

    def save_session(self, user_id, mode, sec_id, questions, idx, score, total):
        payload = [dict(question) for question in questions]
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO active_sessions
                    (user_id, mode, sec_id, questions_json, current_idx, score, total, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """,
                (
                    user_id,
                    mode,
                    sec_id,
                    json.dumps(payload, ensure_ascii=False),
                    idx,
                    score,
                    total,
                ),
            )

    def get_session(self, user_id):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM active_sessions WHERE user_id=?",
                (user_id,),
            ).fetchone()

        if not row:
            return None

        return {
            "mode": row["mode"],
            "sec_id": row["sec_id"],
            "qs": json.loads(row["questions_json"]),
            "idx": row["current_idx"],
            "score": row["score"],
            "total": row["total"],
        }

    def update_session(self, user_id, idx, score):
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE active_sessions
                SET current_idx=?, score=?, updated_at=datetime('now')
                WHERE user_id=?
                """,
                (idx, score, user_id),
            )

    def delete_session(self, user_id):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM active_sessions WHERE user_id=?",
                (user_id,),
            )

    def stats(self):
        with self._connect() as conn:
            return {
                "sections": conn.execute("SELECT COUNT(*) FROM sections").fetchone()[0],
                "questions": conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0],
                "students": conn.execute("SELECT COUNT(*) FROM students").fetchone()[0],
            }
