# SB24 Live Results Bot

Telegram notification bot for live round and result updates.

## Telegram profile

**Name:** SB24 Live Results

**About:** ការជូនដំណឹងអំពីជុំផ្សាយផ្ទាល់ និងលទ្ធផលថ្មីៗ

**Description:** ជូនដំណឹងអំពីជុំផ្សាយផ្ទាល់ និងលទ្ធផលថ្មីៗដោយស្វ័យប្រវត្តិ។

## Features

- Khmer-language start message
- New-round notifications
- New-result notifications
- /latest command
- /status command
- Configurable live-data endpoint and JSON field paths

## Setup

1. Create a Telegram bot with BotFather and put its token in `BOT_TOKEN`.
2. Set `ALERT_CHAT_ID` to the Telegram channel/group where alerts should be posted.
3. Set `DATA_URL` to an authorized live-data endpoint.
4. Adjust `ROUND_ID_PATH` and `RESULT_PATH` to match the JSON returned by the data source.
5. Install dependencies with `pip install -r requirements.txt`.
6. Run `python bot.py`.

The repository does not include a Telegram token or any private credentials. Only use a data source you are authorized to access.
