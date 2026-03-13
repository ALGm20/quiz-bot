# 🤖 بوت الاختبارات التعليمية — Telegram Quiz Bot

بوت تلغرام متكامل للاختبارات متعدد الخيارات (MCQ) مع نظام تسجيل وقاعدة بيانات.

---

## 📁 هيكل الملفات

```
quiz_bot/
├── bot.py            ← البوت الرئيسي
├── database.py       ← طبقة قاعدة البيانات (SQLite)
├── populate_db.py    ← تعبئة البيانات الأولية (شغّلها مرة واحدة)
├── admin_tools.py    ← أدوات الإدارة
├── requirements.txt  ← المكتبات المطلوبة
└── quiz_bot.db       ← قاعدة البيانات (تُنشأ تلقائياً)
```

---

## 🚀 خطوات التشغيل

### 1. إنشاء البوت على تلغرام
- افتح [@BotFather](https://t.me/BotFather)
- أرسل `/newbot` واتبع التعليمات
- احفظ التوكن (TOKEN)

### 2. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 3. ضع التوكن في bot.py
افتح `bot.py` وغيّر هذا السطر:
```python
TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
```
أو يمكنك استخدام متغير البيئة:
```bash
export BOT_TOKEN="1234567890:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 4. تعبئة البيانات الأولية
```bash
python populate_db.py
```
هذا سيضيف الطلاب والأسئلة التجريبية.

### 5. تشغيل البوت
```bash
python bot.py
```

---

## 👥 إضافة الطلاب

**طريقة 1:** عدّل قائمة `STUDENTS` في `populate_db.py`

**طريقة 2:** أنشئ ملف `students.txt` (اسم ثلاثي في كل سطر):
```
أحمد محمد علي
سارة خالد إبراهيم
محمد عبدالله حسن
```
ثم شغّل:
```bash
python admin_tools.py add-students students.txt
```

---

## ❓ إضافة أسئلة

أنشئ ملف `questions.json` بهذا الشكل:
```json
[
  {
    "chapter": "الفصل الأول: اسم الفصل",
    "chapter_description": "وصف الفصل (اختياري)",
    "question": "نص السؤال هنا",
    "a": "الخيار الأول",
    "b": "الخيار الثاني",
    "c": "الخيار الثالث",
    "d": "الخيار الرابع",
    "answer": "A",
    "explanation": "شرح الإجابة الصحيحة (اختياري)"
  }
]
```
ثم شغّل:
```bash
python admin_tools.py add-questions questions.json
```

---

## 🛠️ أوامر الإدارة

```bash
python admin_tools.py stats              # إحصائيات عامة
python admin_tools.py list-chapters     # عرض الفصول
python admin_tools.py list-students     # عرض الطلاب وحالة تسجيلهم
python admin_tools.py add-students students.txt
python admin_tools.py add-questions questions.json
```

---

## 🎮 كيف يعمل البوت

| الخطوة | التفاصيل |
|--------|---------|
| `/start` | يطلب من المستخدم كتابة اسمه الثلاثي |
| التحقق | البوت يتحقق من الاسم في قاعدة البيانات |
| التسجيل | إذا وُجد الاسم، يُربط حساب تلغرام به |
| الاختبارات | اختيار فصل أو الاختبار اليومي |
| النتائج | تُحفظ كل إجابة وتُعرض النتيجة النهائية |
| لوحة الشرف | مقارنة النتائج بين جميع الطلاب |

---

## ⚙️ قاعدة البيانات (SQLite)

```
students      ← قائمة الطلاب المسموح لهم
chapters      ← الفصول الدراسية
questions     ← أسئلة MCQ مرتبطة بفصول
quiz_sessions ← جلسات الاختبارات
quiz_answers  ← إجابات كل سؤال
```

---

## 📌 ملاحظات

- **الاختبار اليومي:** 10 أسئلة عشوائية من جميع الفصول — كل الطلاب يحصلون على نفس الأسئلة في نفس اليوم (seed يومي)
- **لا يمكن لطالبين مشاركة نفس الاسم** — كل اسم ثلاثي فريد
- **البوت لا يقبل مستخدمين جدد** — الطلاب يجب أن يكونوا مضافين مسبقاً من قِبل المشرف
