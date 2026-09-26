import asyncio
import json
import logging
import os
from dataclasses import dataclass
from typing import Any

import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("sb24-live-results")

BOT_TOKEN = os.environ["BOT_TOKEN"]
ALERT_CHAT_ID = os.getenv("ALERT_CHAT_ID")
DATA_URL = os.getenv("DATA_URL", "")
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "5"))
ROUND_ID_PATH = os.getenv("ROUND_ID_PATH", "round_id")
RESULT_PATH = os.getenv("RESULT_PATH", "result")


@dataclass
class LiveState:
    round_id: str | None = None
    result: str | None = None


state = LiveState()


def get_path(data: Any, path: str) -> Any:
    value = data
    for key in path.split("."):
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None
    return value


async def fetch_live_data() -> dict[str, Any] | None:
    if not DATA_URL:
        return None
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(DATA_URL) as response:
                response.raise_for_status()
                return await response.json()
    except Exception:
        log.exception("Unable to fetch live data")
        return None


async def send_alert(app: Application, text: str) -> None:
    if not ALERT_CHAT_ID:
        log.info("Alert destination not configured: %s", text)
        return
    await app.bot.send_message(chat_id=ALERT_CHAT_ID, text=text)


async def poller(app: Application) -> None:
    while True:
        data = await fetch_live_data()
        if data is not None:
            round_id = get_path(data, ROUND_ID_PATH)
            result = get_path(data, RESULT_PATH)

            if round_id is not None and str(round_id) != state.round_id:
                state.round_id = str(round_id)
                state.result = None
                await send_alert(app, f"ជុំថ្មី\nRound: {state.round_id}")

            if result is not None and str(result) != state.result:
                state.result = str(result)
                if state.round_id:
                    await send_alert(
                        app,
                        f"លទ្ធផលថ្មី\nRound: {state.round_id}\nResult: {state.result}",
                    )
        await asyncio.sleep(POLL_SECONDS)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "សូមស្វាគមន៍មកកាន់ SB24 Live Results។\n"
        "ទទួលបានការជូនដំណឹងអំពីជុំផ្សាយផ្ទាល់ និងលទ្ធផលថ្មីៗ។"
    )


async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not state.round_id:
        await update.message.reply_text("មិនទាន់មានទិន្នន័យថ្មី។")
        return
    result = state.result or "កំពុងរង់ចាំលទ្ធផល"
    await update.message.reply_text(
        f"Round: {state.round_id}\nResult: {result}"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    configured = "បានកំណត់" if DATA_URL else "មិនទាន់កំណត់"
    await update.message.reply_text(f"Live data source: {configured}")


async def post_init(app: Application) -> None:
    app.create_task(poller(app))


def main() -> None:
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.add_handler(CommandHandler("status", status))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
