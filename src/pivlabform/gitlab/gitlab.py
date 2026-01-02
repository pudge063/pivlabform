import json
import sys
from enum import Enum

import requests
from typing_extensions import Any, Self

from ..utils import _helpers
from ..utils._helpers import LOGGER


class Entity(str, Enum):
    GROUP = "groups"
    PROJECT = "projects"
    SUBGROUP = "subgroups"

    @property
    def lname(self) -> str:
        return self.name.lower()

    @classmethod
    def from_string(cls, value: str) -> "Entity":
        value_lower = value.lower().strip()

        mapping = {
            "group": cls.GROUP,
            "project": cls.PROJECT,
            "subgroup": cls.SUBGROUP,
            "g": cls.GROUP,
            "p": cls.PROJECT,
            "s": cls.SUBGROUP,
        }

        if value_lower in mapping:
            return mapping[value_lower]
        LOGGER.error(f"Unknown entity type: {value}")
        sys.exit(1)


class GitLab:
    def __init__(
        self: Self,
        gitlab_host: str = "",
    ):
        gitlab_host = _helpers.get_gitlab_host() if not gitlab_host else gitlab_host
        self.gitlab_api_url = f"{gitlab_host}/api/v4"
        self.gitlab_session = requests.Session()

        self.gitlab_session.headers.update(
            {"PRIVATE-TOKEN": _helpers.get_gitlab_token()}
        )

    def _send_gitlab_request(
        self: Self,
        method: str = "GET",
        url_postfix: str = "",
        data: dict[str, Any] | Any = {},
    ) -> requests.Response:
        r = self.gitlab_session.request(
            method=method,
            url=f"{self.gitlab_api_url}/{url_postfix}",
            json=data,
        )

        if not r.ok:
            LOGGER.error(f"ERROR: {r.status_code}:{r.text}")
            LOGGER.error(f"URL: {self.gitlab_api_url}/{url_postfix}")
            LOGGER.error(f"DATA:\n{json.dumps(data, indent=4)}")
            if not _helpers.ignore_errors():
                sys.exit(1)

        return r

    def get_all_projects_from_group(
        self: Self,
        target_group: int,
    ) -> list[int]:
        all_projects: list[int] = []
        next_page = 1

        while True:
            r = self._send_gitlab_request(
                method="GET",
                url_postfix=(
                    f"{Entity.GROUP.value}/{target_group}/{Entity.PROJECT.value}"
                    "?pagination=keyset"
                    "&per_page=100"
                    "&order_by=id"
                    f"&page={next_page}"
                ),
            )

            if not r.ok:
                raise RuntimeError(f"ERROR: {r.text}" f"STATUS: {r.status_code}")

            found_projects = [project["id"] for project in r.json()]

            all_projects.extend(found_projects)

            next_page += 1

            if len(r.json()) < 100:
                break

        return all_projects

    def get_all_groups_from_group(
        self: Self,
        target_group: int,
    ) -> list[int]:
        all_groups: list[int] = []
        next_page = 1

        while True:
            r = self._send_gitlab_request(
                method="GET",
                url_postfix=(
                    f"{Entity.GROUP.value}/{target_group}/{Entity.SUBGROUP.value}"
                    "?pagination=keyset"
                    "&per_page=100"
                    "&order_by=id"
                    f"&page={next_page}"
                ),
            )

            if not r.ok:
                raise RuntimeError(f"ERROR: {r.text}" f"STATUS: {r.status_code}")

            found_groups = [group["id"] for group in r.json()]

            all_groups.extend(found_groups)

            if len(r.json()) < 100:
                break

        return all_groups

    def get_all_groups_recursive(
        self: Self,
        target_group: int,
        groups: list[int] = [],
    ):
        LOGGER.debug(f"finding subgroups in {target_group}")
        subgroups = self.get_all_groups_from_group(target_group)
        LOGGER.debug(f"found subgroups: {subgroups}")
        groups.extend(subgroups)

        for subgroup in subgroups:
            groups = self.get_all_groups_recursive(
                subgroup,
                groups,
            )

        return groups

    def get_all_projects_recursive(
        self: Self,
        target_group: int,
        projects: list[int] = [],
    ) -> list[int]:

        LOGGER.debug(f"finding projects in {target_group}")
        projects.extend(self.get_all_projects_from_group(target_group))
        LOGGER.debug(f"found projects: {projects}")

        subgroups = self.get_all_groups_from_group(target_group)
        for subgroup in subgroups:
            projects = self.get_all_projects_recursive(
                subgroup,
                projects,
            )

        return projects

    def get_entity_id_from_url(
        self: Self,
        entity_path: str,
        entity_type: Entity,
    ) -> int:
        url_path = _helpers.get_urlencoded_path(entity_path)

        r = self._send_gitlab_request(
            method="GET",
            url_postfix=f"{entity_type.value}/{url_path}",
        )

        return r.json()["id"]

    def confugure_entity(
        self: Self,
        entity_id: int | int,
        entity_type: Entity,
        config: dict[str, Any],
    ) -> None:
        self._send_gitlab_request(
            method="PUT",
            url_postfix=(f"{entity_type.value}/{entity_id}"),
            data=config,
        )

        LOGGER.debug(f"{entity_type.lname} {entity_id} configured success")

    def update_entity_variables(
        self: Self,
        entity_id: int,
        entity_type: Entity,
        config_variables: list[dict[str, Any]],
    ):
        r = self._send_gitlab_request(
            method="GET",
            url_postfix=f"{entity_type.value}/{entity_id}/variables",
        )
        current_variables = r.json()

        variables = _helpers.check_variables_diff(current_variables, config_variables)

        for var in variables["create"]:
            self._send_gitlab_request(
                method="POST",
                url_postfix=(f"{entity_type.value}/{entity_id}/variables"),
                data=var,
            )

        for var in variables["update"]:
            self._send_gitlab_request(
                method="PUT",
                url_postfix=(
                    (f"{entity_type.value}/" f"{entity_id}/variables/{var['key']}")
                ),
                data=var,
            )

        # COMMENT THIS BLOCK FOR DISABLE REMOVING VARIABLES
        for var in variables["delete"]:
            self._send_gitlab_request(
                method="DELETE",
                url_postfix=(
                    (f"{entity_type.value}/" f"{entity_id}/variables/{var['key']}")
                ),
            )

    def update_entity_protected_branches(
        self: Self,
        entity_id: int,
        entity_type: Entity,
        config_protected_branches: dict[str, Any],
    ) -> None:
        r = self._send_gitlab_request(
            method="GET",
            url_postfix=(f"{entity_type.value}/{entity_id}/protected_branches"),
        )

        if entity_type == Entity.GROUP and not self.is_top_level_group(entity_id):
            LOGGER.info(f"SKIP: group {entity_id} is not top-level")
            return None

        current_branches = _helpers.parse_protected_branches(r.json())

        LOGGER.debug(f"current_branches:\n{json.dumps(current_branches, indent=2)}")
        LOGGER.debug(
            (
                f"config_protected_branches:\n"
                f"{json.dumps(config_protected_branches, indent=2)}"
            )
        )

        for branch in current_branches:
            if branch not in config_protected_branches:
                LOGGER.debug(f"REMOVE: {branch} not found in config")
                self._send_gitlab_request(
                    method="DELETE",
                    url_postfix=(
                        f"{entity_type.value}/{entity_id}/protected_branches/{branch}"
                    ),
                )

        for branch in config_protected_branches:
            if branch in current_branches:
                if not config_protected_branches[branch] == current_branches[branch]:
                    LOGGER.debug(f"REMOVE: {branch} in entity and config has diff")
                    self._send_gitlab_request(
                        method="DELETE",
                        url_postfix=(
                            f"{entity_type.value}/"
                            f"{entity_id}/protected_branches/{branch}"
                        ),
                    )
                else:
                    LOGGER.debug(f"SKIP: {branch} in entity and config are equals")
                    continue

            branch_data = {"name": branch}
            branch_params = config_protected_branches[branch]
            if branch_params:
                branch_data.update(branch_params)
            LOGGER.debug(f"CREATE: {branch} added to entity")
            self._send_gitlab_request(
                method="POST",
                url_postfix=(f"{entity_type.value}/{entity_id}/protected_branches"),
                data=branch_data,
            )

    def is_top_level_group(self: Self, group_id: int) -> bool:
        response = self._send_gitlab_request(
            method="GET",
            url_postfix=f"{Entity.GROUP.value}/{group_id}",
        )
        group_info = response.json()

        return group_info.get("parent_id") is None

    def create_entity(
        self: Self,
        entity_type: Entity,
        entity_settings: dict[str, Any],
    ) -> int:
        r = self._send_gitlab_request(
            method="POST",
            url_postfix=f"{entity_type.value}",
            data=entity_settings,
        )

        return r.json()["id"]

    def archive_entity(
        self: Self,
        entity_id: int,
        entity_type: Entity,
        archive: bool,
    ) -> None:
        if entity_type == Entity.GROUP:
            """
            Archive GitLab group currently unavailable
            https://gitlab.com/gitlab-org/gitlab/-/issues/15967
            https://gitlab.com/groups/gitlab-org/-/epics/15019
            """
            LOGGER.warning(
                "archive group disabled in GitLab, see issue:"
                "https://gitlab.com/groups/gitlab-org/-/epics/15019"
            )
            return None

        status = "archive" if archive else "unarchive"

        self._send_gitlab_request(
            method="POST",
            url_postfix=f"{entity_type.value}/{entity_id}/{status}",
        )

    def delete_entity(
        self: Self,
        entity_id: int,
        entity_type: Entity,
    ):
        self._send_gitlab_request(
            method="DELETE",
            url_postfix=f"{entity_type.value}/{entity_id}",
        )
