"""
Populate the plant classification quiz database from the curated JSON bank.
Run this file after generating the bank with:
    py -3 tools/build_curated_bank.py
"""

import json
import os
from collections import Counter
from pathlib import Path

from database import Database

os.makedirs("/data", exist_ok=True)
db = Database("/data/quiz_bot.db")

BASE_DIR = Path(__file__).resolve().parent
BANK_PATH = BASE_DIR / "data" / "plant_question_bank.json"

with db._connect() as conn:
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("DELETE FROM active_sessions")
    conn.execute("DELETE FROM section_progress")
    conn.execute("DELETE FROM questions")
    conn.execute("DELETE FROM sections")
    conn.execute("PRAGMA foreign_keys = ON")

print("تم حذف بنك الأسئلة القديم وإعادة تجهيز قاعدة البيانات.")

questions = json.loads(BANK_PATH.read_text(encoding="utf-8"))
db.import_questions(questions)

counts = Counter(item["section"] for item in questions)
print(f"تمت إضافة {len(questions)} سؤالاً جديداً:\n")
for section_name, count in counts.items():
    emoji = next(
        (item.get("section_emoji", "🌿") for item in questions if item["section"] == section_name),
        "🌿",
    )
    print(f"{emoji} {section_name}: {count} سؤال")

print("\nشغّل البوت عبر: python run.py")
