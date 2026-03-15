"""
bot.py — تسجيل حر (أي طالب يكتب اسمه يُحفظ مباشرة)
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

db           = Database("quiz_bot.db")
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

def training_menu(sections):
    rows = []
    for sec in sections:
        cnt = db.count_q(sec["id"])
        rows.append([InlineKeyboardButton(
            f"{sec['emoji'] or '📖'}  {sec['name']}   ┃   {cnt} سؤال",
            callback_data=f"sec_{sec['id']}"
        )])
    return InlineKeyboardMarkup(rows)

async def notify_teacher(ctx, text: str):
    tid = os.environ.get("TEACHER_CHAT_ID", "")
    if tid:
        try:
            await ctx.bot.send_message(chat_id=tid, text=text, parse_mode="Markdown")
        except Exception as e:
            logger.warning(f"Teacher notify failed: {e}")

# ══════════════════════════════════════════════════════════════════
#  /start
# ══════════════════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)

    # طالب مسجّل وأنهى الاختبار → يدخل للتدريب مباشرة
    if student and student["assessed"]:
        sections = db.get_sections()
        await update.message.reply_text(
            f"👋 *أهلاً {student['full_name']}!*\n\n"
            f"نتيجتك السابقة: *{student['score']}/{student['total_q']}* "
            f"({student['pct']}%)\n\n"
            f"اختر سكشناً للتدريب 👇",
            parse_mode="Markdown",
            reply_markup=training_menu(sections)
        )
        return ConversationHandler.END

    # طالب مسجّل لكن لم ينهِ الاختبار بعد
    if student and not student["assessed"]:
        db.delete_session(uid)
        await update.message.reply_text(
            f"👋 *أهلاً {student['full_name']}!*\n\n"
            f"⚠️ لم تُنهِ الاختبار التقييمي بعد.\n"
            f"يجب إكماله أولاً قبل الوصول للتدريب.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 ابدأ الاختبار", callback_data="begin_assessment")]
            ])
        )
        return ConversationHandler.END

    # مستخدم جديد — اطلب الاسم
    await update.message.reply_text(
        "🎓 *مرحباً بك في بوت الاختبارات!*\n\n"
        "أرسل *اسمك الثلاثي* للتسجيل:\n\n"
        "مثال: `أحمد محمد علي`",
        parse_mode="Markdown"
    )
    return WAITING_NAME

async def receive_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    uid  = update.effective_user.id

    # تأكد مش مسجل بنفس الـ ID
    if db.get_student_by_telegram(uid):
        await update.message.reply_text("أنت مسجّل مسبقاً. اضغط /start")
        return ConversationHandler.END

    # التحقق من الاسم — لا يقبل أرقام أو رموز فقط
    if len(name) < 5 or any(c.isdigit() for c in name):
        await update.message.reply_text(
            "⚠️ يرجى إدخال اسم ثلاثي صحيح.\n\n"
            "مثال: `أحمد محمد علي`",
            parse_mode="Markdown"
        )
        return WAITING_NAME

    # ← حفظ الاسم مع الـ telegram_id مباشرة
    db.register_new_student(name, uid)

    await update.message.reply_text(
        f"✅ *تم تسجيلك بنجاح!*\n\n"
        f"أهلاً *{name}* 🎉\n\n"
        f"ستبدأ الآن بـ *الاختبار التقييمي الكامل*.\n"
        f"📌 لا يمكن تخطيه — يساعد الأستاذ على معرفة مستواك.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 ابدأ الاختبار الآن", callback_data="begin_assessment")]
        ])
    )
    return ConversationHandler.END

async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء. اضغط /start للبدء.")
    return ConversationHandler.END

# ══════════════════════════════════════════════════════════════════
#  الاختبار التقييمي الكامل
# ══════════════════════════════════════════════════════════════════

async def cb_begin_assessment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q   = update.callback_query
    await q.answer()
    uid = update.effective_user.id

    student = db.get_student_by_telegram(uid)
    if not student:
        await q.edit_message_text("يرجى التسجيل أولاً /start")
        return

    if student["assessed"]:
        sections = db.get_sections()
        await q.edit_message_text(
            "✅ أجريت الاختبار مسبقاً. اختر سكشناً للتدريب:",
            reply_markup=training_menu(sections)
        )
        return

    questions = db.get_all_questions_shuffled()
    if not questions:
        await q.edit_message_text("⚠️ لا توجد أسئلة بعد. تواصل مع الأستاذ.")
        return

    db.save_session(uid, "assessment", None, questions, 0, 0, len(questions))

    await q.edit_message_text(
        f"🎯 *الاختبار التقييمي الكامل*\n\n"
        f"📝 عدد الأسئلة: *{len(questions)}*\n\n"
        f"أجب بصدق — النتيجة تساعد الأستاذ على معرفة مستواك 💪",
        parse_mode="Markdown"
    )
    await asyncio.sleep(0.8)
    await _send_question(update, ctx)

# ══════════════════════════════════════════════════════════════════
#  إرسال السؤال
# ══════════════════════════════════════════════════════════════════

async def _send_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    sess = db.get_session(uid)

    if not sess:
        try:
            await update.callback_query.edit_message_text(
                "⚠️ انتهت الجلسة. اضغط /start"
            )
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
            "⚠️ انتهت الجلسة. اضغط /start",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 ابدأ", callback_data="begin_assessment")]
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
    btn = (f"التالي ←  (سؤال {new_idx+1}/{sess['total']})"
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
#  نهاية الاختبار التقييمي
# ══════════════════════════════════════════════════════════════════

async def _finish_assessment(update: Update, ctx: ContextTypes.DEFAULT_TYPE, sess: dict):
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)
    db.delete_session(uid)

    score = sess["score"]
    total = sess["total"]
    pct   = round((score / total) * 100) if total else 0

    db.save_assessment_result(student["id"], score, total)

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
        f"📋 *نتيجة اختبار جديدة*\n\n"
        f"👤 *{student['full_name']}*\n"
        f"🆔 @{update.effective_user.username or 'لا يوجد'}\n"
        f"📊 *{score}/{total}* ({pct}%)\n"
        f"التقدير: {grade}"
    )

    sections = db.get_sections()
    await update.callback_query.edit_message_text(
        f"{icon} *انتهى الاختبار التقييمي!*\n\n"
        f"`{bar}` {pct}%\n\n"
        f"✅ صحيح: *{score}*\n"
        f"❌ خطأ: *{total - score}*\n"
        f"📊 المجموع: *{score}/{total}*\n\n"
        f"{stars}\n"
        f"التقدير: *{grade}*\n\n"
        f"{'─'*20}\n\n"
        f"🎉 تم حفظ نتيجتك!\n"
        f"يمكنك الآن التدريب على أي سكشن 👇",
        parse_mode="Markdown",
        reply_markup=training_menu(sections)
    )

# ══════════════════════════════════════════════════════════════════
#  السكشنات والتدريب
# ══════════════════════════════════════════════════════════════════

async def cb_section_detail(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)

    if not student or not student["assessed"]:
        await q.answer("⚠️ أكمل الاختبار التقييمي أولاً!", show_alert=True)
        return

    sec_id  = int(q.data.split("_")[1])
    section = db.get_section(sec_id)
    cnt     = db.count_q(sec_id)

    await q.edit_message_text(
        f"{section['emoji'] or '📖'} *{section['name']}*\n\n"
        f"📝 {cnt} سؤال متاح\n\nاختر نوع التدريب:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡️ 10 أسئلة عشوائية", callback_data=f"start_{sec_id}_10")],
            [InlineKeyboardButton("📋 كل الأسئلة",        callback_data=f"start_{sec_id}_all")],
            [InlineKeyboardButton("🔙 رجوع",              callback_data="back_sections")],
        ])
    )

async def cb_start_training(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)

    if not student or not student["assessed"]:
        await q.answer("⚠️ أكمل الاختبار التقييمي أولاً!", show_alert=True)
        return

    parts  = q.data.split("_")
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
    await q.edit_message_text(
        f"{section['emoji'] or '📖'} *{section['name']}*\n\n"
        f"🎯 {len(questions)} سؤال — ابدأ! 🚀",
        parse_mode="Markdown"
    )
    await asyncio.sleep(0.6)
    await _send_question(update, ctx)

async def cb_back_sections(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q       = update.callback_query
    await q.answer()
    uid     = update.effective_user.id
    student = db.get_student_by_telegram(uid)
    sections = db.get_sections()
    name = student["full_name"] if student else ""
    await q.edit_message_text(
        f"📚 *اختر السكشن {name}:*",
        parse_mode="Markdown",
        reply_markup=training_menu(sections)
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
        rows.append([InlineKeyboardButton("🔄 أعد هذا السكشن", callback_data=f"sec_{sec_id}")])
    rows.append([InlineKeyboardButton("📚 سكشن آخر", callback_data="back_sections")])

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
#  ADMIN /stats
# ══════════════════════════════════════════════════════════════════

async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    st  = db.stats()
    url = os.environ.get("RAILWAY_PUBLIC_DOMAIN","")
    url = f"https://{url}" if url else "dashboard.py"
    await update.message.reply_text(
        f"📊 *إحصائيات:*\n\n"
        f"👥 طلاب مسجّلون: {st['students']}\n"
        f"✅ أجروا التقييم: {st['assessed']}\n"
        f"📦 سكشنات: {st['sections']}\n"
        f"❓ أسئلة: {st['questions']}\n\n"
        f"🌐 الداشبورد:\n{url}",
        parse_mode="Markdown"
    )

async def guard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not db.get_student_by_telegram(uid):
        await update.message.reply_text(
            "يرجى التسجيل أولاً عبر /start"
        )

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

    app.add_handler(CallbackQueryHandler(cb_begin_assessment, pattern="^begin_assessment$"))
    app.add_handler(CallbackQueryHandler(cb_section_detail,   pattern=r"^sec_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_start_training,   pattern=r"^start_\d+_(all|\d+)$"))
    app.add_handler(CallbackQueryHandler(cb_answer,           pattern=r"^ans_[AaBbCcDd]_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_next_q,           pattern="^next_q$"))
    app.add_handler(CallbackQueryHandler(cb_back_sections,    pattern="^back_sections$"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guard))

    logger.info("Bot started ✅")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
