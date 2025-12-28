import sys

import requests
import typing_extensions

from .. import _helpers, gvars
from .._helpers import LOGGER


class GitLab:
    def __init__(
        self: typing_extensions.Self,
        gitlab_host: str | None,
    ):
        gitlab_host = _helpers.get_gitlab_host() if not gitlab_host else gitlab_host
        self.gitlab_api_url = f"{gitlab_host}/{gvars.Base.API_PREFIX.value}"
        self.gitlab_session = requests.Session()

        self.gitlab_session.headers.update(
            {gvars.Base.TOKEN.value: _helpers.get_gitlab_token()}
        )

    def _send_gitlab_request(
        self: typing_extensions.Self,
        method: str = "GET",
        url_postfix: str = "",
        data: dict[str, str | int] | typing_extensions.Any = {},
    ) -> requests.Response:
        r = self.gitlab_session.request(
            method=method,
            url=f"{self.gitlab_api_url}/{url_postfix}",
            json=data,
        )

        if not r.ok:
            LOGGER.error(f"ERROR: {r.status_code}:{r.text}")
            sys.exit(1)

        return r

    def get_all_projects_from_group(
        self: typing_extensions.Self,
        target_group: int,
    ) -> list[int | None]:
        all_projects: list[int | None] = []
        next_page = 1

        while True:
            r = self._send_gitlab_request(
                method="GET",
                url_postfix=(
                    f"groups/{target_group}/projects"
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
        self: typing_extensions.Self,
        target_group: int,
    ) -> list[int | None]:
        all_groups: list[int | None] = []
        next_page = 1

        while True:
            r = self._send_gitlab_request(
                method="GET",
                url_postfix=(
                    f"groups/{target_group}/subgroups"
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
        self: typing_extensions.Self,
        target_group: int,
        groups: list[int | None] = [],
    ):
        LOGGER.debug(f"finding subgroups in {target_group}")
        subgroups = self.get_all_groups_from_group(target_group)
        LOGGER.debug(f"found subgroups: {subgroups}")
        groups.extend(subgroups)

        for subgroup in subgroups:
            groups = self.get_all_groups_recursive(
                subgroup,  # pyright: ignore[reportArgumentType]
                groups,
            )

        return groups

    def get_all_projects_recursive(
        self: typing_extensions.Self,
        target_group: int,
        projects: list[int | None] = [],
    ) -> list[int | None]:
        LOGGER.debug(f"finding projects in {target_group}")
        projects.extend(self.get_all_projects_from_group(target_group))
        LOGGER.debug(f"found projects: {projects}")

        subgroups = self.get_all_groups_from_group(target_group)
        for subgroup in subgroups:
            projects = self.get_all_projects_recursive(
                subgroup,  # pyright: ignore[reportArgumentType]
                projects,
            )

        return projects

    def get_entity_id_from_url(
        self: typing_extensions.Self,
        entity_path: str,
        entity_type: str,
    ) -> int:
        url_path = _helpers.get_urlencoded_path(entity_path)

        r = self._send_gitlab_request(
            method="GET",
            url_postfix=f"{_helpers.get_resource_from_entity_type(entity_type)}/{url_path}",
        )

        return r.json()["id"]

    def confugure_entity(
        self: typing_extensions.Self,
        entity_id: int | int,
        entity_type: str,
        config: dict[str, typing_extensions.Any],
    ) -> None:
        self._send_gitlab_request(
            method="PUT",
            url_postfix=(
                f"{_helpers.get_resource_from_entity_type(entity_type)}/{entity_id}"
            ),
            data=config,
        )

        LOGGER.info(f"{entity_type} {entity_id} configured success")

    def update_entity_variables(
        self: typing_extensions.Self,
        entity_id: int,
        entity_type: str,
        config_variables: list[dict[str, typing_extensions.Any]],
    ):
        r = self._send_gitlab_request(
            method="GET",
            url_postfix=f"{_helpers.get_resource_from_entity_type(entity_type)}/{entity_id}/variables",
        )
        current_variables = r.json()

        variables = _helpers.check_variables_diff(current_variables, config_variables)

        for var in variables["create"]:
            self._send_gitlab_request(
                method="POST",
                url_postfix=(
                    f"{_helpers.get_resource_from_entity_type(entity_type)}/{entity_id}/variables"
                ),
                data=var,
            )

        for var in variables["update"]:
            self._send_gitlab_request(
                method="PUT",
                url_postfix=(
                    f"{_helpers.get_resource_from_entity_type(entity_type)}/{entity_id}/variables/{var['key']}"  # type: ignore
                ),
                data=var,
            )

        # COMMENT THIS BLOCK FOR DISABLE REMOVING VARIABLES
        for var in variables["delete"]:
            self._send_gitlab_request(
                method="DELETE",
                url_postfix=(
                    f"{_helpers.get_resource_from_entity_type(entity_type)}/{entity_id}/variables/{var['key']}"  # type: ignore
                ),
            )
