"""
admin_tools.py — أداة الإدارة لإضافة طلاب وأسئلة من ملفات خارجية
الاستخدام:
  python admin_tools.py add-students students.txt
  python admin_tools.py add-questions questions.json
  python admin_tools.py list-chapters
  python admin_tools.py list-students
  python admin_tools.py stats
"""
import sys
import json
from database import Database

db = Database("quiz_bot.db")


def add_students_from_file(path: str):
    with open(path, encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip()]
    db.import_students_from_list(names)
    print(f"✅ تم إضافة/تحديث {len(names)} طالب")


def add_questions_from_json(path: str):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    db.import_questions_from_json(data)
    print(f"✅ تم إضافة {len(data)} سؤال")


def list_chapters():
    chapters = db.get_all_chapters()
    if not chapters:
        print("لا توجد فصول.")
        return
    for ch in chapters:
        count = db.count_questions_in_chapter(ch["id"])
        print(f"[{ch['id']}] {ch['name']}  ({count} سؤال)")


def list_students():
    with db._connect() as conn:
        students = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
    for s in students:
        status = f"✅ Telegram:{s['telegram_id']}" if s["telegram_id"] else "⏳ لم يسجّل بعد"
        print(f"[{s['id']}] {s['full_name']}  — {status}")


def show_stats():
    stats = db.get_stats()
    print("📊 إحصائيات قاعدة البيانات:")
    for k, v in stats.items():
        print(f"   {k}: {v}")


COMMANDS = {
    "add-students":  add_students_from_file,
    "add-questions": add_questions_from_json,
    "list-chapters": lambda _=None: list_chapters(),
    "list-students": lambda _=None: list_students(),
    "stats":         lambda _=None: show_stats(),
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    COMMANDS[cmd](arg)
