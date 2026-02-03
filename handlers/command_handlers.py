from config.texts import START_MESSAGE, HELP_MESSAGE
from database import (
    get_or_create_user,
    add_expense,
    get_today_expenses,
    get_month_expenses
)


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
        START_MESSAGE.format(first_name=user.first_name),
        parse_mode="HTML"
    )


async def help(update, context):
    '''
    A function for outputting all the commands of the bot.
    '''
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode="HTML"
    )


async def add(update, context):
    '''
    Function to add user expenses to the database.
    Accepts /add sum category. Parse sum and category
    And save it in DB.
    '''
    user = update.effective_user
    get_or_create_user(user.id, user.username, user.first_name)
    
    # Parse /add sum category
    if len(context.args) < 2:
        await update.message.reply_text("Формат: /add <сумма> <категория>")
        return

    try:
        amount = float(context.args[0])
        category = context.args[1]
        description = " ".join(context.args[2:]) if len(context.args) > 2 else None
    except ValueError:
        await update.message.reply_text("Сумма должна быть числом!")
        return

    # Save in DB
    expense_id = add_expense(
        user_id=user.id,
        amount=amount,
        category=category,
        description=description
    )

    await update.message.reply_text(f"Расход {amount} на '{category}' сохранён!")


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
    
