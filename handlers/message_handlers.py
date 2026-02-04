from telegram import Update
from telegram.ext import ContextTypes

from config.texts import texts
from keyboards.reply import get_main_keyboard
from utils.logger_decorator import log_message


@log_message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks and regular messages."""
    text = update.message.text

    if text == texts.buttons.ADD_EXPENSE:
        await update.message.reply_text(
            texts.general.ADD_EXPENSE_PROMPT,
            parse_mode="HTML",
        )

    elif text == texts.buttons.CATEGORIES:
        await update.message.reply_text(
            texts.general.CATEGORIES_LIST,
            reply_markup=get_main_keyboard(),
            parse_mode="HTML",
        )

    else:
        await update.message.reply_text(
            texts.general.UNKNOWN_COMMAND,
            reply_markup=get_main_keyboard(),
        )
