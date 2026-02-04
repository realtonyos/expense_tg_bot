from utils.logger_decorator import log_message


@log_message
async def handle_message(update, context):
    await update.message.reply_text(
        "Я понимаю только команды, которые описаны в /help"
    )
