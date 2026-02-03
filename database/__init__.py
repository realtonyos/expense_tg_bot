from .crud import (
    get_or_create_user,
    update_user_settings,
    get_user_settings,
    add_expense,
    get_today_expenses,
    get_month_expenses,
    init_database
)

# Инициализация БД при импорте
init_database()
