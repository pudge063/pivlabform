import os
from typing_extensions import Optional

os.environ["IGNORE_REQUESTS_ERRORS"] = "true"
os.environ["DEBUG"] = "true"
os.environ["CI_SERVER_HOST"] = "pivlab.space"

from pivlabform import LOGGER, GitLab
from pivlabform.gitlab.gitlab import Entity
from pivlabform.gitlab.models import CreateGroupSettings, CreateProjectSettings
from pivlabform.gitlab.models.entity_settings import MergeMethod


GL = GitLab("https://pivlab.space")


def create_group(name: str, path: str, target_group: str):

    target_group_id = GL.get_entity_id_from_url(
        entity_path=target_group,
        entity_type=Entity.GROUP,
    )

    create_group_model = CreateGroupSettings(
        name=name,
        path=path,
        parent_id=target_group_id,
    )

    group_id = GL.create_entity(
        Entity.GROUP,
        create_group_model.to_api_json(),
    )

    LOGGER.warning(f"group created with id: {group_id}")

    return group_id


def create_project(name: Optional[str], namespace_id: int, path: Optional[str] = None):
    create_project_settings = CreateProjectSettings(
        name=name,
        path=path,
        namespace_id=namespace_id,
        allow_merge_on_skipped_pipeline=True,
        only_allow_merge_if_pipeline_succeeds=True,
        only_allow_merge_if_all_discussions_are_resolved=True,
        merge_method=MergeMethod.FF,
        merge_commit_template="""
TItle: %{title}
Merge branch '%{source_branch}' into '%{target_branch}
Description: %{description}
Linked issues: %{issues}
Approved by: %{approved_by}
""",
    )

    project_id = GL.create_entity(
        entity_type=Entity.PROJECT,
        entity_settings=create_project_settings.to_api_json(),
    )

    LOGGER.warning(f"project created with id: {project_id}")


target_group = "sandbox/pivlabform-tests"
group_name = group_path = "test-group-123"
projects = [
    "test-222",
    # "dev-2",
    # "example-3",
]

# group_id = create_group(
#     name=group_name,
#     path=group_path,
#     target_group=target_group,
# )
group_id = 3444

for project in projects:
    create_project(
        name=project,
        namespace_id=group_id,
    )
