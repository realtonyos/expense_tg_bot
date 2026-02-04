from config.currencies import get_currency_settings
from config.categories import get_category_emoji


def format_currency(amount: float, currency_code: str = "RUB") -> str:
    """Formats the amount based on the currency"""
    settings = get_currency_settings(currency_code)
    formatted = f"{amount:,.2f}"

    if settings["thousands_separator"]:
        parts = formatted.split(".")
        int_part = parts[0].replace(",", settings["thousands_separator"])
        formatted = int_part + "." + parts[1] if len(parts) > 1 else int_part

    if settings["decimal_separator"] != ".":
        formatted = formatted.replace(".", settings["decimal_separator"])

    return f"{formatted} {settings['symbol']}"


def format_expense(amount: float, category: str, description: str = None,
                   expense_id: int = None, date: str = None,
                   currency: str = "RUB") -> str:
    """Formats a single expense"""
    emoji = get_category_emoji(category)
    parts = [f"{emoji} {format_currency(amount, currency)} • {category}"]

    if description:
        parts.append(f"\n   📝 {description}")
    if expense_id is not None:
        parts.append(f" (ID: {expense_id})")
    if date:
        parts.append(f" 📅 {date}")

    return "".join(parts)


def format_expenses(
    data: list,
    title: str = "Расходы",
    mode: str = "list"
) -> str:
    """
    Universal formatter for any periods

    Args:
        data: List of expenses OR statistics
        title: Title ("Today's expenses", "Monthly statistics")
        mode: Mode:
        - "list": list of expenses (for /today)
        - "stats": category statistics (for /month)
        - "auto": automatically detects the data structure
    """
    if not data:
        return f"📭 <b>{title}</b>\nПока ничего нет."

    if mode == "auto":
        if data and 'total' in data[0] and 'count' in data[0]:
            mode = "stats"
        else:
            mode = "list"

    if mode == "list":
        return _format_list(data, title)
    else:  # mode == "stats"
        return _format_stats(data, title)


def _format_list(expenses: list, title: str) -> str:
    """Auxiliary: list of expenses"""
    total = sum(exp.get('amount', 0) for exp in expenses)
    lines = [f"📋 <b>{title}:</b>\n"]

    for i, exp in enumerate(expenses, 1):
        amount = exp.get('amount', 0)
        category = exp.get('category', 'другое')
        description = exp.get('description')
        expense_id = exp.get('id')
        date = exp.get('date')

        expense_str = format_expense(
            amount, category,
            description, expense_id, date
            )
        lines.append(f"{i}. {expense_str}")

    lines.append(f"\n<b>Итого: {format_currency(total)}</b>")
    return "\n".join(lines)


def _format_stats(stats: list, title: str) -> str:
    """Auxiliary: statistics by category"""
    total_all = sum(item.get('total', 0) for item in stats)
    sorted_stats = sorted(stats, key=lambda x: x.get('total', 0), reverse=True)

    lines = [f"📊 <b>{title}:</b>\n"]

    for item in sorted_stats:
        category = item.get('category', 'другое')
        total = item.get('total', 0)
        count = item.get('count', 0)

        percentage = (total / total_all * 100) if total_all > 0 else 0
        bar_length = 10
        filled = int(percentage / 100 * bar_length)
        progress_bar = "█" * filled + "░" * (bar_length - filled)

        lines.append(
            f"• {category}: {format_currency(total)}\n"
            f"  {progress_bar} {percentage:.1f}% ({count} раз)"
        )

    lines.append(f"\n<b>Общая сумма: {format_currency(total_all)}</b>")
    return "\n".join(lines)
