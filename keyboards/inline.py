"""Inline keyboards."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config.texts import texts
from config.categories import DEFAULT_CATEGORIES


def get_categories_keyboard(amount: float = None) -> InlineKeyboardMarkup:
    """Inline keyboard with categories from DEFAULT_CATEGORIES."""
    categories = list(DEFAULT_CATEGORIES.keys())
    buttons = []

    for i in range(0, len(categories), 2):
        row = []

        cat1 = categories[i]
        emoji1 = DEFAULT_CATEGORIES[cat1]["emoji"]
        callback1 = _build_callback_data("add", cat1, amount)
        row.append(InlineKeyboardButton(
            f"{emoji1} {cat1}",
            callback_data=callback1,
        ))

        if i + 1 < len(categories):
            cat2 = categories[i + 1]
            emoji2 = DEFAULT_CATEGORIES[cat2]["emoji"]
            callback2 = _build_callback_data("add", cat2, amount)
            row.append(InlineKeyboardButton(
                f"{emoji2} {cat2}",
                callback_data=callback2,
            ))

        buttons.append(row)

    if amount:
        buttons.append([
            InlineKeyboardButton(
                texts.buttons.CUSTOM_CATEGORY,
                callback_data="custom",
            ),
            InlineKeyboardButton(
                texts.buttons.CANCEL,
                callback_data="cancel",
            ),
        ])

    return InlineKeyboardMarkup(buttons)


def get_confirm_keyboard(amount: float, category: str) -> InlineKeyboardMarkup:
    """Keyboard for confirmation."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                texts.buttons.CONFIRM_YES,
                callback_data=f"confirm:{category}:{amount}",
            ),
            InlineKeyboardButton(
                texts.buttons.CONFIRM_NO,
                callback_data="cancel",
            ),
        ],
    ])


def _build_callback_data(action: str,
                         category: str, amount: float = None) -> str:
    """Build callback data string."""
    if amount:
        return f"{action}:{category}:{amount}"
    return f"{action}:{category}"
