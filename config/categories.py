"""
Default expense categories.
Users will be able to add their own.
"""

DEFAULT_CATEGORIES = {
    "продукты": {
        "emoji": "🛒",
        "description": "Продукты питания из магазинов",
        "default": True
    },
    "еда": {
        "emoji": "🍔",
        "description": "Обеды в кафе, рестораны, доставка",
        "default": True
    },
    "транспорт": {
        "emoji": "🚗",
        "description": "Такси, метро, бензин, каршеринг",
        "default": True
    },
    "развлечения": {
        "emoji": "🎬",
        "description": "Кино, концерты, игры, хобби",
        "default": True
    },
    "кафе": {
        "emoji": "☕",
        "description": "Кофе, перекусы, фастфуд",
        "default": True
    },
    "здоровье": {
        "emoji": "🏥",
        "description": "Аптека, врачи, спортзал",
        "default": True
    },
    "образование": {
        "emoji": "📚",
        "description": "Курсы, книги, обучающие материалы",
        "default": True
    },
    "одежда": {
        "emoji": "👕",
        "description": "Одежда, обувь, аксессуары",
        "default": True
    },
    "коммуналка": {
        "emoji": "🏠",
        "description": "Квартплата, электричество, интернет",
        "default": True
    },
    "другое": {
        "emoji": "📦",
        "description": "Прочие расходы",
        "default": True
    }
}

# Для быстрого доступа
CATEGORY_EMOJIS = {cat: data["emoji"] for cat, data in DEFAULT_CATEGORIES.items()}


def get_category_emoji(category_name: str) -> str:
    """Returns an emoji for the category or the default emoji"""
    return CATEGORY_EMOJIS.get(category_name.lower(), "💰")
