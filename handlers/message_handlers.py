from telegram import Update
from telegram.ext import (
    filters,
    CommandHandler,
    ContextTypes
)


async def handle_message(update, context):
    await update.message.reply_text(
        "Я понимаю только команды, которые описаны в /help"
    )
