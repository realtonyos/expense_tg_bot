import logging

from telegram import Update
from telegram.ext import ContextTypes

from database import add_expense
from keyboards.inline import get_confirm_keyboard
from config.texts import texts


logger = logging.getLogger(__name__)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple callback handler."""
    query = update.callback_query
    await query.answer()

    data = query.data
    parts = data.split(":")

    if parts[0] == "add":
        # add:category:amount
        category = parts[1]
        amount = float(parts[2])

        await query.edit_message_text(
            texts.callbacks.CONFIRM_QUESTION.format(
                amount=amount, 
                category=category
            ),
            reply_markup=get_confirm_keyboard(amount, category)
        )

    elif parts[0] == "confirm":
        # confirm:category:amount
        category = parts[1]
        amount = float(parts[2])
        user_id = query.from_user.id

        add_expense(user_id, amount, category)

        await query.edit_message_text(
            texts.callbacks.SUCCESS_ADDED.format(
                amount=amount,
                category=category
            )
        )

    elif parts[0] == "custom":
        await query.edit_message_text(
            texts.callbacks.PROMPT_CUSTOM_CATEGORY
        )
        context.user_data['awaiting_category'] = True

    elif parts[0] == "cancel":
        await query.edit_message_text(texts.callbacks.CANCELLED)
        if 'pending_expense' in context.user_data:
            del context.user_data['pending_expense']
