"""
database.py — SQLite database layer for the Quiz Telegram Bot
"""
import sqlite3
import random
from datetime import date
from typing import Optional


class Database:
    def __init__(self, path: str):
        self.path = path
        self._init_schema()

    # ──────────────────────────────────────────────────────
    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # ──────────────────────────────────────────────────────
    def _init_schema(self):
        with self._connect() as conn:
            conn.executescript("""
                -- Chapters / Units
                CREATE TABLE IF NOT EXISTS chapters (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT NOT NULL,
                    description TEXT
                );

                -- Pre-registered students list
                CREATE TABLE IF NOT EXISTS students (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name   TEXT NOT NULL UNIQUE,
                    telegram_id INTEGER UNIQUE,
                    registered_at TEXT
                );

                -- MCQ Questions
                CREATE TABLE IF NOT EXISTS questions (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    chapter_id      INTEGER NOT NULL REFERENCES chapters(id),
                    question_text   TEXT NOT NULL,
                    option_a        TEXT NOT NULL,
                    option_b        TEXT NOT NULL,
                    option_c        TEXT NOT NULL,
                    option_d        TEXT NOT NULL,
                    correct_answer  TEXT NOT NULL CHECK(correct_answer IN ('A','B','C','D')),
                    explanation     TEXT,
                    difficulty      INTEGER DEFAULT 1  -- 1=easy 2=medium 3=hard
                );

                -- Quiz sessions (per student per run)
                CREATE TABLE IF NOT EXISTS quiz_sessions (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id      INTEGER NOT NULL REFERENCES students(id),
                    chapter_id      INTEGER REFERENCES chapters(id),
                    total_questions INTEGER NOT NULL,
                    score           INTEGER DEFAULT 0,
                    completed       INTEGER DEFAULT 0,
                    is_daily        INTEGER DEFAULT 0,
                    daily_date      TEXT,
                    started_at      TEXT DEFAULT (datetime('now')),
                    completed_at    TEXT
                );

                -- Individual answers per session
                CREATE TABLE IF NOT EXISTS quiz_answers (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id  INTEGER NOT NULL REFERENCES quiz_sessions(id),
                    question_id INTEGER NOT NULL REFERENCES questions(id),
                    user_answer TEXT,
                    is_correct  INTEGER DEFAULT 0
                );
            """)

    # ══════════════════════════════════════════════════════
    #  STUDENTS
    # ══════════════════════════════════════════════════════

    def find_student_by_name(self, full_name: str):
        """Case-insensitive name match (Arabic)."""
        with self._connect() as conn:
            return conn.execute(
                "SELECT * FROM students WHERE TRIM(full_name) = TRIM(?)", (full_name,)
            ).fetchone()

    def get_student_by_telegram(self, telegram_id: int):
        with self._connect() as conn:
            return conn.execute(
                "SELECT * FROM students WHERE telegram_id = ?", (telegram_id,)
            ).fetchone()

    def link_telegram_to_student(self, student_id: int, telegram_id: int):
        from datetime import datetime
        with self._connect() as conn:
            conn.execute(
                "UPDATE students SET telegram_id = ?, registered_at = ? WHERE id = ?",
                (telegram_id, datetime.now().isoformat(), student_id),
            )

    def add_student(self, full_name: str):
        """Admin helper to add a student to the allowed list."""
        with self._connect() as conn:
            conn.execute("INSERT OR IGNORE INTO students (full_name) VALUES (?)", (full_name,))

    # ══════════════════════════════════════════════════════
    #  CHAPTERS
    # ══════════════════════════════════════════════════════

    def get_all_chapters(self):
        with self._connect() as conn:
            return conn.execute("SELECT * FROM chapters ORDER BY id").fetchall()

    def get_chapter(self, chapter_id: int):
        with self._connect() as conn:
            return conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()

    def count_questions_in_chapter(self, chapter_id: int) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as c FROM questions WHERE chapter_id = ?", (chapter_id,)
            ).fetchone()
            return row["c"]

    # ══════════════════════════════════════════════════════
    #  QUESTIONS
    # ══════════════════════════════════════════════════════

    def get_questions(self, chapter_id: int, limit: Optional[int] = None):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM questions WHERE chapter_id = ? ORDER BY RANDOM()",
                (chapter_id,),
            ).fetchall()
        rows = list(rows)
        if limit:
            rows = rows[:limit]
        return rows

    def get_daily_questions(self, today: str, count: int = 10):
        """Pick 'count' random questions across all chapters, seeded by date so
        all students get the same set on the same day."""
        with self._connect() as conn:
            all_ids = [r["id"] for r in conn.execute("SELECT id FROM questions").fetchall()]
        if not all_ids:
            return []
        rng = random.Random(today)   # same seed per day
        chosen_ids = rng.sample(all_ids, min(count, len(all_ids)))
        with self._connect() as conn:
            placeholders = ",".join("?" * len(chosen_ids))
            return conn.execute(
                f"SELECT * FROM questions WHERE id IN ({placeholders})", chosen_ids
            ).fetchall()

    # ══════════════════════════════════════════════════════
    #  SESSIONS
    # ══════════════════════════════════════════════════════

    def create_quiz_session(self, student_id: int, chapter_id, total: int,
                            is_daily=False, daily_date=None) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO quiz_sessions
                   (student_id, chapter_id, total_questions, is_daily, daily_date)
                   VALUES (?, ?, ?, ?, ?)""",
                (student_id, chapter_id, total, int(is_daily), daily_date),
            )
            return cur.lastrowid

    def save_answer(self, session_id: int, question_id: int, answer: str, correct: bool):
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO quiz_answers (session_id, question_id, user_answer, is_correct)
                   VALUES (?, ?, ?, ?)""",
                (session_id, question_id, answer, int(correct)),
            )

    def complete_quiz_session(self, session_id: int, score: int):
        from datetime import datetime
        with self._connect() as conn:
            conn.execute(
                """UPDATE quiz_sessions SET score=?, completed=1, completed_at=?
                   WHERE id=?""",
                (score, datetime.now().isoformat(), session_id),
            )

    def check_daily_done(self, student_id: int, today: str) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                """SELECT id FROM quiz_sessions
                   WHERE student_id=? AND is_daily=1 AND daily_date=? AND completed=1""",
                (student_id, today),
            ).fetchone()
            return row is not None

    def get_daily_score(self, student_id: int, today: str):
        with self._connect() as conn:
            row = conn.execute(
                """SELECT score, total_questions FROM quiz_sessions
                   WHERE student_id=? AND is_daily=1 AND daily_date=? AND completed=1""",
                (student_id, today),
            ).fetchone()
            if row:
                return row["score"], row["total_questions"]
            return 0, 0

    def get_student_sessions(self, student_id: int, limit: int = 10):
        with self._connect() as conn:
            return conn.execute(
                """SELECT qs.*, c.name as chapter_name
                   FROM quiz_sessions qs
                   LEFT JOIN chapters c ON qs.chapter_id = c.id
                   WHERE qs.student_id = ? AND qs.completed = 1
                   ORDER BY qs.started_at DESC
                   LIMIT ?""",
                (student_id, limit),
            ).fetchall()

    # ══════════════════════════════════════════════════════
    #  LEADERBOARD
    # ══════════════════════════════════════════════════════

    def get_leaderboard(self, limit: int = 10):
        with self._connect() as conn:
            return conn.execute(
                """SELECT s.full_name,
                          COUNT(qs.id) as total_quizzes,
                          ROUND(AVG(CAST(qs.score AS FLOAT)/qs.total_questions)*100) as avg_pct
                   FROM quiz_sessions qs
                   JOIN students s ON qs.student_id = s.id
                   WHERE qs.completed = 1 AND qs.total_questions > 0
                   GROUP BY s.id
                   ORDER BY avg_pct DESC
                   LIMIT ?""",
                (limit,),
            ).fetchall()

    # ══════════════════════════════════════════════════════
    #  ADMIN STATS
    # ══════════════════════════════════════════════════════

    def get_stats(self) -> dict:
        with self._connect() as conn:
            total_students = conn.execute("SELECT COUNT(*) as c FROM students").fetchone()["c"]
            registered     = conn.execute("SELECT COUNT(*) as c FROM students WHERE telegram_id IS NOT NULL").fetchone()["c"]
            total_q        = conn.execute("SELECT COUNT(*) as c FROM questions").fetchone()["c"]
            total_sessions = conn.execute("SELECT COUNT(*) as c FROM quiz_sessions WHERE completed=1").fetchone()["c"]
            total_chapters = conn.execute("SELECT COUNT(*) as c FROM chapters").fetchone()["c"]
        return {
            "total_students": total_students,
            "registered": registered,
            "total_questions": total_q,
            "total_sessions": total_sessions,
            "total_chapters": total_chapters,
        }

    # ══════════════════════════════════════════════════════
    #  BULK IMPORT HELPERS
    # ══════════════════════════════════════════════════════

    def import_students_from_list(self, names: list[str]):
        """Add a list of student full-names."""
        with self._connect() as conn:
            conn.executemany(
                "INSERT OR IGNORE INTO students (full_name) VALUES (?)",
                [(n.strip(),) for n in names if n.strip()],
            )

    def import_questions_from_json(self, data: list[dict]):
        """
        data = list of dicts:
        {
          "chapter": "اسم الفصل",
          "chapter_description": "...",   # optional
          "question": "نص السؤال",
          "a": "...", "b": "...", "c": "...", "d": "...",
          "answer": "A",          # A/B/C/D
          "explanation": "..."    # optional
        }
        """
        with self._connect() as conn:
            chapter_cache = {}
            for item in data:
                ch_name = item["chapter"].strip()
                if ch_name not in chapter_cache:
                    row = conn.execute("SELECT id FROM chapters WHERE name=?", (ch_name,)).fetchone()
                    if row:
                        chapter_cache[ch_name] = row["id"]
                    else:
                        cur = conn.execute(
                            "INSERT INTO chapters (name, description) VALUES (?,?)",
                            (ch_name, item.get("chapter_description", "")),
                        )
                        chapter_cache[ch_name] = cur.lastrowid

                conn.execute(
                    """INSERT INTO questions
                       (chapter_id, question_text, option_a, option_b, option_c, option_d,
                        correct_answer, explanation)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (
                        chapter_cache[ch_name],
                        item["question"],
                        item["a"], item["b"], item["c"], item["d"],
                        item["answer"].upper(),
                        item.get("explanation", ""),
                    ),
                )
