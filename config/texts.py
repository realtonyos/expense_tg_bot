"""
Text constants of the bot.
All user responses are collected here for easy editing.
"""

# Command /start
START_MESSAGE = """
Привет, {first_name}!

Я бот для учёта расходов. 
Я помогу вам отслеживать, на что уходят деньги.

<b>Основные команды:</b>
/add <i>[сумма] [категория]</i> — добавить расход
/today — расходы за сегодня
/month — статистика за месяц
/stats — общая статистика
/help — показать это сообщение

Просто начните вводить команды!
"""

# Command /help
HELP_MESSAGE = """
<b>Доступные команды:</b>

<b>Основные</b>
/start — начать работу
/help — эта справка

<b>Учёт расходов</b>
/add <i>сумма категория</i> — добавить расход
/today — показать сегодняшние расходы
/month — статистика за текущий месяц
/categories — управление категориями

<b>Настройки</b>
/limit <i>сумма</i> — установить дневной лимит
/settings — настройки бота

Пример: <code>/add 1500 продукты</code>
"""

# Errors
ERROR_INVALID_FORMAT = "Неверный формат. Используйте: /add <сумма> <категория>"
ERROR_DB_CONNECTION = "Ошибка подключения к базе данных. Попробуйте позже."
ERROR_NOT_A_NUMBER = "Сумма должна быть числом!"


# General answers
WELCOME_BACK = "С возвращением, {first_name}!"
UNKNOWN_COMMAND = "Неизвестная команда. Используйте /help для списка команд."
