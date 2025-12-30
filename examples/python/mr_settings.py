import os

os.environ["DEBUG"] = "true"
os.environ["CI_SERVER_HOST"] = "pivlab.space"

from pivlabform import LOGGER, GitLab
from pivlabform.gitlab.gitlab import Entity
from pivlabform.gitlab.models import GroupSettings, ProjectSettings
from pivlabform.gitlab.models.entity_settings import MergeMethod


def configure_projects_in_group(group: str) -> None:
    """
    Procedure for confugure all projects in group with settings:
        - default_branch: master
        - description: configuration from test_api.py
        - for merge needs resolve all discussions and pipeline success
        - merge strategy: fast-forward

    :param group: target group path
    :type group: str
    """
    gl = GitLab()

    project_settings_model = ProjectSettings(
        default_branch="master",
        description="configuration from test_api.py",
        only_allow_merge_if_all_discussions_are_resolved=True,
        only_allow_merge_if_pipeline_succeeds=True,
        merge_method=MergeMethod.FF,
    )

    group_settings_model = GroupSettings(
        default_branch="master",
    )

    group_id = gl.get_entity_id_from_url(group, Entity.GROUP)
    groups = gl.get_all_groups_recursive(group_id)
    projects = gl.get_all_projects_recursive(group_id)

    LOGGER.info(f"projects for config: {projects}")
    LOGGER.info(f"groups for config: {groups}")

    for group_id in groups:
        gl.confugure_entity(
            entity_id=group_id,
            entity_type=Entity.GROUP,
            config=group_settings_model.to_api_json(),
        )

    for project_id in projects:
        gl.confugure_entity(
            entity_id=project_id,
            entity_type=Entity.PROJECT,
            config=project_settings_model.to_api_json(),
        )


if __name__ == "__main__":
    configure_projects_in_group("sandbox/pivlabform-tests")
