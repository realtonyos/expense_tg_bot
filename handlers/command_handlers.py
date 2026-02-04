import logging

from telegram import Update
from telegram.ext import ContextTypes

from config import texts
from config.categories import DEFAULT_CATEGORIES
from database import (
    get_or_create_user,
    add_expense,
    get_today_expenses,
    get_month_expenses
)
from utils.logger_decorator import log_command
from utils.formatter import format_expenses
from keyboards.reply import (
    get_main_keyboard,
    get_hide_keyboard
)


logger = logging.getLogger(__name__)


@log_command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''
    Starting interaction with the bot.
    The bot receives information about the user and adds it to the database.
    '''
    user = update.effective_user
    get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )
    await update.message.reply_text(
        texts.START_MESSAGE.format(first_name=user.first_name),
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )


@log_command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''
    A function for outputting all the commands of the bot.
    '''
    await update.message.reply_text(
        texts.HELP_MESSAGE,
        parse_mode="HTML"
    )


@log_command
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''
    Function to add user expenses to the database.
    Accepts /add sum category. Parse sum and category
    And save it in DB.
    '''
    user = update.effective_user
    # Register user
    try:
        get_or_create_user(user.id, user.username, user.first_name)
    except Exception as e:
        logger.error(f"DB error while registering user {user.id}: {e}")
        await update.message.reply_text(texts.ERROR_DB_CONNECTION)
        return

    # Parse /add sum category
    # Check for arguments
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(texts.ERROR_INVALID_FORMAT)
        return

    # Valid amount
    amount_text = context.args[0]
    try:
        amount = float(amount_text.replace(',', '.'))
    except ValueError:
        await update.message.reply_text(texts.ERROR_NOT_A_NUMBER)
        return

    if amount <= 0 or amount >= 1_000_000:
        await update.message.reply_text(texts.ERROR_INVALID_NUMBER)
        return

    # Valid category
    category = context.args[1].strip()
    if len(category) > 50 or len(category) < 2:
        await update.message.reply_text(texts.ERROR_INVALID_CATEGORY)
        return

    # Get a description
    description = None
    if len(context.args) > 2:
        description = ' '.join(context.args[2:])
        if len(description) > 200:
            description = description[:197] + "..."

    # Save in DB
    try:
        add_expense(
            user_id=user.id,
            amount=amount,
            category=category,
            description=description
        )

        await update.message.reply_text(
            f"Расход {amount} на '{category}' сохранён!"
        )
    except Exception as e:
        logger.error(f"DB error while adding expense for user {user.id}: {e}")
        await update.message.reply_text(texts.ERROR_DB_CONNECTION)


@log_command
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    A function for displaying expenses for day.
    Information is taken for each user from the database.
    '''
    user = update.effective_user
    expenses = get_today_expenses(user.id)
    if not expenses:
        await update.message.reply_text("За сегодня расходов нет.")
        return
    response = format_expenses(
        data=expenses,
        title="Расходы за сегодня",
        mode="list"  # или "auto"
    )
    await update.message.reply_text(response, parse_mode="HTML")


@log_command
async def month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''
    A function for displaying expenses for month.
    Information is taken for each user from the database.
    '''
    user = update.effective_user
    stats = get_month_expenses(user.id)
    if not stats:
        await update.message.reply_text("В этом месяце ещё нет расходов.")
        return
    response = format_expenses(
        data=stats,
        title="Статистика за месяц",
        mode="stats"  # или "auto"
    )
    await update.message.reply_text(response, parse_mode="HTML")


@log_command
async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /categories - show available categories"""
    lines = ["📂 <b>Доступные категории:</b>\n"]

    for category, data in DEFAULT_CATEGORIES.items():
        if data["default"]:  # только дефолтные
            lines.append(f"{data['emoji']} {category} — {data['description']}")

    lines.append(
        "\n💡 <i>Используйте любую категорию при добавлении расхода</i>"
    )

    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


@log_command
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /menu — show keyboard"""
    await update.message.reply_text(
        "Основное меню:",
        reply_markup=get_main_keyboard()
    )


@log_command
async def hide_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /hide — hide the keyboard"""
    await update.message.reply_text(
        "Клавиатура скрыта. Используйте /menu чтобы вернуть.",
        reply_markup=get_hide_keyboard()
    )
