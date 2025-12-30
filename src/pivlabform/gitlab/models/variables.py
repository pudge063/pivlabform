import re
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Optional

# from typing_extensions import Hashable


class VariableType(str, Enum):
    ENV_VAR = "env_var"
    FILE = "file"


class Variable(BaseModel):
    key: str = Field(
        ...,
        min_length=1,
        max_length=255,
        pattern=r"^[A-Za-z0-9_]+$",
        description="The key of a variable; must have no more than 255 characters; "
        "only A-Z, a-z, 0-9, and _ are allowed",
    )
    "The key of a variable; must have no more than 255 characters; only A-Z, a-z, 0-9, and _ are allowed"

    value: Optional[str] = None
    "The value of a variable"

    description: Optional[str] = None
    "The description of the variable. Default: null. Introduced in GitLab 16.2."

    environment_scope: Optional[str] = None
    "The environment_scope of the variable. Default: *"

    masked: Optional[bool] = None
    "Whether the variable is masked. Default: false"

    # masked_and_hidden: Optional[bool] = None
    # DISABLED
    "Whether the variable is masked and hidden. Default: false"

    protected: Optional[bool] = None
    "Whether the variable is protected."

    # filter: Optional[Hashable] = None
    # DISABLED
    "Filters results when multiple variables share the same key. Possible values: [environment_scope]."
    "Premium and Ultimate only."

    raw: Optional[bool] = None
    "If true, indicates the variable is treated as a raw string. When false, the variable value is expanded."
    "Default: true."

    variable_type: Optional[VariableType] = VariableType.ENV_VAR
    "https://gitlab.com/gitlab-org/gitlab/-/blob/master/spec/fixtures/api/schemas/variable.json"

    @field_validator("key")
    @classmethod
    def validate_key_format(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("Key cannot be empty")

        if len(v) > 255:
            raise ValueError(f"Key length cannot exceed 255 characters. Got {len(v)}")

        if not re.fullmatch(r"^[A-Za-z0-9_]+$", v):
            raise ValueError(
                "Key can only contain letters A-Z, a-z, digits 0-9, and underscore _"
            )

        reserved_keys = {"CI", "GITLAB", "KUBERNETES"}
        if v.upper() in reserved_keys:
            raise ValueError(f"Key '{v}' is reserved")

        return v
