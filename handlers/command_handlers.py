import logging

from telegram import Update
from telegram.ext import ContextTypes

from config.texts import texts
from config.categories import DEFAULT_CATEGORIES
from database import (
    get_or_create_user,
    get_today_expenses,
    get_month_expenses,
    add_expense
)
from utils.logger_decorator import log_command
from utils.formatter import format_expenses
from keyboards.reply import (
    get_main_keyboard,
    get_hide_keyboard,
)
from keyboards.inline import get_categories_keyboard


logger = logging.getLogger(__name__)


@log_command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start interaction with the bot."""
    user = update.effective_user
    get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )
    await update.message.reply_text(
        texts.commands.START.format(first_name=user.first_name),
        reply_markup=get_main_keyboard(),
        parse_mode="HTML",
    )


@log_command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show all bot commands."""
    await update.message.reply_text(
        texts.commands.HELP,
        parse_mode="HTML",
    )


@log_command
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add expense."""
    user = update.effective_user

    try:
        get_or_create_user(user.id, user.username, user.first_name)
    except Exception as e:
        logger.error(f"DB error: {e}")
        await update.message.reply_text(texts.errors.DB_CONNECTION)
        return

    if not context.args:
        await update.message.reply_text(texts.errors.INVALID_FORMAT)
        return

    # Only amount: /add 1500 → show buttons
    if len(context.args) == 1:
        try:
            amount = float(context.args[0])
            if 0 < amount <= 1_000_000:
                await update.message.reply_text(
                    f"Выберите категорию для {amount} ₽:",
                    reply_markup=get_categories_keyboard(amount)
                )
            else:
                await update.message.reply_text(texts.errors.INVALID_NUMBER)
        except ValueError:
            await update.message.reply_text(texts.errors.NOT_A_NUMBER)
        return

    # Amount + category: /add 1500 продукты
    try:
        amount = float(context.args[0].replace(',', '.'))
        if amount <= 0 or amount >= 1_000_000:
            await update.message.reply_text(texts.errors.INVALID_NUMBER)
            return
    except ValueError:
        await update.message.reply_text(texts.errors.NOT_A_NUMBER)
        return

    category = context.args[1].strip()
    if len(category) > 50 or len(category) < 2:
        await update.message.reply_text(texts.errors.INVALID_CATEGORY)
        return

    description = None
    if len(context.args) > 2:
        description = ' '.join(context.args[2:])
        if len(description) > 200:
            description = description[:197] + "..."

    try:
        add_expense(user.id, amount, category, description)
        await update.message.reply_text(
            f"Расход {amount} на '{category}' сохранён!"
        )
    except Exception as e:
        logger.error(f"DB error: {e}")
        await update.message.reply_text(texts.errors.DB_CONNECTION)


@log_command
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show expenses for today."""
    user = update.effective_user
    expenses = get_today_expenses(user.id)

    if not expenses:
        await update.message.reply_text(texts.general.NO_EXPENSES_TODAY)
        return

    response = format_expenses(
        data=expenses,
        title="Расходы за сегодня",
        mode="list",
    )
    await update.message.reply_text(response, parse_mode="HTML")


@log_command
async def month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show expenses for month."""
    user = update.effective_user
    stats = get_month_expenses(user.id)

    if not stats:
        await update.message.reply_text(texts.general.NO_EXPENSES_MONTH)
        return

    response = format_expenses(
        data=stats,
        title="Статистика за месяц",
        mode="stats",
    )
    await update.message.reply_text(response, parse_mode="HTML")


@log_command
async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available categories."""
    lines = ["📂 <b>Доступные категории:</b>\n"]

    for category, data in DEFAULT_CATEGORIES.items():
        if data["default"]:
            lines.append(f"{data['emoji']} {category} — {data['description']}")

    lines.append(texts.general.CATEGORY_HINT)

    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


@log_command
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show keyboard menu."""
    await update.message.reply_text(
        texts.general.MENU_TITLE,
        reply_markup=get_main_keyboard(),
    )


@log_command
async def hide_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hide the keyboard."""
    await update.message.reply_text(
        texts.general.KEYBOARD_HIDDEN,
        reply_markup=get_hide_keyboard(),
    )
