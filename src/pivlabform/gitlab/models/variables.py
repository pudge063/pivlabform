from enum import Enum
from typing import List, Optional

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

    def to_api_json(
        self,
        exclude_none: bool = True,
    ) -> dict[str, typing_extensions.Any]:
        data = self.model_dump(
            exclude_none=exclude_none,
            mode="json",
            by_alias=False,
        )
        return data


class Variables(BaseModel):
    variables: dict[str, Variable]

    def to_api_variables(self) -> List[dict[str, typing_extensions.Any]]:
        result: list[dict[str, typing_extensions.Any]] = []

        for var_name, var_obj in self.variables.items():
            var_data = var_obj.model_dump(exclude_none=True)

            if "key" not in var_data or not var_data["key"]:
                var_data["key"] = var_name.upper()

            if "value" not in var_data:
                continue

            result.append(var_data)

        return result
