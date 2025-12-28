import sys

import typing_extensions

from . import _helpers
from ._helpers import LOGGER
from .gitlab.gitlab import GitLab


class Pivlabform:
    def __init__(
        self: typing_extensions.Self,
        gitlab_host: str,
    ) -> None:
        self.gl = GitLab(gitlab_host)

    def validate_configuration(
        self: typing_extensions.Self,
    ):
        # TODO: validation for CI with dry-run
        pass

    def _process_entity_configuration(
        self: typing_extensions.Self,
        config: dict[str, typing_extensions.Any],
        entities: list[str | None],
        entity_type: str,
    ) -> None:
        group_variables_json = None
        group_settings_json = _helpers.get_settings_json(
            config, f"{entity_type}_settings"
        )
        if "variables" in config[f"{entity_type}_settings"]:
            group_variables_json = _helpers.get_variables_json(
                config,
                f"{entity_type}_settings",
            )

        for entity in entities:
            self.gl.confugure_entity(
                entity,  # type: ignore
                entity_type,
                group_settings_json,  # type: ignore
            )

            if group_variables_json:
                self.gl.update_entity_variables(
                    entity_id=entity,  # type: ignore
                    entity_type=entity_type,
                    config_variables=group_variables_json,
                )

    def process_manual_configuration(
        self: typing_extensions.Self,
        path_type: typing_extensions.Optional[str],
        path: typing_extensions.Optional[str],
        id: typing_extensions.Optional[int],
        config_file: str,
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

        config = _helpers.load_data_from_yaml(config_file)

        if validate:
            LOGGER.warning("validate only")
            sys.exit(0)

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

        self._process_entity_configuration(
            config=config,
            entities=groups,  # type: ignore
            entity_type="group",
        )

        self._process_entity_configuration(
            config=config,
            entities=projects,  # type: ignore
            entity_type="project",
        )

    def get_entities_list(
        self: typing_extensions.Self,
        config: dict[str, typing_extensions.Any],
        recursive: bool,
    ) -> tuple[list[int], list[int]]:
        projects: list[str | int] = config["projects"] if "projects" in config else []
        groups: list[str | int] = config["groups"] if "groups" in config else []

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
        config_file: str,
        recursive: bool,
        validate: bool,
    ):
        config = _helpers.load_data_from_yaml(config_file)

        groups, projects = self.get_entities_list(
            config=config,
            recursive=recursive,
        )

        LOGGER.warning(f"projects for configuration: {projects}")
        LOGGER.warning(f"groups for configuration: {groups}")

        self._process_entity_configuration(
            config=config,
            entities=projects,  # type: ignore
            entity_type="project",
        )

        self._process_entity_configuration(
            config=config,
            entities=groups,  # type: ignore
            entity_type="group",
        )
