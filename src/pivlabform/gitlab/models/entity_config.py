from abc import ABC

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Optional

from .entity_settings import GroupSettings, ProjectSettings
from .protected_branches import ProtectedBranch
from .variables import Variable


class EntityConfig(BaseModel, ABC):
    model_config = ConfigDict(extra="forbid")

    variables: Optional[dict[str, Variable]] = None
    "https://docs.gitlab.com/api/project_level_variables/#update-a-variable"


class GroupConfig(EntityConfig):
    settings: Optional[GroupSettings] = None
    "https://docs.gitlab.com/api/groups/#update-group-attributes"


class ProjectConfig(EntityConfig):
    settings: Optional[ProjectSettings] = None
    "https://docs.gitlab.com/api/projects/#edit-a-project"

    protected_branches: Optional[dict[str, Optional[ProtectedBranch]]] = Field(
        default_factory=dict
    )
    "https://docs.gitlab.com/api/protected_branches/"
