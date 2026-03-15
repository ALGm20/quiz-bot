"""
bot.py — الجلسة محفوظة في SQLite (لا تضيع عند restart)
"""
import logging
import asyncio
import os
import random
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

def question_keyboard(q_obj):
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
    uid = update.effective_user.id
    db.delete_session(uid)   # امسح أي جلسة قديمة
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
    uid = update.effective_user.id
    db.delete_session(uid)
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
        cnt   = db.count_q(sec["id"])
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
        [InlineKeyboardButton("⚡️ 10 أسئلة عشوائية", callback_data=f"start_{sec_id}_10")],
        [InlineKeyboardButton("📋 كل الأسئلة",        callback_data=f"start_{sec_id}_all")],
        [InlineKeyboardButton("🔙 رجوع",              callback_data="menu_sections")],
    ])

    await q.edit_message_text(
        f"{emoji} *{section['name']}*\n"
        f"{'_' + desc + '_' if desc else ''}\n\n"
        f"📝 عدد الأسئلة: *{cnt}*\n\n"
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
    uid    = update.effective_user.id
    parts  = q.data.split("_")
    sec_id = int(parts[1])
    limit  = None if parts[2] == "all" else int(parts[2])

    questions = db.get_questions(sec_id, limit)
    if not questions:
        await q.edit_message_text("⚠️ لا توجد أسئلة.", reply_markup=back_main())
        return

    questions = list(questions)
    random.shuffle(questions)

    # ← احفظ الجلسة في قاعدة البيانات
    db.save_session(uid, sec_id, questions, idx=0, score=0, total=len(questions))

    section = db.get_section(sec_id)
    emoji   = section["emoji"] or "📖"

    await q.edit_message_text(
        f"{emoji} *{section['name']}*\n\n"
        f"🎯 عدد الأسئلة: *{len(questions)}*\n\n"
        f"ابدأ الآن! 🚀",
        parse_mode="Markdown"
    )
    await asyncio.sleep(0.6)
    await _send_question(update, ctx)

# ══════════════════════════════════════════════════════════════════
#  SEND QUESTION — يقرأ من DB
# ══════════════════════════════════════════════════════════════════

async def _send_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    sess = db.get_session(uid)

    if not sess:
        try:
            await update.callback_query.edit_message_text(
                "⚠️ انتهت الجلسة.\n\nاضغط /start للبدء من جديد.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 ابدأ من جديد", callback_data="main_menu")]
                ])
            )
        except Exception:
            pass
        return

    idx   = sess["idx"]
    total = sess["total"]

    if idx >= total:
        await _finish_quiz(update, ctx, sess)
        return

    q_obj = sess["qs"][idx]

    # شريط التقدم
    filled = round((idx / total) * 10) if total > 0 else 0
    bar    = "█" * filled + "░" * (10 - filled)
    pct    = round((idx / total) * 100) if total > 0 else 0

    text = (
        f"*سؤال {idx + 1} من {total}*\n"
        f"`{bar}` {pct}%\n\n"
        f"❓ *{q_obj['question_text']}*"
    )

    kbd = question_keyboard(q_obj)

    try:
        await update.callback_query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=kbd
        )
    except Exception as e:
        logger.warning(f"edit_message failed: {e}")
        try:
            await update.effective_chat.send_message(
                text, parse_mode="Markdown", reply_markup=kbd
            )
        except Exception as e2:
            logger.error(f"send_message also failed: {e2}")

# ══════════════════════════════════════════════════════════════════
#  ANSWER HANDLER — يقرأ ويحدّث DB
# ══════════════════════════════════════════════════════════════════

async def cb_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q   = update.callback_query
    await q.answer()
    uid = update.effective_user.id

    # ← اقرأ الجلسة من DB
    sess = db.get_session(uid)
    if not sess:
        await q.edit_message_text(
            "⚠️ انتهت الجلسة أو تمت إعادة تشغيل البوت.\n\n"
            "اضغط /start للبدء من جديد.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 ابدأ من جديد", callback_data="main_menu")]
            ])
        )
        return

    # استخرج الإجابة: callback_data = ans_A_123
    parts    = q.data.split("_")
    user_ans = parts[1].upper()

    idx    = sess["idx"]
    q_obj  = sess["qs"][idx]
    correct    = q_obj["correct_answer"].upper()
    is_correct = (user_ans == correct)

    new_score = sess["score"] + (1 if is_correct else 0)
    new_idx   = idx + 1

    # ← احفظ التقدم في DB فوراً
    db.update_session(uid, new_idx, new_score)

    # خريطة الألوان والخيارات
    color = {"A": "🔵", "B": "🟢", "C": "🟡", "D": "🔴"}
    opt   = {
        "A": q_obj["option_a"], "B": q_obj["option_b"],
        "C": q_obj["option_c"], "D": q_obj["option_d"],
    }

    if is_correct:
        result = (
            f"✅ *إجابة صحيحة!*\n"
            f"{color[correct]}  {correct})  {opt[correct]}"
        )
    else:
        result = (
            f"❌ *إجابة خاطئة!*\n"
            f"اخترت: {color[user_ans]}  {user_ans})  {opt[user_ans]}\n\n"
            f"✅ الصحيحة: {color[correct]}  {correct})  {opt[correct]}"
        )

    exp      = q_obj.get("explanation") or ""
    exp_line = f"\n\n💡 _{exp}_" if exp else ""

    # زر التالي
    remaining = sess["total"] - new_idx
    if remaining > 0:
        btn_label = f"التالي ←   (سؤال {new_idx + 1} من {sess['total']})"
    else:
        btn_label = "عرض النتيجة النهائية 🏁"

    await q.edit_message_text(
        f"❓ *{q_obj['question_text']}*\n\n"
        f"{'─' * 18}\n\n"
        f"{result}{exp_line}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(btn_label, callback_data="next_q")]
        ])
    )

async def cb_next_q(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid  = update.effective_user.id
    sess = db.get_session(uid)

    if not sess:
        await q.edit_message_text(
            "⚠️ انتهت الجلسة. اضغط /start للبدء.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 ابدأ", callback_data="main_menu")]
            ])
        )
        return

    if sess["idx"] >= sess["total"]:
        await _finish_quiz(update, ctx, sess)
    else:
        await _send_question(update, ctx)

# ══════════════════════════════════════════════════════════════════
#  FINISH QUIZ
# ══════════════════════════════════════════════════════════════════

async def _finish_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE, sess: dict):
    uid   = update.effective_user.id
    db.delete_session(uid)

    score = sess["score"]
    total = sess["total"]
    pct   = round((score / total) * 100) if total else 0

    if pct == 100:   grade, msg = "ممتاز 🏆",      "علامة كاملة! أحسنت جداً 🎯"
    elif pct >= 90:  grade, msg = "ممتاز 🥇",      "أداء رائع جداً! استمر 💪"
    elif pct >= 75:  grade, msg = "جيد جداً 🥈",   "أداء جيد، قريب من القمة!"
    elif pct >= 60:  grade, msg = "جيد 🥉",        "مقبول، راجع الأسئلة التي أخطأت فيها."
    elif pct >= 50:  grade, msg = "مقبول 📘",      "تحتاج مزيداً من المراجعة."
    else:            grade, msg = "راجع المادة 📖", "لا تيأس، كرر الاختبار بعد المراجعة!"

    filled = round(pct / 10)
    bar    = "█" * filled + "░" * (10 - filled)

    if pct == 100:   stars = "⭐⭐⭐⭐⭐"
    elif pct >= 80:  stars = "⭐⭐⭐⭐"
    elif pct >= 60:  stars = "⭐⭐⭐"
    elif pct >= 40:  stars = "⭐⭐"
    else:            stars = "⭐"

    sec_id = sess.get("sec_id")
    kbd_rows = []
    if sec_id:
        kbd_rows.append([InlineKeyboardButton("🔄 أعد الاختبار", callback_data=f"sec_{sec_id}")])
    kbd_rows.append([InlineKeyboardButton("📚 اختر سكشن آخر",    callback_data="menu_sections")])
    kbd_rows.append([InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")])

    await update.callback_query.edit_message_text(
        f"🎉 *انتهى الاختبار!*\n\n"
        f"`{bar}` {pct}%\n\n"
        f"✅ صحيح: *{score}*     ❌ خطأ: *{total - score}*\n"
        f"📊 المجموع: *{score} / {total}*\n\n"
        f"{stars}\n"
        f"التقدير: *{grade}*\n"
        f"_{msg}_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kbd_rows)
    )

# ══════════════════════════════════════════════════════════════════
#  ADMIN /stats
# ══════════════════════════════════════════════════════════════════

async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    st       = db.stats()
    sections = db.get_sections()
    lines    = ["📊 *إحصائيات البوت:*\n",
                f"📦 سكشنات: {st['sections']}",
                f"❓ أسئلة: {st['questions']}\n"]
    for sec in sections:
        lines.append(f"{sec['emoji'] or '📖'} {sec['name']}: {db.count_q(sec['id'])} سؤال")
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
