import os

from flask import Flask, redirect, render_template_string, request, session

from database import Database

app = Flask(__name__)
app.secret_key = os.environ.get("DASH_SECRET", "plant_quiz_secret")

os.makedirs("/data", exist_ok=True)
db = Database("/data/quiz_bot.db")
PASSWORD = os.environ.get("DASH_PASSWORD", "admin123")

PAGE = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>لوحة نتائج بوت تصنيف النباتات</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Segoe UI',Tahoma,sans-serif;background:#f2f7f2;color:#163020;min-height:100vh}
    .hdr{background:linear-gradient(135deg,#2f6f3e,#8bbf5a);padding:22px 28px;display:flex;justify-content:space-between;align-items:center;color:#fff}
    .hdr h1{font-size:1.6rem;font-weight:700}
    .hdr p{font-size:.95rem;opacity:.92;margin-top:4px}
    .logout{background:#8f2d2d;color:#fff;padding:8px 14px;border-radius:10px;text-decoration:none}
    .cards{display:flex;gap:14px;padding:22px 28px;flex-wrap:wrap}
    .card{background:#fff;border:1px solid #d8e7d2;border-radius:16px;padding:18px 22px;min-width:150px;box-shadow:0 8px 24px rgba(47,111,62,.08)}
    .card .n{font-size:1.8rem;font-weight:700;color:#2f6f3e}
    .card .l{font-size:.88rem;color:#56705f;margin-top:4px}
    .wrap{padding:0 28px 28px;overflow-x:auto}
    .search{margin-bottom:14px}
    .search input{width:300px;max-width:100%;padding:10px 14px;border-radius:10px;border:1px solid #bfd3bc;background:#fff;color:#163020}
    table{width:100%;border-collapse:collapse;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(47,111,62,.08)}
    th{background:#e4f0df;padding:14px;text-align:right;color:#355842;font-size:.84rem}
    td{padding:14px;border-top:1px solid #edf4ea;vertical-align:middle}
    tr:hover td{background:#f8fbf7}
    .bar-w{width:110px;background:#e6eee4;border-radius:999px;height:8px;display:inline-block;vertical-align:middle;overflow:hidden}
    .bar-f{height:8px;border-radius:999px}
    .good{background:#4caf50}
    .mid{background:#d5a021}
    .low{background:#d9534f}
    .pt{display:inline-block;width:42px;font-size:.82rem;color:#56705f;text-align:left}
    .badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.75rem;font-weight:700}
    .badge-good{background:#dff4de;color:#2c6b35}
    .badge-mid{background:#fff2cc;color:#8a6b08}
    .badge-low{background:#fde2e2;color:#982f2f}
    .login{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px}
    .lbox{background:#fff;padding:34px;border-radius:18px;width:360px;box-shadow:0 18px 42px rgba(47,111,62,.12)}
    .lbox h2{margin-bottom:20px;color:#2f6f3e}
    .lbox input{width:100%;padding:11px 12px;border:1px solid #bfd3bc;border-radius:10px;margin-bottom:14px}
    .lbox button{width:100%;padding:11px;background:#2f6f3e;color:#fff;border:none;border-radius:10px;cursor:pointer;font-weight:700}
    .err{color:#b42318;margin-bottom:12px}
    .empty{text-align:center;padding:54px;color:#6f8575}
  </style>
</head>
<body>
{% if not auth %}
  <div class="login">
    <div class="lbox">
      <h2>دخول لوحة النتائج</h2>
      {% if err %}<div class="err">{{ err }}</div>{% endif %}
      <form method="POST" action="/login">
        <input type="password" name="p" placeholder="كلمة المرور" autofocus>
        <button>دخول</button>
      </form>
    </div>
  </div>
{% else %}
  <div class="hdr">
    <div>
      <h1>لوحة نتائج بوت تصنيف النباتات</h1>
      <p>{{ st.students }} طالب مسجل</p>
    </div>
    <a href="/logout" class="logout">خروج</a>
  </div>

  <div class="cards">
    <div class="card"><div class="n">{{ st.students }}</div><div class="l">الطلاب</div></div>
    <div class="card"><div class="n">{{ st.questions }}</div><div class="l">الأسئلة</div></div>
    <div class="card"><div class="n">{{ st.sections }}</div><div class="l">الأقسام</div></div>
  </div>

  <div class="wrap">
    <div class="search">
      <input id="si" placeholder="ابحث باسم الطالب..." onkeyup="filterRows()">
    </div>

    {% if students %}
      <table id="t">
        <thead>
          <tr>
            <th>#</th>
            <th>الاسم</th>
            <th>النسبة</th>
            <th>المجموع</th>
            <th>التقدير</th>
            <th>تاريخ التسجيل</th>
          </tr>
        </thead>
        <tbody>
          {% for s in students %}
            {% set p = s.pct|default(0) %}
            <tr>
              <td style="color:#6f8575">{{ loop.index }}</td>
              <td style="font-weight:700">{{ s.full_name }}</td>
              <td>
                <div class="bar-w">
                  <div class="bar-f {{ 'good' if p >= 75 else 'mid' if p >= 50 else 'low' }}" style="width:{{ p }}%"></div>
                </div>
                <span class="pt">{{ p }}%</span>
              </td>
              <td style="color:#56705f">{{ s.score|default(0) }}/{{ s.total_q|default(0) }}</td>
              <td>
                {% if p >= 75 %}
                  <span class="badge badge-good">ممتاز</span>
                {% elif p >= 50 %}
                  <span class="badge badge-mid">جيد</span>
                {% else %}
                  <span class="badge badge-low">يحتاج مراجعة</span>
                {% endif %}
              </td>
              <td style="color:#6f8575;font-size:.85rem">{{ s.registered_at[:10] if s.registered_at else '—' }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% else %}
      <div class="empty">
        <p style="font-size:2.5rem">🌱</p>
        <p style="margin-top:10px">لا توجد نتائج بعد</p>
      </div>
    {% endif %}
  </div>

  <script>
    function filterRows() {
      const value = document.getElementById('si').value.toLowerCase();
      document.querySelectorAll('#t tbody tr').forEach((row) => {
        row.style.display = row.cells[1].textContent.toLowerCase().includes(value) ? '' : 'none';
      });
    }
  </script>
{% endif %}
</body>
</html>"""


@app.route("/login", methods=["POST"])
def login():
    if request.form.get("p") == PASSWORD:
        session["a"] = True
        return redirect("/")
    return render_template_string(PAGE, auth=False, err="كلمة المرور غير صحيحة", students=[], st={})


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    if not session.get("a"):
        return render_template_string(PAGE, auth=False, err=None, students=[], st={})

    with db._connect() as conn:
        students = conn.execute(
            """
            SELECT s.full_name, s.registered_at,
                   p.score, p.total_q, p.pct
            FROM students s
            LEFT JOIN (
                SELECT student_id,
                       SUM(score) AS score,
                       SUM(total_q) AS total_q,
                       CAST(SUM(score) * 100.0 / NULLIF(SUM(total_q), 0) AS INTEGER) AS pct
                FROM section_progress
                WHERE assessed = 1
                GROUP BY student_id
            ) p ON s.id = p.student_id
            ORDER BY p.pct DESC NULLS LAST, s.registered_at ASC
            """
        ).fetchall()

    return render_template_string(
        PAGE,
        auth=True,
        students=students,
        st=db.stats(),
        err=None,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8090))
    app.run(host="0.0.0.0", port=port, debug=False)
