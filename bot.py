import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("sb24-info")

BOT_TOKEN = os.environ["BOT_TOKEN"]

state = {
    "latest_info": None,
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "សូមស្វាគមន៍មកកាន់ SB24 Info។\n"
        "ទទួលបានព័ត៌មាន និងការជូនដំណឹងថ្មីៗតាម Telegram។"
    )


async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    info = state["latest_info"] or "មិនទាន់មានព័ត៌មានថ្មី។"
    await update.message.reply_text(f"ព័ត៌មានថ្មីៗ៖ {info}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot is online and ready.")


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.add_handler(CommandHandler("status", status))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
