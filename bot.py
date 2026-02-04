"""Main bot file."""

import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config.config import TOKEN
from handlers import (
    command_handlers,
    message_handlers,
    callbacks,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    """Start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", command_handlers.start))
    application.add_handler(CommandHandler("help", command_handlers.help))
    application.add_handler(CommandHandler("add", command_handlers.add))
    application.add_handler(CommandHandler("today", command_handlers.today))
    application.add_handler(CommandHandler("month", command_handlers.month))
    application.add_handler(
        CommandHandler("category", command_handlers.show_categories)
    )
    application.add_handler(CommandHandler("menu", command_handlers.show_menu))
    application.add_handler(
        CommandHandler("hide", command_handlers.hide_keyboard)
    )

    # Callback handlers
    application.add_handler(CallbackQueryHandler(callbacks.handle_callback))

    # Message handlers
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handlers.handle_message,
        )
    )

    application.run_polling()


if __name__ == "__main__":
    main()
