import json
import sys

import typing_extensions

from . import _helpers
from ._helpers import LOGGER
from .gitlab.gitlab import GitLab
from .gitlab.models import ConfigModel


class Pivlabform:
    def __init__(
        self: typing_extensions.Self,
        config_file: str,
        gitlab_host: str,
    ) -> None:
        self.gl = GitLab(gitlab_host)

        config_model = ConfigModel(**_helpers.load_data_from_yaml(config_file))
        self.config_model_json = config_model.dump_model_to_json()

        LOGGER.info(
            f"config_model_json:\n{json.dumps(self.config_model_json, indent=4)}"
        )

    def validate_configuration(
        self: typing_extensions.Self,
    ):
        # TODO: validation for CI with dry-run
        pass

    def _process_entity_configuration(
        self: typing_extensions.Self,
        entities: list[int | None],
        entity_type: str,
    ) -> None:
        for entity in entities:
            self.gl.confugure_entity(
                entity_id=entity,  # type: ignore
                entity_type=entity_type,
                config=self.config_model_json[f"{entity_type}_config"]["settings"],  # type: ignore
            )

            self.gl.update_entity_variables(
                entity_id=entity,  # type: ignore
                entity_type=entity_type,
                config_variables=self.config_model_json[f"{entity_type}_config"][
                    "variables"
                ],
            )

    def process_manual_configuration(
        self: typing_extensions.Self,
        path_type: typing_extensions.Optional[str],
        path: typing_extensions.Optional[str],
        id: typing_extensions.Optional[int],
        recursive: bool,
        validate: bool,
    ):
        if not path_type:
            LOGGER.error("ERROR: not provided type of path")
            sys.exit(1)
        if not path and not id or (id and path):
            LOGGER.error("ERROR: required only one argumend - `id` or `path`")
            sys.exit(1)
        if recursive and path_type == "project":
            LOGGER.error("ERROR: recursive only for groups")
            sys.exit(1)

        if not id:
            id = self.gl.get_entity_id_from_url(
                entity_path=path,  # type: ignore
                entity_type=path_type,
            )

        groups: list[int | None]
        projects: list[int | None]
        groups, projects = [], []

        if path_type == "group":
            groups = self.gl.get_all_groups_recursive(id) if recursive else [id]
            projects = (
                self.gl.get_all_projects_recursive(id)
                if recursive
                else self.gl.get_all_projects_from_group(id)
            )
        elif path_type == "project":
            groups = []
            projects = [id]

        LOGGER.info(f"groups: {groups}")
        LOGGER.info(f"projects: {projects}")

        _helpers.check_validate(validate)

        self._process_entity_configuration(
            entities=groups,  # type: ignore
            entity_type="group",
        )

        self._process_entity_configuration(
            entities=projects,  # type: ignore
            entity_type="project",
        )

    def get_entities_id_list(
        self: typing_extensions.Self,
        recursive: bool,
    ) -> tuple[list[int], list[int]]:

        projects = self.config_model_json.get("projects", [])
        groups = self.config_model_json.get("groups", [])

        LOGGER.warning(f"projects: {projects}")
        LOGGER.warning(f"groups: {groups}")

        project_entities: list[int] = []
        group_entities: list[int] = []

        for group in groups:
            if type(group) is str:
                id = self.gl.get_entity_id_from_url(group, "group")
            elif type(group) is int:
                id = group
            else:
                LOGGER.error(f"ERROR: unknown type of group: {group} - {type(group)}")
                sys.exit(1)

            if recursive:
                group_entities.extend(
                    self.gl.get_all_groups_recursive(
                        id,
                    )  # type: ignore
                )
                project_entities.extend(
                    self.gl.get_all_projects_recursive(
                        id,
                    )  # type: ignore
                )
            else:
                project_entities.extend(
                    self.gl.get_all_projects_from_group(
                        id,
                    )  # type: ignore
                )

            group_entities.append(id)

        for project in projects:
            if type(project) is str:
                id = self.gl.get_entity_id_from_url(project, "project")
            elif type(project) is int:
                id = project
            else:
                LOGGER.error(
                    f"ERROR: unknown type of group: {project} - {type(project)}"
                )
                sys.exit(1)

            project_entities.append(id)

        return (group_entities, project_entities)

    def process_auto_configuration(
        self: typing_extensions.Self,
        recursive: bool,
        validate: bool,
    ):

        groups, projects = self.get_entities_id_list(
            recursive=recursive,
        )

        LOGGER.warning(f"projects for configuration: {projects}")
        LOGGER.warning(f"groups for configuration: {groups}")

        _helpers.check_validate(validate)

        if projects:
            self._process_entity_configuration(
                entities=projects,  # type: ignore
                entity_type="project",
            )

        if groups:
            self._process_entity_configuration(
                entities=groups,  # type: ignore
                entity_type="group",
            )
