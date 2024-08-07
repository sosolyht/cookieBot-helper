# File: my_logger.py
# Path: utils\my_logger.py

import logging

RESET = "\033[0m"
COLORS = {
    'INFO': "\033[94m",
    'WARNING': "\033[93m",
    'DEBUG': "\033[33m",
    'ERROR': "\033[91m",
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, RESET)
        message = super().format(record)
        return f"{log_color}{message}{RESET}"

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    console_formatter = ColoredFormatter(format_string)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(console_handler)

    return logger
