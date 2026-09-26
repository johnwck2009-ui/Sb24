# SB24 Live Results Bot

Telegram bot for live round and result notifications.

## Telegram profile

**Name:** SB24 Live Results

**About:** ការជូនដំណឹងអំពីជុំផ្សាយផ្ទាល់ និងលទ្ធផលថ្មីៗ

**Description:** ជូនដំណឹងអំពីជុំផ្សាយផ្ទាល់ និងលទ្ធផលថ្មីៗដោយស្វ័យប្រវត្តិ។

## Features

- Khmer-language start message
- /latest command
- /status command
- Uses only the Telegram Bot API
- No external live-data URL or API required
- Ready to deploy on Render

## Setup

1. Create a Telegram bot with BotFather.
2. Set only the `BOT_TOKEN` environment variable on Render.
3. Start the service with `python bot.py`.

The repository does not include the Telegram token or other private credentials.

## Important

This version does not automatically obtain live round/result data from an external source. It can run independently using only the Telegram Bot API.
