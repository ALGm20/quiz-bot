"""
dashboard.py — لوحة النتائج للأستاذ
"""
from flask import Flask, render_template_string, request, redirect, session
import os
from database import Database

app = Flask(__name__)
app.secret_key = os.environ.get("DASH_SECRET","quiz_secret_2024")
db  = Database("/data/quiz_bot.db")
PASS = os.environ.get("DASH_PASSWORD","admin123")

PAGE = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>نتائج الطلاب</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh}
.hdr{background:linear-gradient(135deg,#1e40af,#7c3aed);padding:20px 28px;display:flex;justify-content:space-between;align-items:center}
.hdr h1{font-size:1.5rem;font-weight:700}
.hdr p{color:#bfdbfe;font-size:.9rem;margin-top:3px}
.logout{background:#dc2626;color:white;padding:6px 14px;border-radius:8px;text-decoration:none;font-size:.85rem}
.cards{display:flex;gap:12px;padding:20px 28px;flex-wrap:wrap}
.card{background:#1e293b;border-radius:12px;padding:16px 22px;flex:1;min-width:130px}
.card .n{font-size:1.8rem;font-weight:700;color:#60a5fa}
.card .l{color:#94a3b8;font-size:.85rem;margin-top:2px}
.wrap{padding:0 28px 28px;overflow-x:auto}
.search{margin-bottom:12px}
.search input{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:8px 14px;color:#e2e8f0;width:280px;font-size:.9rem}
table{width:100%;border-collapse:collapse;background:#1e293b;border-radius:12px;overflow:hidden}
th{background:#334155;padding:12px 14px;text-align:right;color:#94a3b8;font-size:.82rem;font-weight:600}
td{padding:12px 14px;border-top:1px solid #334155;vertical-align:middle}
tr:hover td{background:#263548}
.bar-w{width:100px;background:#334155;border-radius:5px;height:7px;display:inline-block;vertical-align:middle}
.bar-f{height:7px;border-radius:5px}
.bg{background:#22c55e}.by{background:#f59e0b}.br{background:#ef4444}
.pt{display:inline-block;width:38px;font-size:.82rem;color:#94a3b8;text-align:left}
.badge{display:inline-block;padding:2px 9px;border-radius:20px;font-size:.75rem;font-weight:600}
.bg2{background:#14532d;color:#86efac}.by2{background:#713f12;color:#fde68a}.br2{background:#7f1d1d;color:#fca5a5}
.login{display:flex;align-items:center;justify-content:center;min-height:100vh}
.lbox{background:#1e293b;padding:36px;border-radius:16px;width:340px}
.lbox h2{margin-bottom:20px;color:#60a5fa}
.lbox input{width:100%;padding:9px 12px;background:#334155;border:1px solid #475569;border-radius:8px;color:#e2e8f0;font-size:.95rem;margin-bottom:14px}
.lbox button{width:100%;padding:11px;background:#2563eb;color:white;border:none;border-radius:8px;font-size:.95rem;cursor:pointer;font-weight:600}
.lbox button:hover{background:#1d4ed8}
.err{color:#f87171;margin-bottom:10px;font-size:.88rem}
.empty{text-align:center;padding:50px;color:#64748b}
</style>
</head>
<body>
{% if not auth %}
<div class="login">
  <div class="lbox">
    <h2>🔐 دخول الأستاذ</h2>
    {% if err %}<div class="err">{{ err }}</div>{% endif %}
    <form method="POST" action="/login">
      <input type="password" name="p" placeholder="كلمة المرور" autofocus>
      <button>دخول</button>
    </form>
  </div>
</div>
{% else %}
<div class="hdr">
  <div><h1>📊 نتائج الطلاب</h1><p>{{ st.assessed }} أجروا التقييم من {{ st.students }}</p></div>
  <a href="/logout" class="logout">خروج</a>
</div>
<div class="cards">
  <div class="card"><div class="n">{{ st.students }}</div><div class="l">إجمالي الطلاب</div></div>
  <div class="card"><div class="n">{{ st.assessed }}</div><div class="l">أجروا التقييم</div></div>
  <div class="card"><div class="n">{{ st.questions }}</div><div class="l">الأسئلة</div></div>
  <div class="card"><div class="n">{{ st.sections }}</div><div class="l">السكشنات</div></div>
</div>
<div class="wrap">
<div class="search"><input id="si" placeholder="🔍 ابحث باسم الطالب..." onkeyup="f()"></div>
{% if students %}
<table id="t">
  <thead><tr><th>#</th><th>الاسم</th><th>النتيجة</th><th>المجموع</th><th>التقدير</th><th>التاريخ</th></tr></thead>
  <tbody>
  {% for s in students %}
  {% set p=s.pct %}
  <tr>
    <td style="color:#64748b">{{ loop.index }}</td>
    <td style="font-weight:600">{{ s.full_name }}</td>
    <td>
      <div class="bar-w"><div class="bar-f {{ 'bg' if p>=60 else 'by' if p>=40 else 'br' }}" style="width:{{p}}%"></div></div>
      <span class="pt"> {{p}}%</span>
    </td>
    <td style="color:#94a3b8">{{ s.score }}/{{ s.total_q }}</td>
    <td>
      {% if p>=75 %}<span class="badge bg2">ممتاز</span>
      {% elif p>=60 %}<span class="badge by2">جيد</span>
      {% else %}<span class="badge br2">يحتاج مراجعة</span>{% endif %}
    </td>
    <td style="color:#64748b;font-size:.82rem">{{ s.assessed_at[:10] if s.assessed_at else '—' }}</td>
  </tr>
  {% endfor %}
  </tbody>
</table>
{% else %}
<div class="empty"><p style="font-size:2.5rem">📭</p><p style="margin-top:10px">لا توجد نتائج بعد</p></div>
{% endif %}
</div>
<script>function f(){const v=document.getElementById('si').value.toLowerCase();document.querySelectorAll('#t tbody tr').forEach(r=>{r.style.display=r.cells[1].textContent.toLowerCase().includes(v)?'':'none'})}</script>
{% endif %}
</body></html>"""

@app.route("/login", methods=["POST"])
def login():
    if request.form.get("p") == PASS:
        session["a"] = True
        return redirect("/")
    return render_template_string(PAGE, auth=False, err="كلمة المرور خاطئة", students=[], st={})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    if not session.get("a"):
        return render_template_string(PAGE, auth=False, err=None, students=[], st={})
    students = db.get_all_students()
    st = db.stats()
    return render_template_string(PAGE, auth=True, students=students, st=st, err=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
