import logging

from config import texts
from database import (
    get_or_create_user,
    add_expense,
    get_today_expenses,
    get_month_expenses
)
from utils.logger_decorator import log_command


logger = logging.getLogger(__name__)


@log_command
async def start(update, context):
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
        parse_mode="HTML"
    )


@log_command
async def help(update, context):
    '''
    A function for outputting all the commands of the bot.
    '''
    await update.message.reply_text(
        texts.HELP_MESSAGE,
        parse_mode="HTML"
    )


@log_command
async def add(update, context):
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
        expense_id = add_expense(
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
async def today(update, context):
    '''
    A function for displaying expenses for today.
    Information is taken for each user from the database.
    '''
    user = update.effective_user

    # Get expenses from DB
    expenses = get_today_expenses(user.id)

    # Format
    if not expenses:
        await update.message.reply_text("Сегодня ещё нет расходов")
        return

    total = sum(e['amount'] for e in expenses)
    lines = [f"<b>Расходы за сегодня:</b>\n"]

    for exp in expenses:
        desc = f" — {exp['description']}" if exp['description'] else ""
        lines.append(f"• {exp['amount']} руб. ({exp['category']}){desc}")

    lines.append(f"\n<b>Итого: {total} руб.</b>")

    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


@log_command
async def month(update, context):
    '''
    A function for displaying expenses for month.
    Information is taken for each user from the database.
    '''
    user = update.effective_user

    stats = get_month_expenses(user.id)

    if not stats:
        await update.message.reply_text("В этом месяце ещё нет расходов.")
        return

    response = ["📊 <b>Статистика за месяц:</b>\n"]
    for item in stats:
        response.append(
            f"• {item['category']}: {item['total']} руб. ({item['count']} раз)"
        )

    total = sum(item['total'] for item in stats)
    response.append(f"\n<b>Общая сумма: {total} руб.</b>")

    await update.message.reply_text("\n".join(response), parse_mode="HTML")
