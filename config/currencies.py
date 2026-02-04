"""
Supported currencies and their settings.
"""

CURRENCIES = {
    "RUB": {
        "symbol": "₽",
        "name": "Российский рубль",
        "decimal_separator": ",",  # fractional part separator
        "thousands_separator": " ",  # thousand separator
        "default": True  # default currency
    },
    "USD": {
        "symbol": "$",
        "name": "Доллар США",
        "decimal_separator": ".",
        "thousands_separator": ",",
        "default": False
    },
    "EUR": {
        "symbol": "€",
        "name": "Евро",
        "decimal_separator": ",",
        "thousands_separator": " ",
        "default": False
    },
    "KZT": {
        "symbol": "₸",
        "name": "Казахстанский тенге",
        "decimal_separator": ",",
        "thousands_separator": " ",
        "default": False
    }
}

# Active currencies (to show to the user)
ACTIVE_CURRENCIES = ["RUB", "USD", "EUR"]


def get_currency_settings(currency_code: str):
    """Returns the default currency settings or RUB"""
    return CURRENCIES.get(currency_code.upper(), CURRENCIES["RUB"])
