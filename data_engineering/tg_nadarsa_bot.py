#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import requests
import os
import csv
from datetime import datetime


from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    log_user_action(user.id, "/start")
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def process_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    user_id = update.effective_user.id
    log_user_action(user_id, f"вопрос: {user_text}")
    
    def get_iam_token():
        response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
        json={'yandexPassportOauthToken': "token"})
        response.raise_for_status()
        
        return response.json()['iamToken']

    # Получаем IAM токен
    iam_token = get_iam_token()

    # Собираем запрос
    data = {}
    # Указываем тип модели
    data["modelUri"] = f"gpt://b1gj13o6a5r2fp51llq8/yandexgpt"
    # Настраиваем опции
    data["completionOptions"] = {"temperature": 0.3, "maxTokens": 1000}
    # Указываем контекст для модели
    data["messages"] = [
        {"role": "user", "text": f"{user_text}"},
    ]

    URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    # Отправляем запрос
    response = requests.post(
        URL,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {iam_token}"
        },
        json=data,
    ).json()

    # Распечатываем результат
    print(response)

    answer = response.get('result', {})\
                     .get('alternatives', [{}])[0]\
                     .get('message', {})\
                     .get('text', {})

    await update.message.reply_text(answer)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("token").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    

def log_user_action(user_id: int, action: str) -> None:
    # Убедимся, что папка существует
    os.makedirs("data", exist_ok=True)
    filepath = "data/user_logs.csv"

    # Формируем строку данных
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [user_id, timestamp, action]

    # Записываем в файл
    write_header = not os.path.exists(filepath)
    with open(filepath, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["user_id", "timestamp", "action"])
        writer.writerow(row)


if __name__ == "__main__":
    main()