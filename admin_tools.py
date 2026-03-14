"""
admin_tools.py — أدوات الإدارة
الاستخدام:
  python admin_tools.py stats
  python admin_tools.py list-sections
  python admin_tools.py list-students
  python admin_tools.py add-questions questions.json
  python admin_tools.py add-students students.txt
"""
import sys, json
from database import Database

db = Database("quiz_bot.db")

def stats(_=None):
    s = db.stats()
    print(f"📊 إحصائيات:\n  طلاب: {s['registered']}/{s['total_students']}\n  سكشنات: {s['sections']}\n  أسئلة: {s['questions']}\n  اختبارات منجزة: {s['sessions']}")

def list_sections(_=None):
    for s in db.get_sections():
        print(f"[{s['id']}] {s['emoji']} {s['name']}  ({db.count_q(s['id'])} سؤال)")

def list_students(_=None):
    with db._connect() as c:
        for s in c.execute("SELECT * FROM students ORDER BY id").fetchall():
            status = f"✅ {s['telegram_id']}" if s["telegram_id"] else "⏳ لم يسجل"
            print(f"[{s['id']}] {s['full_name']}  — {status}")

def add_questions(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    db.import_questions(data)
    print(f"✅ تم إضافة {len(data)} سؤال")

def add_students(path):
    with open(path, encoding="utf-8") as f:
        names = [l.strip() for l in f if l.strip()]
    db.import_students(names)
    print(f"✅ تم إضافة {len(names)} طالب")

CMDS = {
    "stats": stats, "list-sections": list_sections,
    "list-students": list_students, "add-questions": add_questions,
    "add-students": add_students,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__); sys.exit(1)
    CMDS[sys.argv[1]](sys.argv[2] if len(sys.argv) > 2 else None)
