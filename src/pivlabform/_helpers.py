import json
import logging
import os
import sys
import urllib.parse

import colorlog
import typing_extensions
import yaml

from . import _consts
from .gitlab.models import GroupSettings, Variable, Variables


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


def get_settings_json(
    config: dict[str, typing_extensions.Any],
    section: str,
) -> dict[str, typing_extensions.Any]:
    settings = GroupSettings(**config[section])

    group_settings_json = settings.to_api_json()
    LOGGER.debug(f"group settings: {json.dumps(group_settings_json, indent=4,)}")

    return group_settings_json


def get_variables_json(
    config: dict[str, typing_extensions.Any],
    section: str,
) -> list[dict[str, typing_extensions.Any]]:
    variables = Variables(variables=config[section]["variables"])

    group_variables_json = variables.to_api_variables()
    LOGGER.debug(f"group vars: {json.dumps(group_variables_json, indent=4,)}")

    return group_variables_json


def get_urlencoded_path(path: str) -> str:
    return urllib.parse.quote_plus(path)


def get_gitlab_host() -> str:
    return os.getenv("CI_SERVER_HOST", "https://pivlab.space")


def get_gitlab_token() -> str:
    return os.getenv("GITLAB_TOKEN", "")


def check_variables_diff(
    current_vars: list[dict[str, typing_extensions.Any]],
    config_vars: list[dict[str, typing_extensions.Any]],
) -> dict[str, list[Variables]]:
    result: dict[str, list[Variables]] = {
        "create": [],
        "update": [],
        "delete": [],
        "unchanged": [],
    }

    current_lookup = {}
    config_lookup = {}

    for var in current_vars:
        key = var.get("key", "")
        scope = var.get("environment_scope", "*")
        current_lookup[(key, scope)] = var

    for var in config_vars:
        key = var.get("key", "")
        scope = var.get("environment_scope", "*")
        config_lookup[(key, scope)] = var

    for (
        key,  # type: ignore
        scope,  # type: ignore
    ), config_var in (  # type: ignore
        config_lookup.items()
    ):
        if (key, scope) not in current_lookup:
            result["create"].append(
                config_var,  # type: ignore
            )

    for (
        key,  # type: ignore
        scope,  # type: ignore
    ), current_var in (  # type: ignore
        current_lookup.items()
    ):
        if (key, scope) in config_lookup:
            config_var = config_lookup[(key, scope)]  # type: ignore
            if not _are_variables_equal(
                current_var,  # type: ignore
                config_var,  # type: ignore
            ):
                result["update"].append(config_var)  # type: ignore
            else:
                result["unchanged"].append(current_var)  # type: ignore
        else:
            result["delete"].append(current_var)  # type: ignore

    LOGGER.debug(
        f"Variables diff: "
        f"create={len(result['create'])}, "
        f"update={len(result['update'])}, "
        f"delete={len(result['delete'])}, "
        f"unchanged={len(result['unchanged'])}"
    )

    return result


def _are_variables_equal(var1: Variable, var2: Variable) -> bool:
    fields_to_compare = [
        "value",
        "masked",
        "protected",
        "raw",
        "variable_type",
        "description",
    ]

    for field in fields_to_compare:
        val1 = var1.get(field)  # type: ignore
        val2 = var2.get(field)  # type: ignore

        if field in ["masked", "protected", "raw"]:
            val1 = bool(val1) if val1 is not None else False  # type: ignore
            val2 = bool(val2) if val2 is not None else False  # type: ignore

        if isinstance(val1, (int, float)):
            val1 = str(val1)
        if isinstance(val2, (int, float)):
            val2 = str(val2)

        if val1 != val2:
            return False

    return True
