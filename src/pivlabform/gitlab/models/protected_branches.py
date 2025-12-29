from enum import Enum

from pydantic import BaseModel
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
    # name: str = Field(..., min_length=2, max_length=255)

    # TODO: fields for Premium and Ultimate only
    # FIXME: not supports multy access
    # allowed_to_merge: Optional[list[dict[str, typing_extensions.Any]]] = None
    # allowed_to_push: Optional[list[dict[str, typing_extensions.Any]]] = None
    # allowed_to_unprotect: Optional[list[dict[str, typing_extensions.Any]]] = None
    # code_owner_approval_required: Optional[bool] = None

    merge_access_level: Optional[AccessLevelEnum] = None
    push_access_level: Optional[AccessLevelEnum] = None
    unprotect_access_level: Optional[AccessLevelEnum] = None
    allow_force_push: Optional[bool] = None
