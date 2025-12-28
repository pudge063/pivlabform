from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .base_settings import BaseSettings


class Visibility(str, Enum):
    PRIVATE = "private"
    INTERNAL = "internal"
    PUBLIC = "public"


class MergeMethod(str, Enum):
    MERGE = "merge"
    REBASE_MERGE = "rebase_merge"
    FF = "ff"


class SquashOption(str, Enum):
    ALWAYS = "always"
    NEVER = "never"
    DEFAULT_ON = "default_on"
    DEFAULT_OFF = "default_off"


class AccessLevel(str, Enum):
    DISABLED = "disabled"
    PRIVATE = "private"
    ENABLED = "enabled"
    PUBLIC = "public"


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


class ProjectSettings(BaseSettings):
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
    ci_id_token_sub_claim_components: Optional[List[str]] = None
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
    topics: Optional[List[str]] = None

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
