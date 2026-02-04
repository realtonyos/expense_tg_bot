"""Logging decorators for the bot."""

import logging
import functools


logger = logging.getLogger(__name__)


def log_command(func):
    """Decorator for logging bot commands."""
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        command = (
            f"/{func.__name__}"
            if not func.__name__.startswith("/")
            else func.__name__
        )

        logger.info(
            f"Command {command} called by {user.id} (@{user.username})"
        )

        try:
            result = await func(update, context, *args, **kwargs)
            logger.info(f"Command {command} completed for user {user.id}")
            return result

        except Exception as e:
            logger.error(
                f"Error in {command} for {user.id}: {str(e)}",
                exc_info=True,
            )
            raise

    return wrapper


def log_message(func):
    """Decorator for logging messages."""
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        text = update.message.text[:50]

        logger.info(f"Message from {user.id}: '{text}...'")
        return await func(update, context, *args, **kwargs)

    return wrapper
