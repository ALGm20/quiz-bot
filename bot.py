"""
bot.py — بوت اختبارات MCQ مبسّط
بدون تسجيل دخول — فقط اختر سكشن وابدأ الأسئلة
"""
import logging
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes,
)
from database import Database

logging.basicConfig(format="%(asctime)s — %(levelname)s — %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database("quiz_bot.db")


# ══════════════════════════════════════════════════════════════════
#  KEYBOARDS
# ══════════════════════════════════════════════════════════════════

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 اختر سكشن", callback_data="menu_sections")],
    ])

def back_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
    ])


# ══════════════════════════════════════════════════════════════════
#  /start
# ══════════════════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *أهلاً بك في بوت الاختبارات!*\n\n"
        "اختر سكشناً وابدأ الأسئلة مباشرة:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )


# ══════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════

async def cb_main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "📚 *القائمة الرئيسية* — اختر سكشناً:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )


# ══════════════════════════════════════════════════════════════════
#  SECTIONS LIST
# ══════════════════════════════════════════════════════════════════

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
        emoji = sec["emoji"] or "📖"
        rows.append([InlineKeyboardButton(
            f"{emoji} {sec['name']}  ({cnt} سؤال)",
            callback_data=f"sec_{sec['id']}"
        )])

    await q.edit_message_text(
        "📚 *اختر السكشن:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(rows)
    )


# ══════════════════════════════════════════════════════════════════
#  SECTION DETAIL
# ══════════════════════════════════════════════════════════════════

async def cb_section_detail(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    sec_id  = int(q.data.split("_")[1])
    section = db.get_section(sec_id)
    cnt     = db.count_q(sec_id)

    kbd = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ 10 أسئلة عشوائية",  callback_data=f"start_{sec_id}_10")],
        [InlineKeyboardButton("📋 كل الأسئلة",          callback_data=f"start_{sec_id}_all")],
        [InlineKeyboardButton("🔙 رجوع",                callback_data="menu_sections")],
    ])

    emoji = section["emoji"] or "📖"
    desc  = section["description"] or ""
    await q.edit_message_text(
        f"{emoji} *{section['name']}*\n"
        f"{desc}\n\n"
        f"📝 عدد الأسئلة: *{cnt}*",
        parse_mode="Markdown",
        reply_markup=kbd
    )


# ══════════════════════════════════════════════════════════════════
#  START QUIZ
# ══════════════════════════════════════════════════════════════════

async def cb_start_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q     = update.callback_query
    await q.answer()
    parts  = q.data.split("_")          # start_<sec_id>_<count>
    sec_id = int(parts[1])
    limit  = None if parts[2] == "all" else int(parts[2])

    questions = db.get_questions(sec_id, limit)
    if not questions:
        await q.edit_message_text("⚠️ لا توجد أسئلة في هذا السكشن.", reply_markup=back_main())
        return

    import random
    random.shuffle(questions)

    ctx.user_data["session"] = {
        "sec_id": sec_id,
        "qs":     questions,
        "idx":    0,
        "score":  0,
        "total":  len(questions),
    }

    section = db.get_section(sec_id)
    await q.edit_message_text(
        f"🚀 *{section['name']}* — {len(questions)} سؤال\nاستعد! ⏱️",
        parse_mode="Markdown"
    )
    await asyncio.sleep(0.5)
    await _send_question(update, ctx)


# ══════════════════════════════════════════════════════════════════
#  SEND QUESTION
# ══════════════════════════════════════════════════════════════════

async def _send_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sess  = ctx.user_data.get("session")
    if not sess:
        return

    idx   = sess["idx"]
    total = sess["total"]

    if idx >= total:
        await _finish_quiz(update, ctx)
        return

    q_obj = sess["qs"][idx]

    # شريط التقدم
    filled = min(idx, 10)
    empty  = min(total - idx, 10)
    bar    = "🟩" * filled + "⬜" * empty
    if total > 10:
        bar += f"  {idx}/{total}"

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
        await update.effective_chat.send_message(
            text, parse_mode="Markdown", reply_markup=kbd
        )


# ══════════════════════════════════════════════════════════════════
#  ANSWER HANDLER
# ══════════════════════════════════════════════════════════════════

async def cb_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    sess = ctx.user_data.get("session")
    if not sess:
        await q.edit_message_text("انتهت الجلسة، ابدأ من /start")
        return

    parts    = q.data.split("_")      # ans_<letter>_<qid>
    user_ans = parts[1]
    q_obj    = sess["qs"][sess["idx"]]
    correct  = q_obj["correct_answer"].upper()
    is_right = user_ans == correct

    if is_right:
        sess["score"] += 1

    opt = {
        "A": q_obj["option_a"], "B": q_obj["option_b"],
        "C": q_obj["option_c"], "D": q_obj["option_d"]
    }

    if is_right:
        result = "✅ *إجابة صحيحة!*"
    else:
        result = f"❌ *خطأ!*\nالإجابة الصحيحة: *{correct})* {opt[correct]}"

    exp      = q_obj.get("explanation", "")
    exp_line = f"\n\n💡 _{exp}_" if exp else ""

    sess["idx"] += 1
    ctx.user_data["session"] = sess

    remaining = sess["total"] - sess["idx"]
    if sess["idx"] < sess["total"]:
        next_label = f"التالي  ({sess['idx'] + 1}/{sess['total']}) ➡️"
    else:
        next_label = "عرض النتيجة 🏁"

    await q.edit_message_text(
        f"❓ {q_obj['question_text']}\n\n{result}{exp_line}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(next_label, callback_data="next_q")]
        ])
    )


async def cb_next_q(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await _send_question(update, ctx)


# ══════════════════════════════════════════════════════════════════
#  FINISH — النتيجة النهائية
# ══════════════════════════════════════════════════════════════════

async def _finish_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sess  = ctx.user_data.pop("session", {})
    score = sess.get("score", 0)
    total = sess.get("total", 1)
    pct   = round((score / total) * 100)

    # تقييم نصي
    if pct == 100:
        grade = "ممتاز 🏆"
        msg   = "أحسنت! حصلت على العلامة الكاملة 🎯"
    elif pct >= 90:
        grade = "ممتاز 🥇"
        msg   = "أداء رائع جداً!"
    elif pct >= 75:
        grade = "جيد جداً 🥈"
        msg   = "أداء جيد، استمر!"
    elif pct >= 60:
        grade = "جيد 🥉"
        msg   = "مقبول، راجع الأسئلة التي أخطأت فيها."
    elif pct >= 50:
        grade = "مقبول 📘"
        msg   = "تحتاج مزيداً من المراجعة."
    else:
        grade = "راجع المادة 📖"
        msg   = "لا تستسلم، كرر الاختبار بعد المراجعة!"

    # شريط النتيجة البصري
    filled_bar = round(pct / 10)
    bar = "🟩" * filled_bar + "⬜" * (10 - filled_bar)

    kbd = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 أعد الاختبار",       callback_data=f"sec_{sess['sec_id']}")],
        [InlineKeyboardButton("📚 اختر سكشن آخر",      callback_data="menu_sections")],
        [InlineKeyboardButton("🏠 القائمة الرئيسية",   callback_data="main_menu")],
    ])

    await update.callback_query.edit_message_text(
        f"🎉 *انتهى الاختبار!*\n\n"
        f"{bar}\n\n"
        f"النتيجة: *{score} / {total}*  ({pct}%)\n"
        f"التقدير: {grade}\n\n"
        f"_{msg}_",
        parse_mode="Markdown",
        reply_markup=kbd
    )


# ══════════════════════════════════════════════════════════════════
#  ADMIN — /stats
# ══════════════════════════════════════════════════════════════════

async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    st = db.stats()
    sections = db.get_sections()
    lines = ["📊 *إحصائيات البوت:*\n"]
    lines.append(f"📦 سكشنات: {st['sections']}")
    lines.append(f"❓ أسئلة: {st['questions']}\n")
    for sec in sections:
        cnt = db.count_q(sec["id"])
        lines.append(f"{sec['emoji'] or '📖'} {sec['name']}: {cnt} سؤال")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
    app   = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("stats", cmd_stats))

    app.add_handler(CallbackQueryHandler(cb_main_menu,      pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(cb_sections,       pattern="^menu_sections$"))
    app.add_handler(CallbackQueryHandler(cb_section_detail, pattern=r"^sec_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_start_quiz,     pattern=r"^start_\d+_(all|\d+)$"))
    app.add_handler(CallbackQueryHandler(cb_answer,         pattern=r"^ans_[ABCD]_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_next_q,         pattern="^next_q$"))

    logger.info("Bot started ✅")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
