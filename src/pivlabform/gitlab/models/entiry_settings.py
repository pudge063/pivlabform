import re
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Hashable, Optional

from .protected_branches import ProtectedBranch
from .variables import Variable


class Visibility(str, Enum):
    PRIVATE = "private"
    INTERNAL = "internal"
    PUBLIC = "public"


class AccessLevel(str, Enum):
    DISABLED = "disabled"
    PRIVATE = "private"
    ENABLED = "enabled"
    PUBLIC = "public"


class EntitySettings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    default_branch: Optional[str] = None
    "The default branch name. Requires initialize_with_readme to be true."

    lfs_enabled: Optional[bool] = None
    "Enable LFS."

    description: Optional[str] = None
    "Short project description."

    visibility: Optional[Visibility] = None
    "https://docs.gitlab.com/api/projects/#project-visibility-level"

    auto_devops_enabled: Optional[bool] = None
    "Enable Auto DevOps for this project or group."

    max_artifacts_size: Optional[int] = Field(None, ge=0)
    "The maximum file size in megabytes for individual job artifacts."

    web_based_commit_signing_enabled: Optional[bool] = None
    "Enables web-based commit signing for commits created from the GitLab UI."
    "Available only on GitLab SaaS."

    only_allow_merge_if_pipeline_succeeds: Optional[bool] = None
    "Set whether merge requests can only be merged with successful jobs."

    allow_merge_on_skipped_pipeline: Optional[bool] = None
    "Set whether or not merge requests can be merged with skipped jobs."

    only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None
    "Set whether merge requests can only be merged when all the discussions are resolved."

    request_access_enabled: Optional[bool] = None
    "Allow users to request member access."

    wiki_access_level: Optional[AccessLevel] = None
    "Set visibility of wiki. https://docs.gitlab.com/user/project/wiki/#enable-or-disable-a-project-wiki"

    @field_validator("default_branch")
    @classmethod
    def validate_default_branch(cls, v: str):
        if v and not re.match(r"^[a-zA-Z0-9_\-./]+$", v):
            raise ValueError("Invalid branch name")
        return v


class DuoAvailability(str, Enum):
    DEFAULT_ON = "default_on"
    DEFAULT_OFF = "default_off"
    NEVER_ON = "never_on"


class CreationLevels(str, Enum):
    ADMINISTRATOR = "administrator"
    NOONE = "noone"
    MAINTAINER = "maintainer"
    DEVELOPER = "developer"


class SharedRunnersSetting(str, Enum):
    DISABLED_AND_UNOVERRIDABLE = "disabled_and_unoverridable"
    DISABLED_AND_OVERRIDABLE = "disabled_and_overridable"
    ENABLED = "enabled"
    # DISABLED_WITH_OVERRIDE = "disabled_with_override"


class GroupSettings(EntitySettings):
    model_config = ConfigDict(extra="ignore")

    # security
    default_branch_protection: Optional[int] = None
    "Deprecated in GitLab 17.0. Use default_branch_protection_defaults instead."

    default_branch_protection_defaults: Optional[Hashable] = None
    "Introduced in GitLab 17.0. For available options, see Options for default_branch_protection_defaults."

    two_factor_grace_period: Optional[int] = Field(None, ge=0)
    "Time before Two-factor authentication is enforced (in hours)."

    ip_restriction_ranges: Optional[str] = None
    "Comma-separated list of IP addresses or subnet masks to restrict group access."
    "Premium and Ultimate only."

    duo_availability: Optional[DuoAvailability] = None
    "GitLab Duo availability setting."
    "Valid values are: default_on, default_off, never_on."
    "Note: In the UI, never_on is displayed as “Always Off”."

    duo_features_enabled: Optional[bool] = None
    "Indicates whether GitLab Duo features are enabled for this group."
    "Introduced in GitLab 16.10. GitLab Self-Managed, Premium and Ultimate only."

    lock_duo_features_enabled: Optional[bool] = None
    "Indicates whether the GitLab Duo features enabled setting is enforced for all subgroups."
    "Introduced in GitLab 16.10. GitLab Self-Managed, Premium and Ultimate only."

    # access control
    membership_lock: Optional[bool] = None
    "Users cannot be added to projects in this group."
    "Premium and Ultimate only."

    prevent_sharing_groups_outside_hierarchy: Optional[bool] = None
    "See Prevent group sharing outside the group hierarchy. This attribute is only available on top-level groups."
    "https://docs.gitlab.com/user/project/members/sharing_projects_groups/#prevent-inviting-groups-outside-the-group-hierarchy"

    prevent_forking_outside_group: Optional[bool] = None
    "When enabled, users can not fork projects from this group to external namespaces. Premium and Ultimate only."

    share_with_group_lock: Optional[bool] = None
    "Prevent sharing a project with another group within this group."

    subgroup_creation_level: Optional[str] = None
    "Allowed to create subgroups. Can be owner (users with the Owner role), or maintainer (users with the Maintainer role)."
    "https://docs.gitlab.com/user/group/subgroups/#create-a-subgroup"

    project_creation_level: Optional[CreationLevels] = None
    "Determine if developers can create projects in the group."
    """Can be
        administrator (users with Admin Mode enabled),
        noone (No one),
        maintainer (users with the Maintainer role),
        or developer (users with the Developer or Maintainer role).
    """

    # complience
    shared_runners_setting: Optional[SharedRunnersSetting] = None
    "See Options for shared_runners_setting. Enable or disable instance runners for a group’s subgroups and projects."

    extra_shared_runners_minutes_limit: Optional[int] = Field(None, ge=0)
    "Can be set by administrators only. Additional compute minutes for this group."
    "GitLab Self-Managed, Premium and Ultimate only."

    shared_runners_minutes_limit: Optional[int] = Field(None, ge=0)
    "Can be set by administrators only. Maximum number of monthly compute minutes for this group."
    "Can be nil (default; inherit system default), 0 (unlimited), or > 0."
    "GitLab Self-Managed, Premium and Ultimate only."

    enabled_git_access_protocol: Optional[str] = None
    "Enabled protocols for Git access. Allowed values are: ssh, http, and all to allow both protocols. Introduced in GitLab 16.9."

    emails_disabled: Optional[bool] = None
    "(Deprecated in GitLab 16.5.) Disable email notifications. Use emails_enabled instead."

    emails_enabled: Optional[bool] = None
    "Enable email notifications."

    mentions_disabled: Optional[bool] = None
    "Disable the capability of a group from getting mentioned."

    step_up_auth_required_oauth_provider: Optional[str] = None
    "OAuth provider required for step-up authentication. Pass empty string to disable. Introduced in GitLab 18.4."
    "Available when omniauth_step_up_auth_for_namespace feature flag is enabled."

    # TOP-LEVEL GROUPS ONLY

    file_template_project_id: Optional[int] = None
    "The ID of a project to load custom file templates from."
    "Premium and Ultimate only."

    require_two_factor_authentication: Optional[bool] = None
    "Require all users in this group to set up two-factor authentication."

    allowed_email_domains_list: Optional[str] = None
    "Comma-separated list of email address domains to allow group access."
    "Introduced in 17.4. GitLab Premium and Ultimate only."

    unique_project_download_limit: Optional[int] = Field(None, ge=0)
    "Maximum number of unique projects a user can download in the specified time period before they are banned."
    "Available only on top-level groups. Default: 0, Maximum: 10,000. Ultimate only."

    unique_project_download_limit_interval_in_seconds: Optional[int] = Field(None, ge=0)
    "Time period during which a user can download a maximum amount of projects before they are banned."
    "Available only on top-level groups. Default: 0, Maximum: 864,000 seconds (10 days). Ultimate only."

    unique_project_download_limit_allowlist: Optional[list[str]] = None
    "List of usernames excluded from the unique project download limit."
    "Available only on top-level groups. Default: [], Maximum: 100 usernames. Ultimate only."

    unique_project_download_limit_alertlist: Optional[list[str]] = None
    "List of user IDs that are emailed when the unique project download limit is exceeded."
    "Available only on top-level groups. Default: [], Maximum: 100 user IDs. Ultimate only."

    auto_ban_user_on_excessive_projects_download: Optional[bool] = None
    "When enabled, users are automatically banned from the group when they download more than the maximum number"
    "of unique projects specified by unique_project_download_limit and unique_project_download_limit_interval_in_seconds."
    "Ultimate only."

    # experemental settings
    experiment_features_enabled: Optional[bool] = None
    "Enable experiment features for this group."

    math_rendering_limits_enabled: Optional[bool] = None
    "Indicates if math rendering limits are used for this group."

    lock_math_rendering_limits_enabled: Optional[bool] = None
    "Indicates if math rendering limits are locked for all descendent groups."


class GroupConfig(BaseModel):
    settings: Optional[GroupSettings] = None
    variables: Optional[dict[str, Variable]] = None
    protected_branches: Optional[dict[str, Optional[ProtectedBranch]]] = Field(
        default_factory=dict
    )


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


class PipelineCancellationRole(str, Enum):
    DEVELOPER = "developer"
    MAINTAINER = "maintainer"
    NO_ONE = "no_one"
    OWNER = "owner"
    NO_ONE_ALLOWED = "no_one_allowed"


class ProjectSettings(EntitySettings):
    model_config = ConfigDict(extra="ignore")

    # Merge Request settings
    allow_pipeline_trigger_approve_deployment: Optional[bool] = None
    "Set whether or not a pipeline triggerer is allowed to approve deployments."
    "Premium and Ultimate only."

    only_allow_merge_if_all_status_checks_passed: Optional[bool] = None
    "Indicates that merges of merge requests should be blocked unless all status checks have passed. Defaults to false."
    "Introduced in GitLab 15.5 with feature flag only_allow_merge_if_all_status_checks_passed disabled by default."
    "Ultimate only."

    approvals_before_merge: Optional[int] = Field(None, ge=0)
    "How many approvers should approve merge requests by default."
    "To configure approval rules, see Merge request approvals API."
    "Deprecated in GitLab 16.0. Premium and Ultimate only."

    remove_source_branch_after_merge: Optional[bool] = None
    "Enable Delete source branch option by default for all new merge requests."

    mr_default_target_self: Optional[bool] = None
    "For forked projects, target merge requests to this project. If false, the target is the upstream project."

    squash_option: Optional[SquashOption] = None
    "One of never, always, default_on, or default_off."

    # Pipeline settings
    auto_cancel_pending_pipelines: Optional[str | bool] = None
    "Auto-cancel pending pipelines. This action toggles between an enabled state and a disabled state; it is not a boolean."

    auto_devops_deploy_strategy: Optional[AutoDevopsDeployStrategy] = None
    "Auto Deploy strategy (continuous, manual or timed_incremental)."

    ci_config_path: Optional[str] = None
    "The path to CI configuration file."

    ci_default_git_depth: Optional[int] = Field(None, ge=0)
    "Default number of revisions for shallow cloning."
    "https://docs.gitlab.com/ci/pipelines/settings/#limit-the-number-of-changes-fetched-during-clone"

    ci_delete_pipelines_in_seconds: Optional[int] = Field(None, ge=0)
    "Pipelines older than the configured time are deleted."

    ci_forward_deployment_enabled: Optional[bool] = None
    "Enable or disable prevent outdated deployment jobs."
    "https://docs.gitlab.com/ci/pipelines/settings/#prevent-outdated-deployment-jobs"

    ci_forward_deployment_rollback_allowed: Optional[bool] = None
    "Enable or disable allow job retries for rollback deployments."
    "https://docs.gitlab.com/ci/pipelines/settings/#prevent-outdated-deployment-jobs"

    ci_allow_fork_pipelines_to_run_in_parent_project: Optional[bool] = None
    "Enable or disable running pipelines in the parent project for merge requests from forks. (Introduced in GitLab 15.3.)"
    "https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/#run-pipelines-in-the-parent-project"

    ci_id_token_sub_claim_components: Optional[list[str]] = None
    "Fields included in the sub claim of the ID Token. Accepts an array starting with project_path."
    "The array might also include ref_type, ref, environment_protected, and deployment_tier."
    "Defaults to ['project_path', 'ref_type', 'ref']. Introduced in GitLab 17.10."
    "Support for environment_protected and deployment_tier introduced in GitLab 18.7."

    ci_separated_caches: Optional[bool] = None
    "Set whether or not caches should be separated by branch protection status."
    "https://docs.gitlab.com/ci/caching/#cache-key-names"

    ci_restrict_pipeline_cancellation_role: Optional[PipelineCancellationRole] = None
    "Set the role required to cancel a pipeline or job. One of developer, maintainer, or no_one."
    "Introduced in GitLab 16.8. Premium and Ultimate only."
    "https://docs.gitlab.com/ci/pipelines/settings/#restrict-roles-that-can-cancel-pipelines-or-jobs"

    ci_pipeline_variables_minimum_override_role: Optional[PipelineCancellationRole] = (
        None
    )
    "You can specify which role can override variables. One of owner, maintainer, developer or no_one_allowed."
    "Introduced in GitLab 17.1. In GitLab 17.1 to 17.7, restrict_user_defined_variables must be enabled."

    ci_push_repository_for_job_token_allowed: Optional[bool] = None
    "Enable or disable the ability to push to the project repository using job token. Introduced in GitLab 17.2."

    merge_pipelines_enabled: Optional[bool] = None
    "Enable or disable merged results pipelines."

    merge_trains_enabled: Optional[bool] = None
    "Enable or disable merge trains."

    merge_trains_skip_train_allowed: Optional[bool] = None
    "Allows merge train merge requests to be merged without waiting for pipelines to finish."

    # Code Review
    auto_duo_code_review_enabled: Optional[bool] = None
    "Enable automatic reviews by GitLab Duo on merge requests. See GitLab Duo in merge requests. Ultimate only."
    "https://docs.gitlab.com/user/project/merge_requests/duo_in_merge_requests/#use-gitlab-duo-to-review-your-code"

    duo_remote_flows_enabled: Optional[bool] = None
    "Determine whether or not flows can run in your project."
    "https://docs.gitlab.com/user/duo_agent_platform/flows/"

    # Build settings
    build_git_strategy: Optional[BuildGitStrategy] = None
    "The Git strategy. Defaults to fetch."

    build_timeout: Optional[int] = Field(None, ge=0)
    "The maximum amount of time, in seconds, that a job can run."

    # jobs_enabled: Optional[bool] = None
    "(Deprecated) Enable jobs for this project. Use builds_access_level instead."

    public_jobs: Optional[bool] = None
    "If true, jobs can be viewed by non-project members."

    shared_runners_enabled: Optional[bool] = None
    "Enable instance runners for this project."

    group_runners_enabled: Optional[bool] = None
    "Enable group runners for this project."

    keep_latest_artifact: Optional[bool] = None
    "Disable or enable the ability to keep the latest artifact for this project."

    # Repository settings
    repository_storage: Optional[str] = None
    "Limit results to projects stored on repository_storage. (administrators only)"

    suggestion_commit_message: Optional[str] = None
    "The commit message used to apply merge request suggestions."
    "https://docs.gitlab.com/user/project/merge_requests/reviews/suggestions/"

    issue_branch_template: Optional[str] = None
    "Template used to suggest names for branches created from issues. (Introduced in GitLab 15.6.)"
    "https://docs.gitlab.com/user/project/merge_requests/creating_merge_requests/#from-an-issue"

    merge_commit_template: Optional[str] = None
    "Template used to create merge commit message in merge requests."
    "https://docs.gitlab.com/user/project/merge_requests/commit_templates/"

    squash_commit_template: Optional[str] = None
    "Template used to create squash commit message in merge requests."

    issues_template: Optional[str] = None
    "Default description for Issues. Description is parsed with GitLab Flavored Markdown."
    "See Templates for issues and merge requests."
    "Premium and Ultimate only."

    warn_about_potentially_unwanted_characters: Optional[bool] = None
    "Enable warnings about usage of potentially unwanted characters in this project."

    # Merge settings
    merge_method: Optional[MergeMethod] = None
    """Set the project’s merge method. Can be merge (merge commit), rebase_merge
    (merge commit with semi-linear history), or ff (fast-forward merge).
    https://docs.gitlab.com/user/project/merge_requests/methods/"""

    # merge_requests_enabled: Optional[bool] = None
    "(Deprecated) Enable merge requests for this project. Use merge_requests_access_level instead."

    # Container Registry
    container_registry_enabled: Optional[bool] = None
    "(Deprecated) Enable container registry for this project. Use container_registry_access_level instead."

    container_expiration_policy_attributes: Optional[ContainerExpirationPolicy] = None
    "Update the image cleanup policy for this project. Accepts: cadence (string), keep_n (integer), older_than"
    "(string), name_regex (string), name_regex_delete (string), name_regex_keep (string), enabled (boolean)."

    # Packages
    # packages_enabled: Optional[bool] = None
    "Deprecated in GitLab 17.10. Enable or disable packages repository feature. Use package_registry_access_level instead."

    # Mirroring
    mirror: Optional[bool] = None
    "Enables pull mirroring in a project. Premium and Ultimate only."

    mirror_overwrites_diverged_branches: Optional[bool] = None
    "Pull mirror overwrites diverged branches. Premium and Ultimate only."

    mirror_trigger_builds: Optional[bool] = None
    "Pull mirroring triggers builds. Premium and Ultimate only."

    mirror_user_id: Optional[int] = None
    "User responsible for all the activity surrounding a pull mirror event. (administrators only)"
    "Premium and Ultimate only."

    only_mirror_protected_branches: Optional[bool] = None
    "Only mirror protected branches. Premium and Ultimate only."

    # Issues
    autoclose_referenced_issues: Optional[bool] = None
    "Set whether auto-closing referenced issues on default branch."

    external_authorization_classification_label: Optional[str] = None
    "The classification label for the project. Premium and Ultimate only."

    # Security & Compliance
    enforce_auth_checks_on_uploads: Optional[bool] = None
    "Enforce auth checks on uploads."
    "https://docs.gitlab.com/security/user_file_uploads/#enable-authorization-checks-for-all-media-files"

    prevent_merge_without_jira_issue: Optional[bool] = None
    "Set whether merge requests require an associated issue from Jira. Ultimate only."

    restrict_user_defined_variables: Optional[bool] = None
    "(Deprecated in GitLab 17.7 in favour of ci_pipeline_variables_minimum_override_role)"
    "Allow only users with the Maintainer role to pass user-defined variables when triggering a pipeline."
    "For example when the pipeline is triggered in the UI, with the API, or by a trigger token."

    resolve_outdated_diff_discussions: Optional[bool] = None
    "Automatically resolve merge request diffs discussions on lines changed with a push."

    # Service Desk & Emails
    service_desk_enabled: Optional[bool] = None
    "Enable or disable Service Desk feature."

    emails_enabled: Optional[bool] = None
    "Enable email notifications."

    # Import/Export
    import_url: Optional[str] = None
    "URL to import repository from. When the URL value isn’t empty, you must not set initialize_with_readme to true."
    "Doing so might result in the following error: not a git repository."

    # UI/UX
    printing_merge_request_link_enabled: Optional[bool] = None
    "Show link to create/view merge request when pushing from the command line."

    show_default_award_emojis: Optional[bool] = None
    "Show default emoji reactions."

    # snippets_enabled: Optional[bool] = None
    "(Deprecated) Enable snippets for this project. Use snippets_access_level instead."

    # Topics
    topics: Optional[list[str]] = None
    "The list of topics for a project; put array of topics, that should be finally assigned to a project."

    # SPP (Special Pipeline Permissions)
    spp_repository_pipeline_access: Optional[bool] = None
    "Allow users and tokens read-only access to fetch security policy configurations from this project."
    "Required for enforcing security policies in projects that use this project as their security policy source."
    "Ultimate only."

    # Access Levels
    analytics_access_level: Optional[AccessLevel] = None
    "Set visibility of analytics."

    builds_access_level: Optional[AccessLevel] = None
    "Set visibility of pipelines."

    container_registry_access_level: Optional[AccessLevel] = None
    "Set visibility of container registry."

    environments_access_level: Optional[AccessLevel] = None
    "Set visibility of environments."

    feature_flags_access_level: Optional[AccessLevel] = None
    "Set visibility of feature flags."

    forking_access_level: Optional[AccessLevel] = None
    "Set visibility of forks."

    infrastructure_access_level: Optional[AccessLevel] = None
    "Set visibility of infrastructure management."

    issues_access_level: Optional[AccessLevel] = None
    "Set visibility of issues."

    merge_requests_access_level: Optional[AccessLevel] = None
    "Set visibility of merge requests."

    model_experiments_access_level: Optional[AccessLevel] = None
    "Set visibility of machine learning model experiments."

    model_registry_access_level: Optional[AccessLevel] = None
    "Set visibility of machine learning model registry."

    monitor_access_level: Optional[AccessLevel] = None
    "Set visibility of application performance monitoring."

    pages_access_level: Optional[AccessLevel] = None
    "Set visibility of GitLab Pages."

    releases_access_level: Optional[AccessLevel] = None
    "Set visibility of releases."

    repository_access_level: Optional[AccessLevel] = None
    "Set visibility of repository."

    requirements_access_level: Optional[AccessLevel] = None
    "Set visibility of requirements management."

    security_and_compliance_access_level: Optional[AccessLevel] = None
    "Set visibility of security and compliance."

    snippets_access_level: Optional[AccessLevel] = None
    "Set visibility of snippets."

    package_registry_access_level: Optional[AccessLevel] = None
    "Enable or disable packages repository feature."


class ProjectConfig(BaseModel):
    settings: Optional[ProjectSettings] = None
    variables: Optional[dict[str, Variable]] = None
    protected_branches: Optional[dict[str, Optional[ProtectedBranch]]] = Field(
        default_factory=dict
    )
