"""
Plant Classification Quiz Bot
"""

import asyncio
import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database import Database

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

os.makedirs("/data", exist_ok=True)
db = Database("/data/quiz_bot.db")

WAITING_NAME = 1
BOT_NAME = "بوت تصنيف النباتات"
DEFAULT_EMOJI = "🌿"


def question_keyboard(q_obj):
    question_id = q_obj["id"]
    options = [
        ("A", q_obj["option_a"]),
        ("B", q_obj["option_b"]),
        ("C", q_obj["option_c"]),
        ("D", q_obj["option_d"]),
    ]
    rows = [
        [InlineKeyboardButton(f"{label}) {text}", callback_data=f"ans_{label}_{question_id}")]
        for label, text in options
    ]
    return InlineKeyboardMarkup(rows)


def sections_menu(student_id: int):
    sections = db.get_sections()
    rows = []

    for section in sections:
        count = db.count_q(section["id"])
        progress = db.get_section_progress(student_id, section["id"])
        emoji = section["emoji"] or DEFAULT_EMOJI
        badge = (
            f"✅ {progress['pct']}%"
            if progress and progress["assessed"]
            else "📝 غير مقيم"
        )
        rows.append(
            [
                InlineKeyboardButton(
                    f"{emoji} {section['name']} | {badge} | {count} سؤال",
                    callback_data=f"sec_{section['id']}",
                )
            ]
        )

    if not rows:
        rows.append([InlineKeyboardButton("لا توجد أقسام متاحة حالياً", callback_data="blocked")])

    return InlineKeyboardMarkup(rows)


async def notify_teacher(ctx, text: str):
    ids_text = os.environ.get("TEACHER_CHAT_ID", "")
    if not ids_text:
        return

    for raw_id in ids_text.split(","):
        teacher_id = raw_id.strip()
        if not teacher_id:
            continue
        try:
            await ctx.bot.send_message(chat_id=teacher_id, text=text)
        except Exception as exc:
            logger.warning("Teacher notification failed for %s: %s", teacher_id, exc)


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)

    if student:
        await update.message.reply_text(
            f"أهلاً {student['full_name']} في {BOT_NAME}.\n\n"
            "اختر القسم الذي تريد مراجعته، والأسئلة ستظهر بالترتيب من الأول إلى الأخير.\n"
            "✅ يعني تم تقييم القسم سابقاً، و📝 يعني لم يتم تقييمه بعد.",
            reply_markup=sections_menu(student["id"]),
        )
        return ConversationHandler.END

    await update.message.reply_text(
        f"مرحباً بك في {BOT_NAME}.\n\n"
        "أرسل اسمك الثلاثي للتسجيل ثم سنعرض لك أقسام تصنيف النبات بشكل مرتب.",
    )
    return WAITING_NAME


async def receive_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    user_id = update.effective_user.id

    if db.get_student_by_telegram(user_id):
        await update.message.reply_text("أنت مسجل مسبقاً. أرسل /start للعودة.")
        return ConversationHandler.END

    if len(name) < 5 or any(char.isdigit() for char in name):
        await update.message.reply_text(
            "أدخل الاسم الثلاثي بشكل صحيح.\nمثال: أحمد محمد علي",
        )
        return WAITING_NAME

    db.register_new_student(name, user_id)
    student = db.get_student_by_telegram(user_id)
    await update.message.reply_text(
        f"تم التسجيل بنجاح يا {name}.\n\n"
        "اختر الآن القسم الذي تريد البدء به.",
        reply_markup=sections_menu(student["id"]),
    )
    return ConversationHandler.END


async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء. أرسل /start للعودة.")
    return ConversationHandler.END


async def cb_section(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)
    if not student:
        await query.edit_message_text("يرجى التسجيل أولاً عبر /start")
        return

    section_id = int(query.data.split("_")[1])
    section = db.get_section(section_id)
    count = db.count_q(section_id)
    progress = db.get_section_progress(student["id"], section_id)
    emoji = section["emoji"] or DEFAULT_EMOJI

    if not progress or not progress["assessed"]:
        await query.edit_message_text(
            f"{emoji} {section['name']}\n\n"
            f"عدد أسئلة هذا القسم: {count}\n"
            "التقييم يعرض الأسئلة بالترتيب الثابت بدون عشوائية.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"ابدأ التقييم المرتب ({count} سؤال)",
                            callback_data=f"assess_{section_id}",
                        )
                    ],
                    [InlineKeyboardButton("رجوع", callback_data="back_sections")],
                ]
            ),
        )
        return

    percent = progress["pct"]
    score = progress["score"]
    total = progress["total_q"]
    filled = round(percent / 10)
    bar = "█" * filled + "░" * (10 - filled)
    can_reassess, days_left = db.can_reassess(student["id"], section_id)

    reassess_button = (
        InlineKeyboardButton("إعادة التقييم", callback_data=f"reassess_{section_id}")
        if can_reassess
        else InlineKeyboardButton(
            f"إعادة التقييم بعد {days_left} يوم",
            callback_data="blocked",
        )
    )

    await query.edit_message_text(
        f"{emoji} {section['name']}\n\n"
        f"نتيجتك السابقة: {score}/{total} ({percent}%)\n"
        f"`{bar}`\n\n"
        "اختر طريقة المتابعة:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "مراجعة أول 10 أسئلة بالترتيب",
                        callback_data=f"train_{section_id}_10",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "مراجعة كل الأسئلة بالترتيب",
                        callback_data=f"train_{section_id}_all",
                    )
                ],
                [reassess_button],
                [InlineKeyboardButton("رجوع", callback_data="back_sections")],
            ]
        ),
    )


async def cb_back_sections(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)
    if not student:
        await query.edit_message_text("يرجى التسجيل أولاً عبر /start")
        return

    await query.edit_message_text(
        f"اختر القسم المناسب يا {student['full_name']}.",
        reply_markup=sections_menu(student["id"]),
    )


async def cb_blocked(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer(
        "لا يمكن تنفيذ هذه الخطوة الآن.",
        show_alert=True,
    )


async def cb_assess_section(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)
    if not student:
        await query.edit_message_text("يرجى التسجيل أولاً عبر /start")
        return

    section_id = int(query.data.split("_")[1])
    section = db.get_section(section_id)
    questions = db.get_questions_ordered(section_id)
    db.save_session(user_id, "assessment", section_id, questions, 0, 0, len(questions))

    await query.edit_message_text(
        f"{section['emoji'] or DEFAULT_EMOJI} تقييم: {section['name']}\n\n"
        f"عدد الأسئلة: {len(questions)}\n"
        "سيتم عرض الأسئلة بالتسلسل من الأول إلى الأخير.",
    )
    await asyncio.sleep(0.5)
    await _send_question(update, ctx)


async def cb_reassess_section(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)
    if not student:
        await query.edit_message_text("يرجى التسجيل أولاً عبر /start")
        return

    section_id = int(query.data.split("_")[1])
    can_reassess, days_left = db.can_reassess(student["id"], section_id)
    if not can_reassess:
        await query.answer(
            f"يمكنك إعادة التقييم بعد {days_left} يوم.",
            show_alert=True,
        )
        return

    section = db.get_section(section_id)
    questions = db.get_questions_ordered(section_id)
    db.save_session(user_id, "assessment", section_id, questions, 0, 0, len(questions))

    await query.edit_message_text(
        f"{section['emoji'] or DEFAULT_EMOJI} إعادة تقييم: {section['name']}\n\n"
        f"عدد الأسئلة: {len(questions)}\n"
        "الأسئلة ستظهر بنفس ترتيبها المعتمد.",
    )
    await asyncio.sleep(0.5)
    await _send_question(update, ctx)


async def cb_train_section(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)
    if not student:
        await query.edit_message_text("يرجى التسجيل أولاً عبر /start")
        return

    _, section_id_text, limit_text = query.data.split("_")
    section_id = int(section_id_text)
    limit = None if limit_text == "all" else int(limit_text)
    questions = db.get_questions_ordered(section_id, limit)
    db.save_session(user_id, "training", section_id, questions, 0, 0, len(questions))

    section = db.get_section(section_id)
    await query.edit_message_text(
        f"{section['emoji'] or DEFAULT_EMOJI} {section['name']}\n\n"
        f"تم تجهيز {len(questions)} سؤال للمراجعة المرتبة.",
    )
    await asyncio.sleep(0.5)
    await _send_question(update, ctx)


async def _send_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = db.get_session(user_id)
    if not session:
        try:
            await update.callback_query.edit_message_text("انتهت الجلسة. أرسل /start للعودة.")
        except Exception:
            pass
        return

    index = session["idx"]
    total = session["total"]

    if index >= total:
        if session["mode"] == "assessment":
            await _finish_assessment(update, ctx, session)
        else:
            await _finish_training(update, ctx, session)
        return

    question = session["qs"][index]
    filled = round((index / total) * 10) if total else 0
    bar = "█" * filled + "░" * (10 - filled)
    percent = round((index / total) * 100) if total else 0
    mode_label = "التقييم" if session["mode"] == "assessment" else "المراجعة"

    text = (
        f"*{mode_label}* - السؤال {index + 1} من {total}\n"
        f"`{bar}` {percent}%\n\n"
        f"*{question['question_text']}*"
    )

    try:
        await update.callback_query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=question_keyboard(question),
        )
    except Exception as exc:
        logger.warning("Message edit failed, sending a new one instead: %s", exc)
        try:
            await update.effective_chat.send_message(
                text,
                parse_mode="Markdown",
                reply_markup=question_keyboard(question),
            )
        except Exception as inner_exc:
            logger.error("Sending question failed: %s", inner_exc)


async def cb_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    session = db.get_session(user_id)
    if not session:
        await query.edit_message_text(
            "انتهت الجلسة. أرسل /start للعودة.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("العودة للأقسام", callback_data="back_sections")]]
            ),
        )
        return

    user_answer = query.data.split("_")[1].upper()
    index = session["idx"]
    question = session["qs"][index]
    correct_answer = question["correct_answer"].upper()
    is_correct = user_answer == correct_answer

    new_score = session["score"] + (1 if is_correct else 0)
    new_index = index + 1
    db.update_session(user_id, new_index, new_score)

    options = {
        "A": question["option_a"],
        "B": question["option_b"],
        "C": question["option_c"],
        "D": question["option_d"],
    }

    if is_correct:
        result = f"✅ إجابة صحيحة\n{correct_answer}) {options[correct_answer]}"
    else:
        result = (
            "❌ إجابة غير صحيحة\n"
            f"إجابتك: {user_answer}) {options[user_answer]}\n\n"
            f"الصحيح: {correct_answer}) {options[correct_answer]}"
        )

    explanation = question.get("explanation", "") or ""
    explanation_line = f"\n\nالشرح: {explanation}" if explanation else ""
    remaining = session["total"] - new_index
    next_label = (
        f"التالي ({new_index + 1}/{session['total']})"
        if remaining > 0
        else "عرض النتيجة"
    )

    await query.edit_message_text(
        f"*{question['question_text']}*\n\n{result}{explanation_line}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(next_label, callback_data="next_q")]]
        ),
    )


async def cb_next_q(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    session = db.get_session(user_id)
    if not session:
        await query.edit_message_text("انتهت الجلسة. أرسل /start للعودة.")
        return

    if session["idx"] >= session["total"]:
        if session["mode"] == "assessment":
            await _finish_assessment(update, ctx, session)
        else:
            await _finish_training(update, ctx, session)
        return

    await _send_question(update, ctx)


def grade_from_percent(percent: int):
    if percent >= 90:
        return "ممتاز", "🏆"
    if percent >= 75:
        return "جيد جداً", "🌟"
    if percent >= 60:
        return "جيد", "✅"
    if percent >= 50:
        return "مقبول", "📘"
    return "يحتاج مراجعة", "📚"


async def _finish_assessment(update: Update, ctx: ContextTypes.DEFAULT_TYPE, session: dict):
    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)
    section_id = session["sec_id"]
    db.delete_session(user_id)

    score = session["score"]
    total = session["total"]
    percent = round((score / total) * 100) if total else 0
    db.save_section_assessment(student["id"], section_id, score, total)

    section = db.get_section(section_id)
    emoji = section["emoji"] or DEFAULT_EMOJI
    grade, icon = grade_from_percent(percent)
    filled = round(percent / 10)
    bar = "█" * filled + "░" * (10 - filled)

    username = update.effective_user.username
    username_text = f"@{username}" if username else "لا يوجد"
    await notify_teacher(
        ctx,
        (
            f"نتيجة تقييم جديدة - {BOT_NAME}\n"
            f"الاسم: {student['full_name']}\n"
            f"الحساب: {username_text}\n"
            f"القسم: {section['name']}\n"
            f"النتيجة: {score}/{total} ({percent}%)\n"
            f"التقدير: {grade}"
        ),
    )

    await update.callback_query.edit_message_text(
        f"{icon} انتهى تقييم {section['name']}\n\n"
        f"`{bar}` {percent}%\n"
        f"الصحيح: {score}\n"
        f"الخطأ: {total - score}\n"
        f"التقدير: {grade}\n\n"
        "يمكنك الآن مراجعة القسم بالترتيب أو العودة للأقسام.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "مراجعة أول 10 أسئلة",
                        callback_data=f"train_{section_id}_10",
                    )
                ],
                [InlineKeyboardButton("العودة للأقسام", callback_data="back_sections")],
            ]
        ),
    )


async def _finish_training(update: Update, ctx: ContextTypes.DEFAULT_TYPE, session: dict):
    user_id = update.effective_user.id
    db.delete_session(user_id)

    score = session["score"]
    total = session["total"]
    percent = round((score / total) * 100) if total else 0
    grade, icon = grade_from_percent(percent)
    filled = round(percent / 10)
    bar = "█" * filled + "░" * (10 - filled)

    section_id = session.get("sec_id")
    rows = []
    if section_id:
        rows.append(
            [InlineKeyboardButton("أعد المراجعة", callback_data=f"train_{section_id}_10")]
        )
    rows.append([InlineKeyboardButton("العودة للأقسام", callback_data="back_sections")])

    await update.callback_query.edit_message_text(
        f"{icon} انتهت المراجعة\n\n"
        f"`{bar}` {percent}%\n"
        f"الصحيح: {score}\n"
        f"الخطأ: {total - score}\n"
        f"التقدير: {grade}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(rows),
    )


async def cmd_myid(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "لا يوجد"
    await update.message.reply_text(
        f"معلوماتك:\n\n"
        f"ID: {user_id}\n"
        f"اسم المستخدم: @{username}\n\n"
        f"أضف هذا الرقم في Railway داخل المتغير TEACHER_CHAT_ID.",
    )


async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    stats = db.stats()
    domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
    dashboard_url = f"https://{domain}" if domain else "غير متوفر"
    await update.message.reply_text(
        f"إحصائيات {BOT_NAME}:\n\n"
        f"الطلاب: {stats['students']}\n"
        f"الأقسام: {stats['sections']}\n"
        f"الأسئلة: {stats['questions']}\n\n"
        f"رابط اللوحة: {dashboard_url}",
    )


async def guard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not db.get_student_by_telegram(update.effective_user.id):
        await update.message.reply_text("يرجى التسجيل أولاً عبر /start")


def main():
    token = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
    app = Application.builder().token(token).build()

    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            WAITING_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)
            ]
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
    )

    app.add_handler(conversation)
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("myid", cmd_myid))
    app.add_handler(CallbackQueryHandler(cb_section, pattern=r"^sec_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_back_sections, pattern=r"^back_sections$"))
    app.add_handler(CallbackQueryHandler(cb_assess_section, pattern=r"^assess_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_reassess_section, pattern=r"^reassess_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_train_section, pattern=r"^train_\d+_(all|\d+)$"))
    app.add_handler(CallbackQueryHandler(cb_answer, pattern=r"^ans_[AaBbCcDd]_\d+$"))
    app.add_handler(CallbackQueryHandler(cb_next_q, pattern=r"^next_q$"))
    app.add_handler(CallbackQueryHandler(cb_blocked, pattern=r"^blocked$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guard))

    logger.info("%s started", BOT_NAME)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
