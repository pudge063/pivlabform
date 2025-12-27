import typing_extensions
import sys
import json
import _helpers
from _helpers import LOGGER
from gitlab.gitlab import GitLab
from gitlab.models.configs import ProjectSettings, GroupSettings


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

    def process_manual_configuration(
        self: typing_extensions.Self,
        path_type: typing_extensions.Optional[str],
        path: typing_extensions.Optional[str],
        id: typing_extensions.Optional[str],
        config_file: str,
        recursive: bool,
    ):
        if not path_type:
            LOGGER.error(f"ERROR: not provided type of path")
            sys.exit(1)
        if not path and not id or (id and path):
            LOGGER.error(f"ERROR: required only one argumend - `id` or `path`")
            sys.exit(1)
        if recursive and path_type == "project":
            LOGGER.error(f"ERROR: recursive only for groups")
            sys.exit(1)

        config = _helpers.load_data_from_yaml(config_file)
        if path_type == "group" and "group_settings" in config:
            group_settings = GroupSettings(**config["group_settings"])
            group_settings_json = group_settings.to_api_json()
            LOGGER.debug(
                f"group settings: {json.dumps(group_settings_json, indent=4,)}"
            )

        if "project_settings" in config:
            project_settings = ProjectSettings(**config["project_settings"])
            project_settings_json = project_settings.to_api_json()
            LOGGER.debug(
                f"project settings: {json.dumps(project_settings_json, indent=4,)}"
            )

        if not id:
            id = self.gl.get_entity_id_from_url(
                entity_path=path,  # pyright: ignore[reportArgumentType]
                entity_type=path_type,
            )

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

        for group_id in groups:
            self.gl.confugure_entity(
                group_id,  # pyright: ignore[reportArgumentType]
                "group",
                group_settings_json,  # pyright: ignore[reportPossiblyUnboundVariable]
            )

        for project_id in projects:
            self.gl.confugure_entity(
                project_id,  # pyright: ignore[reportArgumentType]
                "project",
                project_settings_json,  # pyright: ignore[reportPossiblyUnboundVariable]
            )
