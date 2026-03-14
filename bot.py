"""
bot.py — بوت الاختبارات MCQ مبني على السكشنز
كل سكشن = موضوع مستقل، الأسئلة تنزل بشكل متواصل واحدة تلو الأخرى
"""
import logging
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler,
)
from database import Database

logging.basicConfig(format="%(asctime)s — %(levelname)s — %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

WAITING_NAME = 1
db = Database("quiz_bot.db")

# ══════════════════════════════════════════════════════════════════
#  KEYBOARDS & MENUS
# ══════════════════════════════════════════════════════════════════

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 اختر سكشن للدراسة",    callback_data="menu_sections")],
        [InlineKeyboardButton("🎯 الاختبار اليومي",        callback_data="menu_daily")],
        [InlineKeyboardButton("📊 نتائجي",                 callback_data="menu_scores")],
        [InlineKeyboardButton("🏆 لوحة الشرف",             callback_data="menu_leaders")],
    ])


def back_main():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]])


# ══════════════════════════════════════════════════════════════════
#  REGISTRATION
# ══════════════════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    student = db.get_student(uid)
    if student:
        await update.message.reply_text(
            f"👋 أهلاً *{student['full_name']}*!\nاختر ما تريد:",
            parse_mode="Markdown", reply_markup=main_menu_keyboard()
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "🎓 *مرحباً بك في بوت الاختبارات!*\n\n"
        "أرسل *اسمك الثلاثي* كما هو مسجّل لدى المشرف:",
        parse_mode="Markdown"
    )
    return WAITING_NAME


async def register_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    uid  = update.effective_user.id
    result = db.register_student(name, uid)

    if result == "not_found":
        await update.message.reply_text(
            "❌ الاسم غير موجود في القائمة.\n"
            "تأكد من كتابته بالضبط أو تواصل مع المشرف."
        )
        return WAITING_NAME

    if result == "taken":
        await update.message.reply_text("⚠️ هذا الاسم مسجّل بحساب آخر. تواصل مع المشرف.")
        return WAITING_NAME

    await update.message.reply_text(
        f"✅ *تم التسجيل بنجاح!*\nأهلاً *{name}* 🎉",
        parse_mode="Markdown", reply_markup=main_menu_keyboard()
    )
    return ConversationHandler.END


async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END


# ══════════════════════════════════════════════════════════════════
#  MAIN MENU callback
# ══════════════════════════════════════════════════════════════════

async def cb_main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = update.effective_user.id
    s = db.get_student(uid)
    if not s:
        await q.edit_message_text("يرجى التسجيل أولاً /start")
        return
    await q.edit_message_text(
        f"👋 *{s['full_name']}* — القائمة الرئيسية:",
        parse_mode="Markdown", reply_markup=main_menu_keyboard()
    )


def require_student(fn):
    """Decorator: checks student is registered before running callback."""
    async def wrapper(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        s = db.get_student(uid)
        if not s:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text("يرجى التسجيل أولاً /start")
            return
        ctx.user_data["student"] = s
        return await fn(update, ctx)
    return wrapper


# ══════════════════════════════════════════════════════════════════
#  SECTIONS LIST
# ══════════════════════════════════════════════════════════════════

@require_student
async def cb_sections(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    sections = db.get_sections()
    if not sections:
        await q.edit_message_text("⚠️ لا توجد سكشنات بعد.", reply_markup=back_main())
        return

    rows = []
    for sec in sections:
        cnt = db.count_q(sec["id"])
        rows.append([InlineKeyboardButton(
            f"{'🦠' if 'فير' in sec['name'] else '⚗️' if 'ايض' in sec['name'] or 'أيض' in sec['name'] else '📖'} {sec['name']}  ({cnt} سؤال)",
            callback_data=f"sec_{sec['id']}"
        )])
    rows.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])

    await q.edit_message_text(
        "📚 *اختر السكشن الذي تريد دراسته:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(rows)
    )


# ══════════════════════════════════════════════════════════════════
#  SECTION DETAIL
# ══════════════════════════════════════════════════════════════════

@require_student
async def cb_section_detail(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    sec_id  = int(q.data.split("_")[1])
    section = db.get_section(sec_id)
    cnt     = db.count_q(sec_id)

    kbd = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ ابدأ (10 أسئلة عشوائية)", callback_data=f"start_{sec_id}_10")],
        [InlineKeyboardButton("📋 اختبار كامل (كل الأسئلة)",  callback_data=f"start_{sec_id}_all")],
        [InlineKeyboardButton("🔙 رجوع",                      callback_data="menu_sections")],
    ])

    desc = section["description"] or ""
    await q.edit_message_text(
        f"{'🦠' if 'فير' in section['name'] else '📖'} *{section['name']}*\n"
        f"{desc}\n\n"
        f"📝 عدد الأسئلة: *{cnt}*",
        parse_mode="Markdown", reply_markup=kbd
    )


# ══════════════════════════════════════════════════════════════════
#  START QUIZ SESSION
# ══════════════════════════════════════════════════════════════════

@require_student
async def cb_start_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    parts   = q.data.split("_")       # start_<sec_id>_<count>
    sec_id  = int(parts[1])
    limit   = None if parts[2] == "all" else int(parts[2])
    student = ctx.user_data["student"]

    questions = db.get_questions(sec_id, limit)
    if not questions:
        await q.edit_message_text("⚠️ لا توجد أسئلة في هذا السكشن.", reply_markup=back_main())
        return

    import random
    random.shuffle(questions)

    session_id = db.new_session(student["id"], sec_id, len(questions))
    ctx.user_data["session"] = {
        "sid":      session_id,
        "sec_id":   sec_id,
        "qs":       questions,
        "idx":      0,
        "score":    0,
        "total":    len(questions),
        "is_daily": False,
    }

    section = db.get_section(sec_id)
    await q.edit_message_text(
        f"🚀 *{section['name']}* — {len(questions)} سؤال\nاستعد! ⏱️",
        parse_mode="Markdown"
    )
    await asyncio.sleep(0.6)
    await _send_question(update, ctx)


# ══════════════════════════════════════════════════════════════════
#  CORE QUESTION DISPLAY
# ══════════════════════════════════════════════════════════════════

async def _send_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sess = ctx.user_data.get("session")
    if not sess:
        return

    idx   = sess["idx"]
    total = sess["total"]
    if idx >= total:
        await _finish_quiz(update, ctx)
        return

    q_obj = sess["qs"][idx]

    # Progress bar
    done  = idx
    left  = total - idx
    bar   = "🟩" * min(done, 10) + "⬜" * min(left, 10)
    if total > 10:
        bar += f" ({idx}/{total})"

    text = (
        f"*سؤال {idx + 1} من {total}*\n{bar}\n\n"
        f"❓ {q_obj['question_text']}"
    )

    kbd = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🅰  {q_obj['option_a']}", callback_data=f"ans_A_{q_obj['id']}")],
        [InlineKeyboardButton(f"🅱  {q_obj['option_b']}", callback_data=f"ans_B_{q_obj['id']}")],
        [InlineKeyboardButton(f"🅲  {q_obj['option_c']}", callback_data=f"ans_C_{q_obj['id']}")],
        [InlineKeyboardButton(f"🅳  {q_obj['option_d']}", callback_data=f"ans_D_{q_obj['id']}")],
    ])

    try:
        await update.callback_query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=kbd
        )
    except Exception:
        # fallback: send new message
        await update.effective_chat.send_message(
            text, parse_mode="Markdown", reply_markup=kbd
        )


# ══════════════════════════════════════════════════════════════════
#  ANSWER HANDLER  ← the heart of the flow
# ══════════════════════════════════════════════════════════════════

async def cb_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    sess = ctx.user_data.get("session")
    if not sess:
        await q.edit_message_text("انتهت الجلسة، ابدأ من /start")
        return

    parts       = q.data.split("_")   # ans_<letter>_<qid>
    user_ans    = parts[1]
    q_id        = int(parts[2])

    # Find current question
    idx   = sess["idx"]
    q_obj = sess["qs"][idx]

    correct    = q_obj["correct_answer"].upper()
    is_correct = (user_ans == correct)

    if is_correct:
        sess["score"] += 1

    db.save_answer(sess["sid"], q_id, user_ans, is_correct)

    # Build option map for feedback
    opt = {"A": q_obj["option_a"], "B": q_obj["option_b"],
           "C": q_obj["option_c"], "D": q_obj["option_d"]}

    if is_correct:
        result_line = f"✅ *إجابة صحيحة!*"
    else:
        result_line = (
            f"❌ *خطأ!*\n"
            f"الإجابة الصحيحة: *{correct})* {opt[correct]}"
        )

    exp = q_obj.get("explanation", "")
    exp_line = f"\n\n💡 _{exp}_" if exp else ""

    # Move pointer
    sess["idx"] += 1
    ctx.user_data["session"] = sess

    next_num = sess["idx"] + 1
    total    = sess["total"]
    next_label = f"التالي  ({next_num}/{total}) ➡️" if sess["idx"] < total else "عرض النتيجة 🏁"

    feedback_text = (
        f"❓ {q_obj['question_text']}\n\n"
        f"{result_line}{exp_line}"
    )

    kbd = InlineKeyboardMarkup([
        [InlineKeyboardButton(next_label, callback_data="next_q")]
    ])

    await q.edit_message_text(feedback_text, parse_mode="Markdown", reply_markup=kbd)


async def cb_next_q(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await _send_question(update, ctx)


# ══════════════════════════════════════════════════════════════════
#  FINISH QUIZ
# ══════════════════════════════════════════════════════════════════

async def _finish_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sess  = ctx.user_data.pop("session", {})
    score = sess.get("score", 0)
    total = sess.get("total", 1)
    pct   = round((score / total) * 100)

    db.complete_session(sess["sid"], score)

    if pct >= 90:   grade = "ممتاز 🏆"
    elif pct >= 75: grade = "جيد جداً 🥈"
    elif pct >= 60: grade = "جيد 🥉"
    else:           grade = "راجع المادة 📖"

    stars = "⭐" * (pct // 20) or "—"

    kbd = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 إعادة نفس السكشن", callback_data=f"sec_{sess['sec_id']}")],
        [InlineKeyboardButton("📚 اختر سكشن آخر",    callback_data="menu_sections")],
        [InlineKeyboardButton("🏠 القائمة الرئيسية",  callback_data="main_menu")],
    ])

    await update.callback_query.edit_message_text(
        f"🎉 *انتهى الاختبار!*\n\n"
        f"النتيجة: *{score} / {total}*  ({pct}%)\n"
        f"التقدير: {grade}\n"
        f"{stars}",
        parse_mode="Markdown", reply_markup=kbd
    )


# ══════════════════════════════════════════════════════════════════
#  DAILY QUIZ
# ══════════════════════════════════════════════════════════════════

@require_student
async def cb_daily(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    student = ctx.user_data["student"]
    from datetime import date
    today   = date.today().isoformat()

    done, sc, tot = db.check_daily(student["id"], today)
    if done:
        pct = round(sc / tot * 100) if tot else 0
        await q.edit_message_text(
            f"✅ أجريت الاختبار اليومي اليوم!\n\n"
            f"نتيجتك: *{sc}/{tot}* ({pct}%)\n\nعد غداً 📅",
            parse_mode="Markdown", reply_markup=back_main()
        )
        return

    questions = db.daily_questions(today)
    if not questions:
        await q.edit_message_text("⚠️ لا توجد أسئلة للاختبار اليومي.", reply_markup=back_main())
        return

    session_id = db.new_session(student["id"], None, len(questions), is_daily=True, daily_date=today)
    ctx.user_data["session"] = {
        "sid": session_id, "sec_id": None,
        "qs": questions, "idx": 0,
        "score": 0, "total": len(questions),
        "is_daily": True,
    }
    await q.edit_message_text("🎯 *الاختبار اليومي* — 10 أسئلة من كل السكشنات\nاستعد! ⏱️",
                               parse_mode="Markdown")
    await asyncio.sleep(0.6)
    await _send_question(update, ctx)


# ══════════════════════════════════════════════════════════════════
#  MY SCORES
# ══════════════════════════════════════════════════════════════════

@require_student
async def cb_scores(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    student = ctx.user_data["student"]
    rows    = db.student_sessions(student["id"])
    if not rows:
        await q.edit_message_text("لا توجد نتائج بعد — ابدأ اختباراً!", reply_markup=back_main())
        return

    lines = ["📊 *آخر 10 اختبارات:*\n"]
    for r in rows:
        pct  = round(r["score"] / r["total_questions"] * 100) if r["total_questions"] else 0
        name = r["section_name"] or "اختبار يومي"
        dt   = r["started_at"][:10]
        lines.append(f"• {dt} — {name}: {r['score']}/{r['total_questions']} ({pct}%)")

    await q.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=back_main())


# ══════════════════════════════════════════════════════════════════
#  LEADERBOARD
# ══════════════════════════════════════════════════════════════════

@require_student
async def cb_leaders(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rows = db.leaderboard()
    if not rows:
        await q.edit_message_text("لا توجد بيانات بعد.", reply_markup=back_main())
        return
    medals = ["🥇","🥈","🥉"] + ["🔹"]*7
    lines  = ["🏆 *لوحة الشرف:*\n"]
    for i, r in enumerate(rows):
        lines.append(f"{medals[i]} {r['full_name']} — {r['avg_pct']}%  ({r['total']} اختبار)")
    await q.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=back_main())


# ══════════════════════════════════════════════════════════════════
#  ADMIN
# ══════════════════════════════════════════════════════════════════

async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    st = db.stats()
    await update.message.reply_text(
        f"📈 *إحصائيات:*\n\n"
        f"👥 طلاب مسجلون: {st['registered']}/{st['total_students']}\n"
        f"📦 سكشنات: {st['sections']}\n"
        f"❓ أسئلة: {st['questions']}\n"
        f"📋 اختبارات منجزة: {st['sessions']}",
        parse_mode="Markdown"
    )


# ══════════════════════════════════════════════════════════════════
#  UNREGISTERED GUARD
# ══════════════════════════════════════════════════════════════════

async def guard_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not db.get_student(update.effective_user.id):
        await update.message.reply_text("يرجى التسجيل أولاً عبر /start")


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
    app   = Application.builder().token(TOKEN).build()

    # Registration
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)]},
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
    ))

    # Admin
    app.add_handler(CommandHandler("stats", cmd_stats))

    # Menus
    app.add_handler(CallbackQueryHandler(cb_main_menu,     pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(cb_sections,      pattern="^menu_sections$"))
    app.add_handler(CallbackQueryHandler(cb_daily,         pattern="^menu_daily$"))
    app.add_handler(CallbackQueryHandler(cb_scores,        pattern="^menu_scores$"))
    app.add_handler(CallbackQueryHandler(cb_leaders,       pattern="^menu_leaders$"))

    # Section detail
    app.add_handler(CallbackQueryHandler(cb_section_detail, pattern=r"^sec_\d+$"))

    # Quiz flow
    app.add_handler(CallbackQueryHandler(cb_start_quiz, pattern=r"^start_\d+_(all|\d+)$"))
    app.add_handler(CallbackQueryHandler(cb_answer,     pattern=r"^ans_[ABCD]_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_next_q,     pattern="^next_q$"))

    # Guard
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guard_text))

    logger.info("Bot started ✅")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
