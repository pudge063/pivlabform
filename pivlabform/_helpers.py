import yaml
import os
import sys
import typing_extensions
import logging
import colorlog
import urllib.parse
import _consts


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

    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


LOGGER = setup_logger()


def get_resource_from_entity_type(entity_type: str) -> str:
    return _consts.APIResources.from_entity_type(entity_type).value


def load_data_from_yaml(
    yaml_path: str,
) -> dict[str, typing_extensions.Any]:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data


def get_urlencoded_path(path: str) -> str:
    return urllib.parse.quote_plus(path)


def get_gitlab_host() -> str:
    return os.getenv("CI_SERVER_HOST", "")


def get_gitlab_token() -> str:
    return os.getenv("GITLAB_TOKEN", "")
