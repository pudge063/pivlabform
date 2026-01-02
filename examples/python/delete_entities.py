import os

os.environ["IGNORE_REQUESTS_ERRORS"] = "true"
os.environ["DEBUG"] = "true"
os.environ["CI_SERVER_HOST"] = "pivlab.space"

from pivlabform import LOGGER, GitLab
from pivlabform.gitlab.gitlab import Entity

GL = GitLab("https://pivlab.space")


def archive_entity(
    group_path: str,
    entity_type: Entity,
):

    entity = GL.get_entity_id_from_url(
        entity_path=group_path,
        entity_type=entity_type,
    )

    GL.archive_entity(
        entity_id=entity,
        entity_type=entity_type,
        archive=True,
    )

    LOGGER.warning(f"{entity_type.lname} with id: {entity} archived")


def delete_project(project_path: str):
    project_id = GL.get_entity_id_from_url(
        entity_path=project_path,
        entity_type=Entity.PROJECT,
    )

    LOGGER.warning(project_id)

    GL.delete_entity(
        entity_id=project_id,
        entity_type=Entity.PROJECT,
    )

    LOGGER.warning(f"project {project_path} with id: {project_id} removed")


target_group = "sandbox/pivlabform-tests"
group_name = "test-group-123"
projects = [
    "test-222",
    # "dev-2",
    # "example-3",
]

for project in projects:
    delete_project(project_path=f"{target_group}/{group_name}/{project}")

# archive_entity(
#     group_path=f"{target_group}/{group_name}/test",
#     entity_type=Entity.PROJECT,
# )
