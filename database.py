"""
database.py — قاعدة بيانات مبسّطة (بدون تسجيل طلاب)
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
            """)

    # ── SECTIONS ─────────────────────────────────────────────────

    def get_sections(self):
        with self._connect() as c:
            return c.execute("SELECT * FROM sections ORDER BY sort_order, id").fetchall()

    def get_section(self, sec_id: int):
        with self._connect() as c:
            return c.execute("SELECT * FROM sections WHERE id=?", (sec_id,)).fetchone()

    def count_q(self, sec_id: int) -> int:
        with self._connect() as c:
            return c.execute("SELECT COUNT(*) FROM questions WHERE section_id=?", (sec_id,)).fetchone()[0]

    # ── QUESTIONS ────────────────────────────────────────────────

    def get_questions(self, sec_id: int, limit: Optional[int] = None):
        with self._connect() as c:
            rows = list(c.execute(
                "SELECT * FROM questions WHERE section_id=? ORDER BY RANDOM()", (sec_id,)
            ).fetchall())
        return rows[:limit] if limit else rows

    def import_questions(self, data: list):
        """
        كل عنصر:
        {
          "section": "اسم السكشن",
          "section_description": "...",
          "section_emoji": "🦠",
          "question": "نص السؤال",
          "a": "...", "b": "...", "c": "...", "d": "...",
          "answer": "A",
          "explanation": "..."
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

    # ── STATS ────────────────────────────────────────────────────

    def stats(self):
        with self._connect() as c:
            return {
                "sections":  c.execute("SELECT COUNT(*) FROM sections").fetchone()[0],
                "questions": c.execute("SELECT COUNT(*) FROM questions").fetchone()[0],
            }
