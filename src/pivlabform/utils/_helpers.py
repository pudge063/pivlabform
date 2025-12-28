import os
import sys
import urllib.parse

import typing_extensions
import yaml

from . import _consts
from ._logger import LOGGER
from ..gitlab.models import Variable


def get_resource_from_entity_type(entity_type: str) -> str:
    return _consts.APIResources.from_entity_type(entity_type).value


def check_validate(validate: bool) -> None:
    if validate:
        LOGGER.warning("DRY-RUN: validate flag enabled")
        sys.exit(1)


def load_data_from_yaml(
    yaml_path: str,
) -> dict[str, typing_extensions.Any]:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data


def get_urlencoded_path(path: str) -> str:
    return urllib.parse.quote_plus(path)


def get_gitlab_host() -> str:
    return os.getenv("CI_SERVER_HOST", "https://pivlab.space")


def get_gitlab_token() -> str:
    return os.getenv("GITLAB_TOKEN", "")


def _normalize_variables(
    variables: typing_extensions.Union[
        list[dict[str, typing_extensions.Any]],
        dict[str, dict[str, typing_extensions.Any]],
    ],
) -> list[dict[str, typing_extensions.Any]]:
    if isinstance(variables, dict):
        # format: {"VAR_NAME": {...}}
        result: list[dict[str, typing_extensions.Any]] = []
        for _, var_data in variables.items():
            # Если в данных нет ключа "key", добавляем его из имени
            var_dict = dict(var_data)
            # if "key" not in var_dict or not var_dict["key"]:
            #     var_dict["key"] = var_name
            result.append(var_dict)
        return result
    elif isinstance(variables, list):  # type: ignore
        # format: [{"key": "VAR_NAME", ...}]
        return variables
    else:
        return []


def check_variables_diff(
    current_vars: list[dict[str, typing_extensions.Any]],
    config_vars: list[dict[str, typing_extensions.Any]],
) -> dict[str, list[dict[str, Variable]]]:
    current_list = _normalize_variables(current_vars)
    config_list = _normalize_variables(config_vars)

    result: dict[str, list[dict[str, Variable]]] = {
        "create": [],
        "update": [],
        "delete": [],
        "unchanged": [],
    }

    current_lookup = {}
    config_lookup = {}

    for var in current_list:
        key = var.get("key", "")
        scope = var.get("environment_scope", "*")
        current_lookup[(key, scope)] = var

    for var in config_list:
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
