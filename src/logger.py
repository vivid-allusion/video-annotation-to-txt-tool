"""Logging configuration for extraction tool.

Uses loguru for structured console logging.
"""

from loguru import logger
import sys

from .exceptions import ExtractionError

# Configure loguru logger
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
)


def log_error(exception: ExtractionError) -> None:
    """Log an extraction error with exit code.

    Args:
        exception: The extraction error to log
    """
    logger.error(f"{exception.message} (Exit Code: {exception.exit_code})")


def log_success(message: str, count: int) -> None:
    """Log a success message with item count.

    Args:
        message: Success message
        count: Number of items processed
    """
    logger.success(f"{message}: {count}")


def log_info(message: str) -> None:
    """Log an informational message.

    Args:
        message: Information to log
    """
    logger.info(message)
