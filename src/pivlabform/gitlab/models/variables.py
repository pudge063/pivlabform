from enum import Enum
from typing import Optional

import typing_extensions
from pydantic import BaseModel, Field


class VariableType(str, Enum):
    ENV_VAR = "env_var"
    FILE = "file"


class Variable(BaseModel):
    key: str = Field(..., min_length=1, max_length=255)
    value: str = Field(..., min_length=0, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    environment_scope: Optional[str] = None
    filter: Optional[typing_extensions.Hashable] = None
    masked: Optional[bool] = None
    protected: Optional[bool] = None
    raw: Optional[bool] = None
    variable_type: Optional[VariableType] = VariableType.ENV_VAR
    "https://gitlab.com/gitlab-org/gitlab/-/blob/master/spec/fixtures/api/schemas/variable.json"
