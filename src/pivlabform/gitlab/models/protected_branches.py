from enum import Enum

from pydantic import BaseModel, ConfigDict
from typing_extensions import Optional


class AccessLevelEnum(int, Enum):
    NO_ACCESS = 0
    MINIMAL_ACCESS = 5
    GUEST = 10
    REPORTER = 20
    DEVELOPER = 30
    MAINTAINER = 40
    OWNER = 50


class ProtectedBranch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # name: str = Field(..., min_length=2, max_length=255)

    # fields for Premium and Ultimate only
    # TODO: not supports multy access configuration
    # allowed_to_merge: Optional[list[dict[str, typing_extensions.Any]]] = None
    # allowed_to_push: Optional[list[dict[str, typing_extensions.Any]]] = None
    # allowed_to_unprotect: Optional[list[dict[str, typing_extensions.Any]]] = None
    # code_owner_approval_required: Optional[bool] = None

    merge_access_level: Optional[AccessLevelEnum] = None
    "Access levels allowed to merge. Default is 40 (Maintainer role)."

    push_access_level: Optional[AccessLevelEnum] = None
    "Access levels allowed to push. Default is 40 (Maintainer role)."

    unprotect_access_level: Optional[AccessLevelEnum] = None
    "Access levels allowed to unprotect. Default is 40 (Maintainer role)."

    allow_force_push: Optional[bool] = None
    "If true, force push is allowed on this branch."
