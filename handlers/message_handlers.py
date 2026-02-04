from telegram import Update
from telegram.ext import ContextTypes

from config import texts
from keyboards.reply import get_main_keyboard
from utils.logger_decorator import log_message


@log_message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий кнопок и обычных сообщений"""
    text = update.message.text

    if text == "➕ Добавить расход":
        # Redirect to the /add command
        await update.message.reply_text(
            texts.ADD_EXPENSE,
            parse_mode="HTML"
        )

    elif text == "📂 Категории":
        # Redirect to the /categories command
        await update.message.reply_text(
            texts.CATEGORIES,
            reply_markup=get_main_keyboard(),
            parse_mode="HTML"
        )

    else:
        # A regular message (not a button)
        await update.message.reply_text(
            texts.UNKNOWN_COMMAND,
            reply_markup=get_main_keyboard()
        )
