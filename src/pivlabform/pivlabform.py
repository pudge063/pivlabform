import json
import sys

from typing_extensions import Any, Optional, Self

from .gitlab.gitlab import Entity, GitLab
from .gitlab.models import ConfigModel, ProtectedBranch, Variable
from .utils import _helpers
from .utils._helpers import LOGGER


class Pivlabform:
    def __init__(
        self: Self,
        config_file: str,
        gitlab_host: str,
    ) -> None:
        self.gl = GitLab(gitlab_host)

        config_model = ConfigModel(**_helpers.load_data_from_yaml(config_file))
        self.config_model_json = config_model.dump_model_to_json()

        LOGGER.debug(
            f"config_model_json:\n{json.dumps(self.config_model_json, indent=2)}\n"
        )

    def _process_entity_configuration(
        self: Self,
        entities: list[int | None],
        entity_type: Entity,
    ) -> None:
        for entity in entities:
            LOGGER.info(f"processing: {entity_type.lname} - {entity}")
            entity_config: dict[str, Any] = self.config_model_json.get(
                f"{entity_type.lname}_config", {}
            )

            settings: dict[str, Any] = entity_config.get("settings", {})

            variables: list[dict[str, Variable]] = entity_config.get(
                "variables",
                [],
            )

            protected_branches: dict[str, ProtectedBranch] = entity_config.get(
                "protected_branches",
                {},
            )

            if settings:
                LOGGER.info(f"configure settings in entity: {entity}")
                self.gl.confugure_entity(
                    entity_id=entity,  # type: ignore
                    entity_type=entity_type,
                    config=settings,
                )

            if variables:
                LOGGER.info(f"update variables in entity: {entity}")
                self.gl.update_entity_variables(
                    entity_id=entity,  # type: ignore
                    entity_type=entity_type,
                    config_variables=variables,
                )

            if protected_branches:
                LOGGER.info(f"update protected branches entity: {entity}")
                self.gl.update_entity_protected_branches(
                    entity_id=entity,  # type: ignore
                    entity_type=entity_type,
                    config_protected_branches=protected_branches,
                )

    def process_manual_configuration(
        self: Self,
        path_type: Optional[str],
        path: Optional[str],
        id: Optional[int],
        recursive: bool,
        validate: bool,
    ):
        if not path_type:
            LOGGER.error("ERROR: not provided type of path")
            sys.exit(1)

        entity_type = Entity.from_string(path_type)

        if not path and not id or (id and path):
            LOGGER.error("ERROR: required only one argumend - `id` or `path`")
            sys.exit(1)

        if recursive and not entity_type == Entity.GROUP:
            LOGGER.error("ERROR: recursive apply only for groups")
            sys.exit(1)

        if not id:
            id = self.gl.get_entity_id_from_url(
                entity_path=path,  # type: ignore
                entity_type=entity_type,
            )

        groups: list[int]
        projects: list[int]
        groups, projects = [], []

        if entity_type == Entity.GROUP.lname:
            groups = self.gl.get_all_groups_recursive(id) if recursive else [id]
            projects = (
                self.gl.get_all_projects_recursive(id)
                if recursive
                else self.gl.get_all_projects_from_group(id)
            )
        elif entity_type == Entity.PROJECT.lname:
            groups = []
            projects = [id]

        LOGGER.info(f"groups: {groups}")
        LOGGER.info(f"projects: {projects}")

        _helpers.check_validate(validate)

        self._process_entity_configuration(
            entities=groups,  # type: ignore
            entity_type=Entity.GROUP,
        )

        self._process_entity_configuration(
            entities=projects,  # type: ignore
            entity_type=Entity.PROJECT,
        )

    def get_entities_id_list(
        self: Self,
        recursive: bool,
    ) -> tuple[list[int], list[int]]:

        projects = self.config_model_json.get("projects", [])
        groups = self.config_model_json.get("groups", [])

        LOGGER.info((f"config entities:\nprojects: {projects}\ngroups: {groups}\n"))

        project_entities: list[int] = []
        group_entities: list[int] = []

        for group in groups:
            if type(group) is str:
                id = self.gl.get_entity_id_from_url(group, Entity.GROUP)
            elif type(group) is int:
                id = group
            else:
                LOGGER.error(f"ERROR: unknown type of group: {group} - {type(group)}")
                sys.exit(1)

            if recursive:
                LOGGER.info("finding recursive groups and projects")
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
                id = self.gl.get_entity_id_from_url(project, Entity.PROJECT)
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
        self: Self,
        recursive: bool,
        validate: bool,
    ):

        groups, projects = self.get_entities_id_list(
            recursive=recursive,
        )

        LOGGER.info(
            (
                "found entities for setup:\n"
                f"projects for configuration: {projects}\n"
                f"groups for configuration: {groups}\n"
            )
        )

        _helpers.check_validate(validate)

        if projects:
            self._process_entity_configuration(
                entities=projects,  # type: ignore
                entity_type=Entity.PROJECT,
            )

        if groups:
            self._process_entity_configuration(
                entities=groups,  # type: ignore
                entity_type=Entity.GROUP,
            )
