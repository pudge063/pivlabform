from pydantic import BaseModel, ConfigDict
from typing_extensions import Optional
import typing_extensions

from .project import ProjectConfig
from .group import GroupConfig

# from ..._logger import LOGGER
# import json


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    project_config: Optional[ProjectConfig] = None
    group_config: Optional[GroupConfig] = None

    groups: Optional[list[str | int]] = None
    projects: Optional[list[str | int]] = None

    def dump_model_to_json(self) -> dict[str, typing_extensions.Any]:
        return self.model_dump(exclude_none=True)
