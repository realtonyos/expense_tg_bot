import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from config.config import TOKEN
from handlers import (
    message_handlers,
    command_handlers
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    application = ApplicationBuilder().token(token=TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', command_handlers.start))
    application.add_handler(CommandHandler('help', command_handlers.help))
    application.add_handler(CommandHandler('add', command_handlers.add))
    application.add_handler(CommandHandler('today', command_handlers.today))
    application.add_handler(CommandHandler('month', command_handlers.month))

    # Register message handlers
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message_handlers.handle_message
        ))

    application.run_polling()


if __name__ == '__main__':
    main()
