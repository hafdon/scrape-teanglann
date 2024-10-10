import logging
import sys


def setup_logging():
    # Create a logger with a specific name
    logger = logging.getLogger("my_logger")

    # Prevent the logger from propagating messages to the root logger
    logger.propagate = False

    # Check if handlers are already added to prevent duplication
    if not logger.handlers:
        # Set the minimum log level for the logger
        logger.setLevel(logging.DEBUG)  # Adjust as needed

        # Create formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Create and configure file handler
        file_handler = logging.FileHandler("program.log", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Adjust as needed
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Create and configure console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)  # Adjust as needed
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
