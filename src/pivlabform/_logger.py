import logging
import colorlog
import sys
import os


def setup_logger():
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s:%(levelname)s:%(name)s:%(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)

    debug = os.getenv("DEBUG", False)
    logger.setLevel(logging.DEBUG) if debug else logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


LOGGER = setup_logger()
