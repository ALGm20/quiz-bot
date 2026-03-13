import logging
import asyncio
from datetime import datetime, date
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)
from database import Database

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── Conversation States ───────────────────────────────────────────────────────
WAITING_NAME = 1

# ─── Database instance ─────────────────────────────────────────────────────────
db = Database("quiz_bot.db")


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def back_btn(callback: str = "main_menu") -> list:
    return [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data=callback)]]


def build_main_menu(student_name: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📚 اختر فصلاً للمذاكرة", callback_data="choose_chapter")],
        [InlineKeyboardButton("🎯 الاختبار اليومي", callback_data="daily_quiz")],
        [InlineKeyboardButton("📊 نتائجي", callback_data="my_scores")],
        [InlineKeyboardButton("🏆 لوحة الشرف", callback_data="leaderboard")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ══════════════════════════════════════════════════════════════════════════════
#  /start  ──  Registration Flow
# ══════════════════════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)

    if student:
        await update.message.reply_text(
            f"👋 أهلاً مجدداً *{student['full_name']}*!\n\nاختر ما تريد من القائمة أدناه:",
            parse_mode="Markdown",
            reply_markup=build_main_menu(student["full_name"]),
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "🎓 *مرحباً بك في بوت الاختبارات!*\n\n"
        "للتسجيل، أرسل *اسمك الثلاثي* كما هو مسجل في قاعدة البيانات.\n\n"
        "مثال: `أحمد محمد علي`",
        parse_mode="Markdown",
    )
    return WAITING_NAME


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    full_name = update.message.text.strip()
    user_id = update.effective_user.id

    student = db.find_student_by_name(full_name)

    if not student:
        await update.message.reply_text(
            "❌ *الاسم غير موجود في قاعدة البيانات.*\n\n"
            "تأكد من كتابة الاسم الثلاثي بالضبط كما هو مسجل.\n"
            "حاول مرة أخرى أو تواصل مع المشرف.",
            parse_mode="Markdown",
        )
        return WAITING_NAME

    if student["telegram_id"] and student["telegram_id"] != user_id:
        await update.message.reply_text(
            "⚠️ هذا الاسم مسجل مسبقاً بحساب آخر. تواصل مع المشرف.",
        )
        return WAITING_NAME

    db.link_telegram_to_student(student["id"], user_id)

    await update.message.reply_text(
        f"✅ *تم التسجيل بنجاح!*\n\n"
        f"أهلاً *{student['full_name']}* 👏\n\n"
        f"يمكنك الآن البدء بالمذاكرة والاختبارات:",
        parse_mode="Markdown",
        reply_markup=build_main_menu(student["full_name"]),
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN MENU callback
# ══════════════════════════════════════════════════════════════════════════════

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)
    if not student:
        await query.edit_message_text("يرجى التسجيل أولاً بإرسال /start")
        return

    await query.edit_message_text(
        f"👋 *{student['full_name']}* — القائمة الرئيسية:",
        parse_mode="Markdown",
        reply_markup=build_main_menu(student["full_name"]),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  CHOOSE CHAPTER
# ══════════════════════════════════════════════════════════════════════════════

async def choose_chapter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chapters = db.get_all_chapters()
    if not chapters:
        await query.edit_message_text("⚠️ لا توجد فصول متاحة حالياً.")
        return

    keyboard = []
    for ch in chapters:
        q_count = db.count_questions_in_chapter(ch["id"])
        keyboard.append([
            InlineKeyboardButton(
                f"📖 {ch['name']}  ({q_count} سؤال)",
                callback_data=f"chapter_{ch['id']}",
            )
        ])
    keyboard += back_btn()

    await query.edit_message_text(
        "📚 *اختر الفصل الذي تريد المذاكرة منه:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def chapter_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chapter_id = int(query.data.split("_")[1])
    chapter = db.get_chapter(chapter_id)

    keyboard = [
        [InlineKeyboardButton("▶️ ابدأ الاختبار (10 أسئلة عشوائية)", callback_data=f"startquiz_{chapter_id}_10")],
        [InlineKeyboardButton("📋 اختبار كامل (كل الأسئلة)", callback_data=f"startquiz_{chapter_id}_all")],
    ] + back_btn("choose_chapter")

    await query.edit_message_text(
        f"📖 *{chapter['name']}*\n\n{chapter.get('description', '')}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  QUIZ ENGINE
# ══════════════════════════════════════════════════════════════════════════════

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)

    parts = query.data.split("_")   # startquiz_<chapter_id>_<count>
    chapter_id = int(parts[1])
    count = parts[2]

    questions = db.get_questions(chapter_id, None if count == "all" else int(count))
    if not questions:
        await query.edit_message_text("⚠️ لا توجد أسئلة في هذا الفصل.")
        return

    # Create session
    session_id = db.create_quiz_session(student["id"], chapter_id, len(questions))
    context.user_data["session"] = {
        "session_id": session_id,
        "questions": questions,
        "current": 0,
        "score": 0,
        "chapter_id": chapter_id,
    }

    await query.edit_message_text("⏳ جاري تحميل الأسئلة...")
    await send_question(update, context, first=True)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, first=False):
    sess = context.user_data.get("session")
    if not sess:
        return

    q_list = sess["questions"]
    idx = sess["current"]

    if idx >= len(q_list):
        await finish_quiz(update, context)
        return

    q = q_list[idx]
    total = len(q_list)
    progress = f"*سؤال {idx+1} من {total}*\n"
    bar = "🟩" * idx + "⬜" * (total - idx)

    text = (
        f"{progress}{bar}\n\n"
        f"❓ *{q['question_text']}*"
    )

    keyboard = [
        [InlineKeyboardButton(f"🅰️  {q['option_a']}", callback_data=f"ans_A_{q['id']}")],
        [InlineKeyboardButton(f"🅱️  {q['option_b']}", callback_data=f"ans_B_{q['id']}")],
        [InlineKeyboardButton(f"🅲  {q['option_c']}", callback_data=f"ans_C_{q['id']}")],
        [InlineKeyboardButton(f"🅳  {q['option_d']}", callback_data=f"ans_D_{q['id']}")],
    ]

    if first:
        # first message after editing "loading..."
        await update.callback_query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        await update.callback_query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    sess = context.user_data.get("session")
    if not sess:
        await query.edit_message_text("انتهت الجلسة. ابدأ من /start")
        return

    parts = query.data.split("_")   # ans_<letter>_<question_id>
    user_answer = parts[1]
    question_id = int(parts[2])

    q_list = sess["questions"]
    idx = sess["current"]
    q = q_list[idx]

    correct = q["correct_answer"].upper()
    is_correct = user_answer == correct

    if is_correct:
        sess["score"] += 1
        icon = "✅"
        result_text = "إجابة صحيحة!"
    else:
        icon = "❌"
        option_map = {"A": q["option_a"], "B": q["option_b"],
                      "C": q["option_c"], "D": q["option_d"]}
        result_text = f"خطأ! الإجابة الصحيحة: *{correct}) {option_map[correct]}*"

    db.save_answer(sess["session_id"], question_id, user_answer, is_correct)

    explanation = q.get("explanation", "")
    exp_text = f"\n\n💡 *الشرح:* {explanation}" if explanation else ""

    feedback = f"{icon} {result_text}{exp_text}"

    # Move to next
    sess["current"] += 1
    context.user_data["session"] = sess

    keyboard = [[InlineKeyboardButton("التالي ➡️", callback_data="next_question")]]

    await query.edit_message_text(
        f"❓ *{q['question_text']}*\n\n{feedback}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await send_question(update, context)


async def finish_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sess = context.user_data.get("session")
    score = sess["score"]
    total = len(sess["questions"])
    pct = round((score / total) * 100)

    if pct >= 90:
        grade = "ممتاز 🏆"
    elif pct >= 75:
        grade = "جيد جداً 🥈"
    elif pct >= 60:
        grade = "جيد 🥉"
    else:
        grade = "بحاجة للمراجعة 📖"

    db.complete_quiz_session(sess["session_id"], score)

    stars = "⭐" * (pct // 20)
    text = (
        f"🎉 *انتهى الاختبار!*\n\n"
        f"النتيجة: *{score} / {total}* ({pct}%)\n"
        f"التقدير: {grade}\n"
        f"{stars}"
    )

    keyboard = [
        [InlineKeyboardButton("🔄 إعادة الفصل", callback_data=f"chapter_{sess['chapter_id']}")],
        [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")],
    ]

    context.user_data.pop("session", None)

    await update.callback_query.edit_message_text(
        text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  DAILY QUIZ
# ══════════════════════════════════════════════════════════════════════════════

async def daily_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)

    today = date.today().isoformat()
    already_done = db.check_daily_done(student["id"], today)

    if already_done:
        score, total = db.get_daily_score(student["id"], today)
        await query.edit_message_text(
            f"✅ لقد أجريت الاختبار اليومي اليوم!\n\n"
            f"نتيجتك: *{score} / {total}*\n\n"
            f"عد غداً للاختبار الجديد 📅",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(back_btn()),
        )
        return

    questions = db.get_daily_questions(today)
    if not questions:
        await query.edit_message_text(
            "⚠️ لا توجد أسئلة للاختبار اليومي حالياً.",
            reply_markup=InlineKeyboardMarkup(back_btn()),
        )
        return

    session_id = db.create_quiz_session(student["id"], None, len(questions), is_daily=True, daily_date=today)
    context.user_data["session"] = {
        "session_id": session_id,
        "questions": questions,
        "current": 0,
        "score": 0,
        "chapter_id": None,
        "is_daily": True,
        "daily_date": today,
    }

    await query.edit_message_text("🎯 *الاختبار اليومي* — 10 أسئلة من جميع الفصول\n\nاستعد! ⏱️",
                                  parse_mode="Markdown")
    await asyncio.sleep(1)
    await send_question(update, context, first=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MY SCORES
# ══════════════════════════════════════════════════════════════════════════════

async def my_scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)

    sessions = db.get_student_sessions(student["id"], limit=10)
    if not sessions:
        await query.edit_message_text(
            "لا توجد نتائج بعد. ابدأ اختباراً!",
            reply_markup=InlineKeyboardMarkup(back_btn()),
        )
        return

    lines = ["📊 *آخر 10 اختبارات:*\n"]
    for s in sessions:
        pct = round((s["score"] / s["total_questions"]) * 100) if s["total_questions"] else 0
        chapter = s["chapter_name"] or "اختبار يومي"
        date_str = s["started_at"][:10]
        lines.append(f"• {date_str} — {chapter}: {s['score']}/{s['total_questions']} ({pct}%)")

    await query.edit_message_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(back_btn()),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  LEADERBOARD
# ══════════════════════════════════════════════════════════════════════════════

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    leaders = db.get_leaderboard(limit=10)
    if not leaders:
        await query.edit_message_text("لا توجد بيانات بعد.",
                                      reply_markup=InlineKeyboardMarkup(back_btn()))
        return

    medals = ["🥇", "🥈", "🥉"] + ["🔹"] * 7
    lines = ["🏆 *لوحة الشرف — أعلى الدرجات:*\n"]
    for i, row in enumerate(leaders):
        lines.append(f"{medals[i]} {row['full_name']} — {row['avg_pct']}%  ({row['total_quizzes']} اختبار)")

    await query.edit_message_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(back_btn()),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN COMMANDS  (إضافة أسئلة عبر ملف JSON)
# ══════════════════════════════════════════════════════════════════════════════

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Only works for admin Telegram ID set in config."""
    user_id = update.effective_user.id
    stats = db.get_stats()
    await update.message.reply_text(
        f"📈 *إحصائيات البوت:*\n\n"
        f"👥 الطلاب المسجلون: {stats['registered']}/{stats['total_students']}\n"
        f"❓ إجمالي الأسئلة: {stats['total_questions']}\n"
        f"📋 الاختبارات المنجزة: {stats['total_sessions']}\n"
        f"📚 الفصول: {stats['total_chapters']}",
        parse_mode="Markdown",
    )


# ══════════════════════════════════════════════════════════════════════════════
#  UNKNOWN / GUARD
# ══════════════════════════════════════════════════════════════════════════════

async def not_registered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    student = db.get_student_by_telegram(user_id)
    if not student:
        await update.message.reply_text(
            "يرجى التسجيل أولاً عبر الأمر /start"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    import os
    TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")

    app = Application.builder().token(TOKEN).build()

    # Registration conversation
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)

    # Admin
    app.add_handler(CommandHandler("stats", admin_stats))

    # Callback queries
    app.add_handler(CallbackQueryHandler(main_menu_callback,  pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(choose_chapter,       pattern="^choose_chapter$"))
    app.add_handler(CallbackQueryHandler(chapter_menu,         pattern=r"^chapter_\d+$"))
    app.add_handler(CallbackQueryHandler(start_quiz,           pattern=r"^startquiz_\d+_(all|\d+)$"))
    app.add_handler(CallbackQueryHandler(handle_answer,        pattern=r"^ans_[ABCD]_\d+$"))
    app.add_handler(CallbackQueryHandler(next_question,        pattern="^next_question$"))
    app.add_handler(CallbackQueryHandler(daily_quiz,           pattern="^daily_quiz$"))
    app.add_handler(CallbackQueryHandler(my_scores,            pattern="^my_scores$"))
    app.add_handler(CallbackQueryHandler(leaderboard,          pattern="^leaderboard$"))

    # Catch-all text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, not_registered))

    logger.info("Bot started ✅")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
