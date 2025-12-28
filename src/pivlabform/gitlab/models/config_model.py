import typing_extensions
from pydantic import BaseModel, ConfigDict
from typing_extensions import Optional

from .entiry_settings import GroupConfig, ProjectConfig


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    group_config: Optional[GroupConfig] = None
    project_config: Optional[ProjectConfig] = None

    groups: Optional[list[str | int]] = None
    projects: Optional[list[str | int]] = None

    def dump_model_to_json(self) -> dict[str, typing_extensions.Any]:
        return self.model_dump(exclude_none=True)
