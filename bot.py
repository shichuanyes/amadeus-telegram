import json
import logging
from typing import Dict

import requests
from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters

CONFIG_NAME: str = "config.json"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    requests.post(WEBHOOK, json={'content': text})
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Forwarded")


if __name__ == '__main__':
    config: Dict = {}
    try:
        with open(CONFIG_NAME, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        with open(CONFIG_NAME, 'w+') as f:
            f.write("{}")
            f.seek(0)
            config = json.load(f)

    if "token" not in config or len(config['token']) == 0:
        config['token'] = input("Bot token not found! Please input bot token: ")
    TOKEN = config["token"]
    if "webhook" not in config or len(config['webhook']) == 0:
        config['webhook'] = input("Discord webhook not found! Please input webhook: ")
    WEBHOOK = config["webhook"]

    with open(CONFIG_NAME, 'w+') as f:
        json.dump(config, f)

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    forward_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), forward)

    application.add_handler(start_handler)
    application.add_handler(forward_handler)

    application.run_polling()
