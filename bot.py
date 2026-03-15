"""
bot.py — كل سكشن له اختبار تقييمي مستقل
"""
import logging, asyncio, os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler,
)
from database import Database

logging.basicConfig(format="%(asctime)s — %(levelname)s — %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
os.makedirs("/data", exist_ok=True)
db = Database("/data/quiz_bot.db")
WAITING_NAME = 1

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════

def question_keyboard(q_obj):
    qid = q_obj["id"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔵  A)  {q_obj['option_a']}", callback_data=f"ans_A_{qid}")],
        [InlineKeyboardButton(f"🟢  B)  {q_obj['option_b']}", callback_data=f"ans_B_{qid}")],
        [InlineKeyboardButton(f"🟡  C)  {q_obj['option_c']}", callback_data=f"ans_C_{qid}")],
        [InlineKeyboardButton(f"🔴  D)  {q_obj['option_d']}", callback_data=f"ans_D_{qid}")],
    ])

def sections_menu(student_id: int) -> InlineKeyboardMarkup:
    """قائمة السكشنات مع حالة كل واحد"""
    sections = db.get_sections()
    rows = []
    for sec in sections:
        cnt      = db.count_q(sec["id"])
        progress = db.get_section_progress(student_id, sec["id"])
        emoji    = sec["emoji"] or "📖"

        if progress and progress["assessed"]:
            pct   = progress["pct"]
            badge = f"✅ {pct}%"
        else:
            badge = "📝 لم يُقيَّم"

        rows.append([InlineKeyboardButton(
            f"{emoji}  {sec['name']}   ┃   {badge}   ┃   {cnt}س",
            callback_data=f"sec_{sec['id']}"
        )])
    return InlineKeyboardMarkup(rows)

async def notify_teacher(ctx, text: str):
    tid = os.environ.get("TEACHER_CHAT_ID","")
    if tid:
        try:
            await ctx.bot.send_message(chat_id=tid, text=text, parse_mode="Markdown")
        except Exception as e:
            logger.warning(f"Teacher notify failed: {e}")

# ══════════════════════════════════════════════════════════════════
#  /start  — التسجيل
# ══════════════════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)

    if student:
        await update.message.reply_text(
            f"👋 *أهلاً {student['full_name']}!*\n\n"
            f"اختر سكشناً للبدء 👇\n\n"
            f"_(✅ = أجريت التقييم   |   📝 = لم يُقيَّم بعد)_",
            parse_mode="Markdown",
            reply_markup=sections_menu(student["id"])
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "🎓 *مرحباً بك!*\n\n"
        "أرسل *اسمك الثلاثي* للتسجيل:",
        parse_mode="Markdown"
    )
    return WAITING_NAME

async def receive_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    uid  = update.effective_user.id

    if db.get_student_by_telegram(uid):
        await update.message.reply_text("أنت مسجّل مسبقاً. اضغط /start")
        return ConversationHandler.END

    if len(name) < 5 or any(c.isdigit() for c in name):
        await update.message.reply_text(
            "⚠️ أدخل اسماً ثلاثياً صحيحاً.\nمثال: `أحمد محمد علي`",
            parse_mode="Markdown"
        )
        return WAITING_NAME

    db.register_new_student(name, uid)
    student = db.get_student_by_telegram(uid)

    await update.message.reply_text(
        f"✅ *تم التسجيل!*  أهلاً *{name}* 🎉\n\n"
        f"اختر سكشناً للبدء 👇\n\n"
        f"_(كل سكشن يبدأ بتقييم قصير لمعرفة مستواك)_",
        parse_mode="Markdown",
        reply_markup=sections_menu(student["id"])
    )
    return ConversationHandler.END

async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء. /start")
    return ConversationHandler.END

# ══════════════════════════════════════════════════════════════════
#  اختيار السكشن — يفحص هل أُجري التقييم أم لا
# ══════════════════════════════════════════════════════════════════

async def cb_section(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)

    if not student:
        await q.edit_message_text("يرجى التسجيل /start")
        return

    sec_id   = int(q.data.split("_")[1])
    section  = db.get_section(sec_id)
    cnt      = db.count_q(sec_id)
    progress = db.get_section_progress(student["id"], sec_id)
    emoji    = section["emoji"] or "📖"

    if not progress or not progress["assessed"]:
        # لم يُقيَّم بعد — عرض زر التقييم
        await q.edit_message_text(
            f"{emoji} *{section['name']}*\n\n"
            f"📝 لم تُجرِ التقييم لهذا السكشن بعد.\n\n"
            f"ابدأ بالتقييم القصير أولاً — سيساعد الأستاذ\n"
            f"على معرفة مستواك الحالي في هذا الموضوع.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"🎯 ابدأ التقييم ({cnt} سؤال)", callback_data=f"assess_{sec_id}")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_sections")],
            ])
        )
    else:
        # أُجري التقييم — عرض النتيجة + خيارات التدريب
        pct   = progress["pct"]
        score = progress["score"]
        total = progress["total_q"]
        bar   = "█" * round(pct/10) + "░" * (10 - round(pct/10))

        await q.edit_message_text(
            f"{emoji} *{section['name']}*\n\n"
            f"📊 نتيجتك التقييمية:\n"
            f"`{bar}` {pct}%  ({score}/{total})\n\n"
            f"اختر نوع التدريب:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚡️ 10 أسئلة عشوائية", callback_data=f"train_{sec_id}_10")],
                [InlineKeyboardButton("📋 كل الأسئلة",        callback_data=f"train_{sec_id}_all")],
                [InlineKeyboardButton("🔄 أعد التقييم",        callback_data=f"assess_{sec_id}")],
                [InlineKeyboardButton("🔙 رجوع",               callback_data="back_sections")],
            ])
        )

async def cb_back_sections(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)
    if not student:
        await q.edit_message_text("يرجى التسجيل /start")
        return
    await q.edit_message_text(
        f"📚 *السكشنات — {student['full_name']}*\n\n"
        f"_(✅ = أجريت التقييم   |   📝 = لم يُقيَّم بعد)_",
        parse_mode="Markdown",
        reply_markup=sections_menu(student["id"])
    )

# ══════════════════════════════════════════════════════════════════
#  بدء تقييم سكشن معين
# ══════════════════════════════════════════════════════════════════

async def cb_assess_section(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)

    if not student:
        await q.edit_message_text("يرجى التسجيل /start")
        return

    sec_id   = int(q.data.split("_")[1])
    section  = db.get_section(sec_id)
    questions = db.get_questions(sec_id)   # كل أسئلة هذا السكشن

    if not questions:
        await q.edit_message_text("⚠️ لا توجد أسئلة في هذا السكشن.")
        return

    questions = list(questions)
    random.shuffle(questions)
    db.save_session(uid, "assessment", sec_id, questions, 0, 0, len(questions))

    emoji = section["emoji"] or "📖"
    await q.edit_message_text(
        f"{emoji} *تقييم: {section['name']}*\n\n"
        f"📝 {len(questions)} سؤال\n\n"
        f"أجب بصدق — النتيجة تُحفظ لهذا السكشن فقط 💪",
        parse_mode="Markdown"
    )
    await asyncio.sleep(0.6)
    await _send_question(update, ctx)

# ══════════════════════════════════════════════════════════════════
#  بدء تدريب سكشن معين
# ══════════════════════════════════════════════════════════════════

async def cb_train_section(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)

    if not student:
        await q.edit_message_text("يرجى التسجيل /start")
        return

    parts  = q.data.split("_")   # train_<sec_id>_<limit>
    sec_id = int(parts[1])
    limit  = None if parts[2] == "all" else int(parts[2])

    questions = db.get_questions(sec_id, limit)
    if not questions:
        await q.edit_message_text("⚠️ لا توجد أسئلة.")
        return

    questions = list(questions)
    random.shuffle(questions)
    db.save_session(uid, "training", sec_id, questions, 0, 0, len(questions))

    section = db.get_section(sec_id)
    emoji   = section["emoji"] or "📖"
    await q.edit_message_text(
        f"{emoji} *{section['name']}*\n\n"
        f"🎯 {len(questions)} سؤال — ابدأ! 🚀",
        parse_mode="Markdown"
    )
    await asyncio.sleep(0.6)
    await _send_question(update, ctx)

# ══════════════════════════════════════════════════════════════════
#  إرسال السؤال
# ══════════════════════════════════════════════════════════════════

async def _send_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    sess = db.get_session(uid)

    if not sess:
        try:
            await update.callback_query.edit_message_text("⚠️ انتهت الجلسة. /start")
        except Exception:
            pass
        return

    idx   = sess["idx"]
    total = sess["total"]

    if idx >= total:
        if sess["mode"] == "assessment":
            await _finish_assessment(update, ctx, sess)
        else:
            await _finish_training(update, ctx, sess)
        return

    q_obj  = sess["qs"][idx]
    filled = round((idx / total) * 10) if total else 0
    bar    = "█" * filled + "░" * (10 - filled)
    pct    = round((idx / total) * 100)
    icon   = "🎯" if sess["mode"] == "assessment" else "📚"

    text = (
        f"{icon}  *سؤال {idx+1} من {total}*\n"
        f"`{bar}` {pct}%\n\n"
        f"❓ *{q_obj['question_text']}*"
    )

    try:
        await update.callback_query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=question_keyboard(q_obj)
        )
    except Exception as e:
        logger.warning(f"edit failed: {e}")
        try:
            await update.effective_chat.send_message(
                text, parse_mode="Markdown", reply_markup=question_keyboard(q_obj)
            )
        except Exception as e2:
            logger.error(f"send failed: {e2}")

# ══════════════════════════════════════════════════════════════════
#  الإجابة
# ══════════════════════════════════════════════════════════════════

async def cb_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q   = update.callback_query
    await q.answer()
    uid = update.effective_user.id

    sess = db.get_session(uid)
    if not sess:
        await q.edit_message_text(
            "⚠️ انتهت الجلسة. /start",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 رجوع", callback_data="back_sections")]
            ])
        )
        return

    parts    = q.data.split("_")
    user_ans = parts[1].upper()
    idx      = sess["idx"]
    q_obj    = sess["qs"][idx]
    correct  = q_obj["correct_answer"].upper()
    is_right = (user_ans == correct)

    new_score = sess["score"] + (1 if is_right else 0)
    new_idx   = idx + 1
    db.update_session(uid, new_idx, new_score)

    color = {"A":"🔵","B":"🟢","C":"🟡","D":"🔴"}
    opt   = {
        "A": q_obj["option_a"], "B": q_obj["option_b"],
        "C": q_obj["option_c"], "D": q_obj["option_d"],
    }

    if is_right:
        result = f"✅ *صحيح!*\n{color[correct]}  {correct})  {opt[correct]}"
    else:
        result = (
            f"❌ *خطأ!*\n"
            f"اخترت: {color[user_ans]}  {user_ans})  {opt[user_ans]}\n\n"
            f"✅ الصحيحة: {color[correct]}  {correct})  {opt[correct]}"
        )

    exp      = q_obj.get("explanation") or ""
    exp_line = f"\n\n💡 _{exp}_" if exp else ""
    remaining = sess["total"] - new_idx
    btn = (f"التالي ←  ({new_idx+1}/{sess['total']})"
           if remaining > 0 else "عرض النتيجة 🏁")

    await q.edit_message_text(
        f"❓ *{q_obj['question_text']}*\n\n{'─'*18}\n\n{result}{exp_line}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(btn, callback_data="next_q")]
        ])
    )

async def cb_next_q(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q   = update.callback_query
    await q.answer()
    uid = update.effective_user.id
    sess = db.get_session(uid)
    if not sess:
        await q.edit_message_text("⚠️ انتهت الجلسة. /start")
        return
    if sess["idx"] >= sess["total"]:
        if sess["mode"] == "assessment":
            await _finish_assessment(update, ctx, sess)
        else:
            await _finish_training(update, ctx, sess)
    else:
        await _send_question(update, ctx)

# ══════════════════════════════════════════════════════════════════
#  نهاية التقييم — يُحفظ لهذا السكشن فقط
# ══════════════════════════════════════════════════════════════════

async def _finish_assessment(update: Update, ctx: ContextTypes.DEFAULT_TYPE, sess: dict):
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)
    sec_id  = sess["sec_id"]
    db.delete_session(uid)

    score   = sess["score"]
    total   = sess["total"]
    pct     = round((score / total) * 100) if total else 0

    # ← حفظ لهذا السكشن فقط — لا يمس بقية السكشنات
    db.save_section_assessment(student["id"], sec_id, score, total)

    section = db.get_section(sec_id)
    emoji   = section["emoji"] or "📖"

    if pct >= 90:   grade, icon = "ممتاز 🏆",       "🌟"
    elif pct >= 75: grade, icon = "جيد جداً 🥈",    "✅"
    elif pct >= 60: grade, icon = "جيد 🥉",          "👍"
    elif pct >= 50: grade, icon = "مقبول 📘",        "⚠️"
    else:           grade, icon = "يحتاج مراجعة 📖", "❗"

    filled = round(pct / 10)
    bar    = "█" * filled + "░" * (10 - filled)
    stars  = "⭐" * max(1, round(pct / 20))

    # إرسال للأستاذ
    await notify_teacher(ctx,
        f"📋 *نتيجة تقييم*\n\n"
        f"👤 *{student['full_name']}*\n"
        f"{emoji} السكشن: *{section['name']}*\n"
        f"📊 *{score}/{total}* ({pct}%)\n"
        f"التقدير: {grade}"
    )

    await update.callback_query.edit_message_text(
        f"{icon} *انتهى تقييم: {section['name']}*\n\n"
        f"`{bar}` {pct}%\n\n"
        f"✅ صحيح: *{score}*   ❌ خطأ: *{total-score}*\n"
        f"📊 المجموع: *{score}/{total}*\n\n"
        f"{stars}  *{grade}*\n\n"
        f"تم الحفظ ✅ — يمكنك الآن التدريب أو اختيار سكشن آخر 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡️ ابدأ التدريب الآن",   callback_data=f"train_{sec_id}_10")],
            [InlineKeyboardButton("📚 اختر سكشن آخر",        callback_data="back_sections")],
        ])
    )

# ══════════════════════════════════════════════════════════════════
#  نهاية التدريب
# ══════════════════════════════════════════════════════════════════

async def _finish_training(update: Update, ctx: ContextTypes.DEFAULT_TYPE, sess: dict):
    uid   = update.effective_user.id
    db.delete_session(uid)
    score = sess["score"]
    total = sess["total"]
    pct   = round((score/total)*100) if total else 0

    if pct==100:   grade = "ممتاز 🏆"
    elif pct>=90:  grade = "ممتاز 🥇"
    elif pct>=75:  grade = "جيد جداً 🥈"
    elif pct>=60:  grade = "جيد 🥉"
    else:          grade = "راجع المادة 📖"

    filled = round(pct/10)
    bar    = "█"*filled + "░"*(10-filled)
    stars  = "⭐"*max(1,round(pct/20))
    sec_id = sess.get("sec_id")
    rows   = []
    if sec_id:
        rows.append([InlineKeyboardButton("🔄 أعد التدريب",   callback_data=f"train_{sec_id}_10")])
    rows.append([InlineKeyboardButton("📚 سكشن آخر",          callback_data="back_sections")])

    await update.callback_query.edit_message_text(
        f"🎉 *انتهى التدريب!*\n\n"
        f"`{bar}` {pct}%\n\n"
        f"✅ صحيح: *{score}*   ❌ خطأ: *{total-score}*\n"
        f"📊 *{score}/{total}*\n\n"
        f"{stars}  *{grade}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(rows)
    )

# ══════════════════════════════════════════════════════════════════
#  /stats
# ══════════════════════════════════════════════════════════════════

async def cmd_myid(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid      = update.effective_user.id
    username = update.effective_user.username or "لا يوجد"
    name     = update.effective_user.full_name or ""
    await update.message.reply_text(
        f"🆔 *معلوماتك:*\n\n"
        f"الـ ID: `{uid}`\n"
        f"الاسم: {name}\n"
        f"اليوزرنيم: @{username}\n\n"
        f"📋 انسخ الـ ID وضعه في Railway كـ:\n"
        f"`TEACHER_CHAT_ID` = `{uid}`",
        parse_mode="Markdown"
    )

async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    st  = db.stats()
    url = os.environ.get("RAILWAY_PUBLIC_DOMAIN","")
    url = f"https://{url}" if url else "—"
    await update.message.reply_text(
        f"📊 *إحصائيات:*\n\n"
        f"👥 طلاب: {st['students']}\n"
        f"📦 سكشنات: {st['sections']}\n"
        f"❓ أسئلة: {st['questions']}\n\n"
        f"🌐 الداشبورد: {url}",
        parse_mode="Markdown"
    )

async def guard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not db.get_student_by_telegram(update.effective_user.id):
        await update.message.reply_text("يرجى التسجيل /start")

# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    TOKEN = os.environ.get("BOT_TOKEN","PUT_YOUR_TOKEN_HERE")
    app   = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={WAITING_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)
        ]},
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("myid",  cmd_myid))

    # السكشنات
    app.add_handler(CallbackQueryHandler(cb_section,        pattern=r"^sec_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_back_sections,  pattern="^back_sections$"))

    # التقييم والتدريب
    app.add_handler(CallbackQueryHandler(cb_assess_section, pattern=r"^assess_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_train_section,  pattern=r"^train_\d+_(all|\d+)$"))

    # الأسئلة
    app.add_handler(CallbackQueryHandler(cb_answer,  pattern=r"^ans_[AaBbCcDd]_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_next_q,  pattern="^next_q$"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guard))

    logger.info("Bot started ✅")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
