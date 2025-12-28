from enum import Enum
from typing import Optional

from pydantic import ConfigDict, Field

from .base_settings import BaseSettings


class SharedRunnersSetting(str, Enum):
    DISABLED = "disabled_and_unoverridable"
    ENABLED = "enabled"


class GroupSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    # security
    require_two_factor_authentication: Optional[bool] = None
    two_factor_grace_period: Optional[int] = Field(None, ge=0)
    ip_restriction_ranges: Optional[str] = None
    allowed_email_domains_list: Optional[str] = None
    duo_availability: Optional[str] = None
    duo_features_enabled: Optional[str] = None  # locked
    lock_duo_features_enabled: Optional[str] = None  # locked

    # repository
    file_template_project_id: Optional[str] = None  # locked

    # access control
    membership_lock: Optional[bool] = None  # locked
    prevent_sharing_groups_outside_hierarchy: Optional[bool] = None
    prevent_forking_outside_group: Optional[bool] = None  # locked
    share_with_group_lock: Optional[bool] = None
    subgroup_creation_level: Optional[str] = None
    project_creation_level: Optional[str] = None

    # complience
    unique_project_download_limit: Optional[int] = Field(None, ge=0)
    unique_project_download_limit_interval_in_seconds: Optional[int] = Field(None, ge=0)
    unique_project_download_limit_allowlist: Optional[str] = None
    unique_project_download_limit_alertlist: Optional[str] = None
    auto_ban_user_on_excessive_projects_download: Optional[bool] = None

    # experemental settings
    experiment_features_enabled: Optional[bool] = None
    math_rendering_limits_enabled: Optional[bool] = None
    lock_math_rendering_limits_enabled: Optional[bool] = None

    shared_runners_setting: SharedRunnersSetting = SharedRunnersSetting.DISABLED
    extra_shared_runners_minutes_limit: Optional[int] = Field(None, ge=0)  # locked
    shared_runners_minutes_limit: Optional[int] = Field(None, ge=0)  # locked

    enabled_git_access_protocol: Optional[str] = None
    emails_disabled: Optional[bool] = None
    mentions_disabled: Optional[bool] = None
    step_up_auth_required_oauth_provider: Optional[str] = None
