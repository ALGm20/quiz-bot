"""
bot.py — بوت MCQ مصلح مع شكل أزرار محسّن
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

# رموز الخيارات
OPTS = {"A": "🔵", "B": "🟢", "C": "🟡", "D": "🔴"}
LETTERS = {"A": "A", "B": "B", "C": "C", "D": "D"}

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 اختر سكشن للمذاكرة", callback_data="menu_sections")],
    ])

def back_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]
    ])

def build_question_keyboard(q_obj):
    """بناء أزرار الإجابة بشكل جميل"""
    qid = q_obj["id"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔵  A)  {q_obj['option_a']}", callback_data=f"ans_A_{qid}")],
        [InlineKeyboardButton(f"🟢  B)  {q_obj['option_b']}", callback_data=f"ans_B_{qid}")],
        [InlineKeyboardButton(f"🟡  C)  {q_obj['option_c']}", callback_data=f"ans_C_{qid}")],
        [InlineKeyboardButton(f"🔴  D)  {q_obj['option_d']}", callback_data=f"ans_D_{qid}")],
    ])

# ══════════════════════════════════════════════════════════════════
#  /start
# ══════════════════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # امسح أي جلسة قديمة
    ctx.user_data.clear()
    await update.message.reply_text(
        "👋 *أهلاً بك في بوت الاختبارات!*\n\n"
        "اختر سكشناً وابدأ الأسئلة مباشرة 👇",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# ══════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════

async def cb_main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data.clear()
    await q.edit_message_text(
        "🏠 *القائمة الرئيسية*\n\nاختر سكشناً للمذاكرة:",
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
            f"{emoji}  {sec['name']}   ┃   {cnt} سؤال",
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
    emoji   = section["emoji"] or "📖"
    desc    = section["description"] or ""

    kbd = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡️ 10 أسئلة عشوائية",  callback_data=f"start_{sec_id}_10")],
        [InlineKeyboardButton("📋 كل الأسئلة",         callback_data=f"start_{sec_id}_all")],
        [InlineKeyboardButton("🔙 رجوع",               callback_data="menu_sections")],
    ])

    await q.edit_message_text(
        f"{emoji} *{section['name']}*\n"
        f"{'_' + desc + '_' if desc else ''}\n\n"
        f"📝 عدد الأسئلة المتاحة: *{cnt}*\n\n"
        f"اختر نوع الاختبار:",
        parse_mode="Markdown",
        reply_markup=kbd
    )

# ══════════════════════════════════════════════════════════════════
#  START QUIZ
# ══════════════════════════════════════════════════════════════════

async def cb_start_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q      = update.callback_query
    await q.answer()
    parts  = q.data.split("_")   # start_<sec_id>_<count>
    sec_id = int(parts[1])
    limit  = None if parts[2] == "all" else int(parts[2])

    questions = db.get_questions(sec_id, limit)
    if not questions:
        await q.edit_message_text("⚠️ لا توجد أسئلة في هذا السكشن.", reply_markup=back_main())
        return

    import random
    questions = list(questions)
    random.shuffle(questions)

    # احفظ الجلسة
    ctx.user_data["session"] = {
        "sec_id": sec_id,
        "qs":    questions,
        "idx":   0,
        "score": 0,
        "total": len(questions),
    }

    section = db.get_section(sec_id)
    emoji   = section["emoji"] or "📖"

    await q.edit_message_text(
        f"{emoji} *{section['name']}*\n\n"
        f"🎯 عدد الأسئلة: *{len(questions)}*\n\n"
        f"ابدأ الآن! 🚀",
        parse_mode="Markdown"
    )
    await asyncio.sleep(0.8)
    await _send_question(update, ctx)

# ══════════════════════════════════════════════════════════════════
#  SEND QUESTION
# ══════════════════════════════════════════════════════════════════

async def _send_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sess = ctx.user_data.get("session")
    if not sess:
        try:
            await update.callback_query.edit_message_text(
                "⚠️ انتهت الجلسة. اضغط /start للبدء من جديد."
            )
        except Exception:
            pass
        return

    idx   = sess["idx"]
    total = sess["total"]

    if idx >= total:
        await _finish_quiz(update, ctx)
        return

    q_obj = sess["qs"][idx]

    # شريط التقدم
    filled = round((idx / total) * 10)
    bar = "█" * filled + "░" * (10 - filled)
    pct_done = round((idx / total) * 100)

    text = (
        f"*سؤال {idx + 1} من {total}*\n"
        f"`{bar}` {pct_done}%\n\n"
        f"❓ *{q_obj['question_text']}*"
    )

    kbd = build_question_keyboard(q_obj)

    try:
        await update.callback_query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=kbd
        )
    except Exception as e:
        logger.warning(f"edit failed: {e}")
        try:
            await update.effective_chat.send_message(
                text, parse_mode="Markdown", reply_markup=kbd
            )
        except Exception as e2:
            logger.error(f"send also failed: {e2}")

# ══════════════════════════════════════════════════════════════════
#  ANSWER HANDLER
# ══════════════════════════════════════════════════════════════════

async def cb_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    sess = ctx.user_data.get("session")
    if not sess:
        await q.edit_message_text(
            "⚠️ انتهت الجلسة.\n\nاضغط /start للبدء من جديد.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 ابدأ من جديد", callback_data="main_menu")]
            ])
        )
        return

    # استخرج الإجابة ورقم السؤال من callback_data
    # الشكل: ans_A_123
    parts    = q.data.split("_")
    user_ans = parts[1].upper()   # A / B / C / D

    idx   = sess["idx"]
    q_obj = sess["qs"][idx]
    correct    = q_obj["correct_answer"].upper()
    is_correct = (user_ans == correct)

    if is_correct:
        sess["score"] += 1

    # خريطة الخيارات
    opt = {
        "A": q_obj["option_a"],
        "B": q_obj["option_b"],
        "C": q_obj["option_c"],
        "D": q_obj["option_d"],
    }

    # رسالة النتيجة
    color = {"A": "🔵", "B": "🟢", "C": "🟡", "D": "🔴"}

    if is_correct:
        result = f"✅ *إجابة صحيحة!*\n{color[correct]}  {correct})  {opt[correct]}"
    else:
        result = (
            f"❌ *إجابة خاطئة!*\n"
            f"اخترت: {color[user_ans]}  {user_ans})  {opt[user_ans]}\n\n"
            f"✅ الصحيحة: {color[correct]}  {correct})  {opt[correct]}"
        )

    exp = q_obj.get("explanation", "") or ""
    exp_line = f"\n\n💡 _{exp}_" if exp else ""

    # انتقل للسؤال التالي
    sess["idx"] += 1
    ctx.user_data["session"] = sess

    remaining = sess["total"] - sess["idx"]
    if sess["idx"] < sess["total"]:
        btn_label = f"التالي ←  (سؤال {sess['idx'] + 1}/{sess['total']})"
    else:
        btn_label = "عرض النتيجة النهائية 🏁"

    await q.edit_message_text(
        f"❓ *{q_obj['question_text']}*\n\n"
        f"{'─' * 20}\n\n"
        f"{result}{exp_line}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(btn_label, callback_data="next_q")]
        ])
    )

async def cb_next_q(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await _send_question(update, ctx)

# ══════════════════════════════════════════════════════════════════
#  FINISH QUIZ — النتيجة النهائية
# ══════════════════════════════════════════════════════════════════

async def _finish_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sess  = ctx.user_data.pop("session", {})
    score = sess.get("score", 0)
    total = sess.get("total", 1)
    pct   = round((score / total) * 100)

    # التقدير
    if pct == 100:
        grade, msg = "ممتاز 🏆", "علامة كاملة! أحسنت جداً 🎯"
    elif pct >= 90:
        grade, msg = "ممتاز 🥇", "أداء رائع جداً! استمر 💪"
    elif pct >= 75:
        grade, msg = "جيد جداً 🥈", "أداء جيد، قريب من القمة!"
    elif pct >= 60:
        grade, msg = "جيد 🥉", "مقبول، راجع الأسئلة التي أخطأت فيها."
    elif pct >= 50:
        grade, msg = "مقبول 📘", "تحتاج مزيداً من المراجعة."
    else:
        grade, msg = "راجع المادة 📖", "لا تيأس، كرر الاختبار بعد المراجعة!"

    # شريط النتيجة
    filled = round(pct / 10)
    bar = "█" * filled + "░" * (10 - filled)

    # نجوم
    if pct == 100:   stars = "⭐⭐⭐⭐⭐"
    elif pct >= 80:  stars = "⭐⭐⭐⭐"
    elif pct >= 60:  stars = "⭐⭐⭐"
    elif pct >= 40:  stars = "⭐⭐"
    else:            stars = "⭐"

    sec_id = sess.get("sec_id")

    kbd = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 أعد الاختبار",      callback_data=f"sec_{sec_id}")] if sec_id else [],
        [InlineKeyboardButton("📚 اختر سكشن آخر",     callback_data="menu_sections")],
        [InlineKeyboardButton("🏠 القائمة الرئيسية",  callback_data="main_menu")],
    ])

    await update.callback_query.edit_message_text(
        f"🎉 *انتهى الاختبار!*\n\n"
        f"`{bar}` {pct}%\n\n"
        f"✅ الإجابات الصحيحة: *{score}*\n"
        f"❌ الإجابات الخاطئة: *{total - score}*\n"
        f"📊 المجموع: *{score} / {total}*\n\n"
        f"{stars}\n"
        f"التقدير: *{grade}*\n"
        f"_{msg}_",
        parse_mode="Markdown",
        reply_markup=kbd
    )

# ══════════════════════════════════════════════════════════════════
#  ADMIN /stats
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
    app.add_handler(CallbackQueryHandler(cb_answer,         pattern=r"^ans_[AaBbCcDd]_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_next_q,         pattern="^next_q$"))

    logger.info("Bot started ✅")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
