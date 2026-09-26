import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]

state = {"round_id": None, "result": None}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "សូមស្វាគមន៍មកកាន់ SB24 Live Results។\n"
        "ទទួលបានការជូនដំណឹងអំពីជុំផ្សាយផ្ទាល់ និងលទ្ធផលថ្មីៗ។"
    )

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not state["round_id"]:
        await update.message.reply_text("មិនទាន់មានទិន្នន័យថ្មី។")
        return
    result = state["result"] or "កំពុងរង់ចាំលទ្ធផល"
    await update.message.reply_text(
        f"Round: {state['round_id']}\nResult: {result}"
    )

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
