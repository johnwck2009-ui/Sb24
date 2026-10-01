import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("sb24-info")

BOT_TOKEN = os.environ["BOT_TOKEN"]

state = {
    "latest_info": None,
}


def score_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("⚽ Live Score", callback_data="live_score"),
            InlineKeyboardButton("📊 Match Score", callback_data="match_score"),
        ],
        [
            InlineKeyboardButton("🏆 Latest Scores", callback_data="latest_scores"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "⚽ សូមស្វាគមន៍មកកាន់ SB24!\n\n"
        "មើលព័ត៌មានពិន្ទុការប្រកួត បាល់ទាត់ និងលទ្ធផលសម្រាប់ការប្រកួតដែលអ្នកចាប់អារម្មណ៍។\n\n"
        "សូមជ្រើសរើសព័ត៌មានពិន្ទុដែលអ្នកចង់មើល៖",
        reply_markup=score_menu(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    messages = {
        "live_score": "⚽ Live Score\n\nព័ត៌មានពិន្ទុការប្រកួតកំពុងដំណើរការ។",
        "match_score": "📊 Match Score\n\nព័ត៌មានពិន្ទុ និងលទ្ធផលការប្រកួត។",
        "latest_scores": "🏆 Latest Scores\n\nលទ្ធផល និងពិន្ទុការប្រកួតថ្មីៗ។",
    }

    await query.message.reply_text(
        messages.get(query.data, "សូមជ្រើសរើសជម្រើសមួយ។"),
        reply_markup=score_menu(),
    )


async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    info = state["latest_info"] or "មិនទាន់មានព័ត៌មានថ្មី។"
    await update.message.reply_text(f"ព័ត៌មានថ្មីៗ៖ {info}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot is online and ready.")


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("latest", latest))
    app.add_handler(CommandHandler("status", status))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
