from telegram import Update
from telegram.ext import (
    filters,
    CommandHandler,
    ContextTypes
)


async def start(update, context):
    await update.message.reply_text("Привет!")


async def help(update, context):
    pass


async def add():
    pass


async def today():
    pass


async def month():
    pass


async def stats():
    pass
