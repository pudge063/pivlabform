from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re

from .variables import Variable
from .protected_branches import ProtectedBranch


class Visibility(str, Enum):
    PRIVATE = "private"
    INTERNAL = "internal"
    PUBLIC = "public"


class AccessLevel(str, Enum):
    DISABLED = "disabled"
    PRIVATE = "private"
    ENABLED = "enabled"
    PUBLIC = "public"


class EntirySettings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    default_branch: Optional[str] = None
    lfs_enabled: Optional[bool] = None
    description: Optional[str] = None
    visibility: Optional[Visibility] = None
    auto_devops_enabled: Optional[bool] = None
    max_artifacts_size: Optional[int] = Field(None, ge=0)
    web_based_commit_signing_enabled: Optional[bool] = None
    only_allow_merge_if_pipeline_succeeds: Optional[bool] = None
    allow_merge_on_skipped_pipeline: Optional[bool] = None
    only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None
    request_access_enabled: Optional[bool] = None

    wiki_access_level: Optional[AccessLevel] = None

    @field_validator("default_branch")
    @classmethod
    def validate_default_branch(cls, v: str):
        if v and not re.match(r"^[a-zA-Z0-9_\-./]+$", v):
            raise ValueError("Invalid branch name")
        return v


class SharedRunnersSetting(str, Enum):
    DISABLED_AND_UNOVERRIDABLE = "disabled_and_unoverridable"
    DISABLED_AND_OVERRIDABLE = "disabled_and_overridable"
    ENABLED = "enabled"
    # DISABLED_WITH_OVERRIDE = "disabled_with_override"


class GroupSettings(EntirySettings):
    model_config = ConfigDict(extra="ignore")

    # security
    default_branch_protection: Optional[int] = None
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

    shared_runners_setting: Optional[SharedRunnersSetting] = None
    extra_shared_runners_minutes_limit: Optional[int] = Field(None, ge=0)  # locked
    shared_runners_minutes_limit: Optional[int] = Field(None, ge=0)  # locked

    enabled_git_access_protocol: Optional[str] = None
    emails_disabled: Optional[bool] = None
    mentions_disabled: Optional[bool] = None
    step_up_auth_required_oauth_provider: Optional[str] = None


class GroupConfig(BaseModel):
    settings: Optional[GroupSettings] = None
    variables: Optional[dict[str, Variable]] = None


class MergeMethod(str, Enum):
    MERGE = "merge"
    REBASE_MERGE = "rebase_merge"
    FF = "ff"


class SquashOption(str, Enum):
    ALWAYS = "always"
    NEVER = "never"
    DEFAULT_ON = "default_on"
    DEFAULT_OFF = "default_off"


class AutoDevopsDeployStrategy(str, Enum):
    CONTINUOUS = "continuous"
    MANUAL = "manual"
    TIMED_INCREMENTAL = "timed_incremental"


class BuildGitStrategy(str, Enum):
    FETCH = "fetch"
    CLONE = "clone"


class ContainerExpirationPolicy(BaseModel):
    cadence: Optional[str] = None
    enabled: Optional[bool] = None
    keep_n: Optional[int] = None
    older_than: Optional[str] = None
    name_regex: Optional[str] = None
    name_regex_keep: Optional[str] = None


class ProjectSettings(EntirySettings):
    model_config = ConfigDict(extra="ignore")

    # Merge Request settings
    allow_pipeline_trigger_approve_deployment: Optional[bool] = None
    only_allow_merge_if_all_status_checks_passed: Optional[bool] = None
    approvals_before_merge: Optional[int] = Field(None, ge=0)
    remove_source_branch_after_merge: Optional[bool] = None
    mr_default_target_self: Optional[bool] = None
    squash_option: Optional[SquashOption] = None

    # Pipeline settings
    auto_cancel_pending_pipelines: Optional[str] = None
    auto_devops_deploy_strategy: Optional[AutoDevopsDeployStrategy] = None
    ci_config_path: Optional[str] = None
    ci_default_git_depth: Optional[int] = Field(None, ge=0)
    ci_delete_pipelines_in_seconds: Optional[int] = Field(None, ge=0)
    ci_forward_deployment_enabled: Optional[bool] = None
    ci_forward_deployment_rollback_allowed: Optional[bool] = None
    ci_allow_fork_pipelines_to_run_in_parent_project: Optional[bool] = None
    ci_id_token_sub_claim_components: Optional[list[str]] = None
    ci_separated_caches: Optional[bool] = None
    ci_restrict_pipeline_cancellation_role: Optional[str] = None
    ci_pipeline_variables_minimum_override_role: Optional[str] = None
    ci_push_repository_for_job_token_allowed: Optional[bool] = None
    merge_pipelines_enabled: Optional[bool] = None
    merge_trains_enabled: Optional[bool] = None
    merge_trains_skip_train_allowed: Optional[bool] = None

    # Code Review
    auto_duo_code_review_enabled: Optional[bool] = None
    duo_remote_flows_enabled: Optional[bool] = None

    # Build settings
    build_git_strategy: Optional[BuildGitStrategy] = None
    build_timeout: Optional[int] = Field(None, ge=0)
    jobs_enabled: Optional[bool] = None
    public_jobs: Optional[bool] = None
    shared_runners_enabled: Optional[bool] = None
    group_runners_enabled: Optional[bool] = None
    keep_latest_artifact: Optional[bool] = None

    # Repository settings
    repository_storage: Optional[str] = None
    suggestion_commit_message: Optional[str] = None
    issue_branch_template: Optional[str] = None
    merge_commit_template: Optional[str] = None
    squash_commit_template: Optional[str] = None
    issues_template: Optional[str] = None
    warn_about_potentially_unwanted_characters: Optional[bool] = None

    # Merge settings
    merge_method: Optional[MergeMethod] = None
    merge_requests_enabled: Optional[bool] = None

    # Container Registry
    container_registry_enabled: Optional[bool] = None
    container_expiration_policy_attributes: Optional[ContainerExpirationPolicy] = None

    # Packages
    packages_enabled: Optional[bool] = None
    package_registry_access_level: Optional[AccessLevel] = None

    # Mirroring
    mirror: Optional[bool] = None
    mirror_overwrites_diverged_branches: Optional[bool] = None
    mirror_trigger_builds: Optional[bool] = None
    mirror_user_id: Optional[int] = None
    only_mirror_protected_branches: Optional[bool] = None

    # Issues
    autoclose_referenced_issues: Optional[bool] = None
    external_authorization_classification_label: Optional[str] = None

    # Security & Compliance
    enforce_auth_checks_on_uploads: Optional[bool] = None
    prevent_merge_without_jira_issue: Optional[bool] = None
    restrict_user_defined_variables: Optional[bool] = None
    resolve_outdated_diff_discussions: Optional[bool] = None

    # Service Desk & Emails
    service_desk_enabled: Optional[bool] = None
    emails_enabled: Optional[bool] = None

    # Import/Export
    import_url: Optional[str] = None

    # UI/UX
    printing_merge_request_link_enabled: Optional[bool] = None
    show_default_award_emojis: Optional[bool] = None
    snippets_enabled: Optional[bool] = None

    # Topics
    topics: Optional[list[str]] = None

    # SPP (Special Pipeline Permissions)
    spp_repository_pipeline_access: Optional[bool] = None

    # Access Levels
    analytics_access_level: Optional[AccessLevel] = None
    builds_access_level: Optional[AccessLevel] = None
    container_registry_access_level: Optional[AccessLevel] = None
    environments_access_level: Optional[AccessLevel] = None
    feature_flags_access_level: Optional[AccessLevel] = None
    forking_access_level: Optional[AccessLevel] = None
    infrastructure_access_level: Optional[AccessLevel] = None
    issues_access_level: Optional[AccessLevel] = None
    merge_requests_access_level: Optional[AccessLevel] = None
    model_experiments_access_level: Optional[AccessLevel] = None
    model_registry_access_level: Optional[AccessLevel] = None
    monitor_access_level: Optional[AccessLevel] = None
    pages_access_level: Optional[AccessLevel] = None
    releases_access_level: Optional[AccessLevel] = None
    repository_access_level: Optional[AccessLevel] = None
    requirements_access_level: Optional[AccessLevel] = None
    security_and_compliance_access_level: Optional[AccessLevel] = None
    snippets_access_level: Optional[AccessLevel] = None


class ProjectConfig(EntirySettings):
    settings: Optional[ProjectSettings] = None
    variables: Optional[dict[str, Variable]] = None
    protected_branches: Optional[dict[str, Optional[ProtectedBranch]]] = Field(
        default_factory=dict
    )
