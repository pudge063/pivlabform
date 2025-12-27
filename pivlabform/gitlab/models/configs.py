from . import ProjectSettings, GroupSettings
from pydantic import BaseModel
from typing_extensions import Dict


class ProjectConfig(BaseModel):
    projects: dict[str, ProjectSettings]


class GroupConfig(BaseModel):
    recursive: bool = False
    group_settings: GroupSettings
    project_settings: ProjectSettings


class GroupsConfig(BaseModel):
    groups: Dict[str, GroupConfig]
