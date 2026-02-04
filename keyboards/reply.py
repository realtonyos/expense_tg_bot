"""
Reply-keyboards for quick access to commands.
"""

from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    The main keyboard with two buttons.
    Appears below the message input field.
    """
    keyboard = [
        [KeyboardButton("➕ Добавить расход")],
        [KeyboardButton("📂 Категории")]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,  # The buttons adjust to the size
        one_time_keyboard=False,  # The keyboard stays on all the time
        input_field_placeholder="Выберите действие..."  # Hint in input field
    )


def get_hide_keyboard() -> ReplyKeyboardMarkup:
    """
    An empty keyboard to hide the current one.
    """
    return ReplyKeyboardMarkup([[]], resize_keyboard=True)
