import logging
import functools

logger = logging.getLogger(__name__)


def log_command(func):
    """A decorator for logging bot commands"""
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        command = (
            f"/{func.__name__}" if not func.__name__.startswith('/') else func.__name__
        )
        # Logging the start of execution
        logger.info(
            f"🟢 Command {command} called by {user.id} (@{user.username})"
        )

        try:
            # Calling the original function
            result = await func(update, context, *args, **kwargs)

            # Logging a successful completion
            logger.info(f"✅ Command {command} completed for user {user.id}")
            return result

        except Exception as e:
            # Logging the error
            logger.error(
                f"❌ Error in {command} for {user.id}: {str(e)}", exc_info=True
            )
            raise  # Pushing the error further

    return wrapper


def log_message(func):
    """A decorator for logging messages"""
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        text = update.message.text[:50]  # The first 50 characters

        logger.info(f"💬 Message from {user.id}: '{text}...'")
        return await func(update, context, *args, **kwargs)

    return wrapper
