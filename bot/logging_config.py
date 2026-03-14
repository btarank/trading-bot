import logging
import os


def setup_logger(name: str) -> logging.Logger:
    """
    Creates a logger that:
    - Writes DEBUG+ logs to logs/trading_bot.log (full detail for submission)
    - Prints WARNING+ logs to console only (clean UX)
    """
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers on re-import
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler - full DEBUG detail
    file_handler = logging.FileHandler("logs/trading_bot.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler - warnings and errors only 
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
