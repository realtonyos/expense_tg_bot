"""Reply keyboards for quick access to commands."""

from telegram import ReplyKeyboardMarkup, KeyboardButton

from config.texts import texts


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Main keyboard with two buttons."""
    keyboard = [
        [KeyboardButton(texts.buttons.ADD_EXPENSE)],
        [KeyboardButton(texts.buttons.CATEGORIES)],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие...",
    )


def get_hide_keyboard() -> ReplyKeyboardMarkup:
    """Empty keyboard to hide the current one."""
    return ReplyKeyboardMarkup([[]], resize_keyboard=True)
