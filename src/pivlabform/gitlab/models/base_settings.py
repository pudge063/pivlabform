from enum import Enum
from typing import Optional

import typing_extensions
from pydantic import BaseModel, ConfigDict, Field


class Visibility(str, Enum):
    PRIVATE = "private"
    INTERNAL = "internal"
    PUBLIC = "public"


class AccessLevel(str, Enum):
    DISABLED = "disabled"
    PRIVATE = "private"
    ENABLED = "enabled"
    PUBLIC = "public"


class BaseSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    default_branch: Optional[str] = None
    lfs_enabled: Optional[bool] = None

    max_artifacts_size: Optional[int] = Field(None, ge=0)
    web_based_commit_signing_enabled: Optional[bool] = None
    only_allow_merge_if_pipeline_succeeds: Optional[bool] = None
    allow_merge_on_skipped_pipeline: Optional[bool] = None
    only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None
    request_access_enabled: Optional[bool] = None
    auto_devops_enabled: Optional[bool] = None
    visibility: Optional[Visibility] = None
    description: Optional[str] = None

    wiki_access_level: Optional[AccessLevel] = None

    def to_api_json(
        self: typing_extensions.Self,
        exclude_none: bool = True,
    ) -> dict[str, typing_extensions.Any]:
        data = self.model_dump(
            exclude_none=exclude_none,
            mode="json",
            by_alias=False,
        )

        return data
