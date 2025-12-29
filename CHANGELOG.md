## Changelog

### [0.3.1] - [2025-12-29]

#### Added
- **Enhanced Configuration Examples**:
  - Added comprehensive example configuration `pivlabform_test.yaml` with real-world settings
  - Included examples for protected branches, merge templates, CI/CD configurations
  - Added template examples for merge commit, squash commit, and suggestion messages

- **Top-Level Group Detection**:
  - Added `is_top_level_group()` method to automatically detect root-level groups
  - Implemented intelligent skipping of protected branches for subgroups
  - Added validation for GitLab API restrictions on subgroup configurations

- **Pipeline Role Management**:
  - Introduced `PipelineCancellationRole` enum for standardized role definitions
  - Added type-safe role configurations for CI/CD pipeline settings

- **Enhanced Model Documentation**:
  - Added comprehensive docstrings to all model fields
  - Included GitLab documentation links and feature availability notes
  - Added warnings for deprecated and premium-only features

#### Changed
- **BREAKING**: Renamed `EntirySettings` to `EntitySettings` (fixed typo)
- **Model Structure**:
  - Updated `ProjectConfig` to inherit from `BaseModel` instead of `EntitySettings`
  - Added proper `ConfigDict` configuration to models
  - Enhanced `ProtectedBranch` model with `extra="forbid"` validation

- **Configuration File Structure**:
  - Updated example files to use new `group_config` and `project_config` structure
  - Added realistic configuration values for testing
  - Removed placeholder comments in template files

- **GitLab API Integration**:
  - Improved error handling for protected branches in subgroups
  - Added proper logging for entity processing stages
  - Enhanced debugging output with JSON formatting

#### Fixed
- **Line Length Warnings**: Added per-file ignore for `entiry_settings.py` in flake8 configuration
- **Model Validation**: Fixed inheritance structure in configuration models
- **API Compatibility**: Ensured proper handling of GitLab API restrictions
- **Logging**: Improved debug and warning messages for better troubleshooting

#### Features
- **Comprehensive Protected Branches**:
  - Support for `allow_force_push` configuration
  - Proper access level management (merge, push, unprotect)
  - Automatic detection of existing branch configurations

- **Template Support**:
  - Added support for `merge_commit_template` with GitLab variables
  - Added `squash_commit_template` configuration
  - Support for multi-line template strings in YAML configuration

- **Enhanced Type Safety**:
  - Added `PipelineCancellationRole` enum for CI role management
  - Improved type hints throughout the codebase
  - Better validation of configuration parameters

#### Configuration Improvements
```yaml
# New features demonstrated:
project_config:
  settings:
    merge_commit_template: |
      Title: %{title}
      Merge branch '%{source_branch}' into '%{target_branch}
      Description: %{description}
      Linked issues: %{issues}
      Approved by: %{approved_by}

    ci_config_path: pipeline.gitlab-ci.yml
    merge_method: ff
    squash_option: default_on

  protected_branches:
    master:
      allow_force_push: false
      merge_access_level: 40
      push_access_level: 40
      unprotect_access_level: 40
```

#### Technical Improvements
- **Code Organization**: Restructured model imports and exports
- **Error Handling**: Graceful degradation for unsupported subgroup features
- **Documentation**: Comprehensive field-level documentation for all settings
- **Validation**: Added Pydantic validation rules for better configuration safety

#### Notes
- This release significantly improves the robustness of configuration management
- Subgroup limitations are now properly handled with clear warnings
- Template support enables consistent commit message formatting across projects
- The example configuration provides a comprehensive reference for real-world usage

---

### [0.3.0] - [2025-12-29]

#### Added
- **Protected Branches Management**:
  - Implemented complete CRUD operations for protected branches in GitLab
  - Added `update_entity_protected_branches()` method with full lifecycle management
  - Support for creating, updating, and deleting protected branches based on configuration
  - Added `allow_force_push` field to protected branch configuration

- **Enhanced Configuration Processing**:
  - Added support for protected branches in entity configuration processing
  - Improved configuration extraction with typed access to settings, variables, and protected branches
  - Added comprehensive debug logging for protected branch operations

- **Model Enhancements**:
  - Added `ProtectedBranch` model to public exports in `__init__.py`
  - Enhanced `ConfigModel` with proper JSON serialization mode

#### Changed
- **BREAKING**: Configuration structure now properly supports protected branches at entity level
- **API Client**: Replaced placeholder `protect_branches()` method with fully functional implementation
- **Serialization**: Updated `ConfigModel.dump_model_to_json()` to use `mode="json"` for proper enum serialization
- **Model Structure**: Moved `ProtectedBranch` model to main exports for better accessibility

#### Features
- **Intelligent Branch Management**:
  - Automatic detection of branches that need to be removed (not in configuration)
  - Smart comparison of existing vs configured branch settings
  - Conditional updates only when configurations differ
  - Support for `allow_force_push` boolean flag

- **Comprehensive Logging**:
  - Added detailed debug logging for branch comparison operations
  - Clear indication of CREATE, REMOVE, and SKIP operations
  - JSON-formatted output for configuration comparison

#### Technical Improvements
- **Code Organization**:
  - Consolidated protected branch logic into dedicated method
  - Improved type hints and documentation
  - Better separation of concerns in configuration processing

- **Error Handling**:
  - Robust parsing of GitLab API responses for protected branches
  - Graceful handling of missing configuration sections
  - Proper validation of branch names and access levels

#### Configuration Example:
```yaml
project_config:
  protected_branches:
    master:
      merge_access_level: 40
      push_access_level: 40
      unprotect_access_level: 50
      allow_force_push: false
    develop:
      merge_access_level: 30
      push_access_level: 30
      allow_force_push: true
```

#### Notes
- This release completes the protected branches feature that was previously a TODO
- Configuration now supports the full GitLab protected branches API capabilities
- The implementation follows GitLab's API constraints (DELETE + POST for updates)
- All operations are idempotent and will only make changes when necessary

---

### [0.2.0] - 2025-12-29

#### Added
- **New CI/CD Jobs**:
  - Added `validate` job to GitLab CI pipeline for configuration validation
  - Introduced `.base_job` template for shared CI configuration
  - Added pre-commit validation job with `DEBUG=true` environment variable

- **Code Structure**:
  - Created `utils` module to organize helper functions
  - Reorganized imports and module structure for better maintainability

- **Configuration Management**:
  - Added centralized configuration template at `configurations/templates/global_template.yaml`

#### Changed
- **BREAKING**: **Major CLI Restructuring**:
  - Renamed main entry point from `pivlabform.main:main` to `pivlabform.cli:cli` in `pyproject.toml`
  - Moved CLI logic from `_cli_logic.py` to `cli.py` module
  - Removed `__main__.py` in favor of direct CLI invocation
  - Updated imports throughout the codebase to use new module structure

- **BREAKING**: **Configuration Files Cleanup**:
  - Removed all example configuration files:
    - `configurations/custom_config.yaml`
    - `configurations/groups.yaml`
    - `configurations/groups_config.yaml`
    - `configurations/pivlabform-test.yaml`
    - `configurations/projects_config.yaml`
    - `configurations/protected_branches.yaml`
    - `configurations/single_project.yaml`
  - Configuration examples now centralized in template directory

- **BREAKING**: **Model Structure Refactor**:
  - Consolidated model classes into `entiry_settings.py`
  - Removed separate `base_settings.py`, `group.py`, and `project.py` model files
  - Simplified imports in `__init__.py`
  - Updated `ConfigModel` to import from new consolidated module

- **CI/CD Pipeline**:
  - Changed default image from `python:3.11` to `pre-commit:6.0.0`
  - Added `interruptible: false` to default job configuration
  - Enhanced pre-commit job with `-v` (verbose) flag
  - Restructured CI pipeline using job inheritance

- **Protected Branches Model**:
  - Simplified `ProtectedBranch` model by removing `name` field requirement
  - Updated import from `typing` to `typing_extensions`
  - Removed `ProtectedBranches` wrapper class

- **Error Handling**:
  - Changed logging level for configuration JSON from `info` to `debug`
  - Improved logging messages with better formatting

- **Dependencies**:
  - Added `.mypy_cache` to `.gitignore`

#### Fixed
- **Logging**: Fixed import paths for logger and helper functions
- **Code Organization**: Cleaned up circular dependencies and import structure
- **Type Safety**: Improved type annotations throughout the codebase

#### Removed
- **Deprecated Modules**:
  - `_cli_logic.py` - CLI logic moved to `cli.py`
  - `_consts.py` - Constants moved elsewhere
  - `_helpers.py` - Helpers moved to `utils/_helpers.py`
  - `_logger.py` - Logger moved to `utils/_logger.py`
  - `main.py` - Main entry point replaced by CLI module
  - `__main__.py` - Python module entry point removed

- **Unused Code**:
  - Removed commented-out `to_api_json` method from `Variable` model
  - Cleaned up redundant model classes and files

#### Notes
- This is a major restructuring release focusing on code organization and maintainability
- All configuration examples have been consolidated into templates
- The CLI interface has been completely reorganized for better extensibility
- The project structure now follows better Python packaging practices
- Configuration validation is now integrated into the CI/CD pipeline

---

### [0.1.2] - 2025-12-29

#### Added
- **New Configuration Structure**:
  - Added `group_config` and `project_config` sections with nested `settings` and `variables`
  - Added `groups` and `projects` root-level arrays for specifying target entities
  - Introduced `ConfigModel` for structured configuration validation

- **New Features**:
  - Support for protected branches configuration (stub implementation)
  - Enhanced error logging with JSON data dump for debugging
  - Added `check_validate()` helper function for dry-run validation
  - Support for multiple variable formats (dict and list) with automatic normalization

#### Changed
- **BREAKING**: Configuration file structure completely changed:
  - `group_settings` → `group_config.settings`
  - `project_settings` → `project_config.settings`
  - Variables now nested under `group_config.variables` and `project_config.variables`
  - Root-level `groups` and `projects` arrays for target specification

- **BREAKING**: CLI interface modified:
  - `Pivlabform` constructor now requires `config_file` parameter
  - Removed `config_file` parameter from `process_manual_configuration()` and `process_auto_configuration()`
  - CLI configuration is loaded once during initialization

- **Code Structure**:
  - Extracted logging setup to separate `_logger.py` module
  - Refactored variable processing with `_normalize_variables()` helper
  - Updated model imports to use new `ConfigModel`
  - Simplified `GroupConfig` and `ProjectConfig` model structures

- **Configuration Updates**:
  - Changed `RELEASE_VERSION` from "Q4_28" to "Q4_29"
  - Updated `VAULT_ROLE` from "pivlab_ci_01" to "pivlab_ci_02"
  - Modified `SECRET_TOKEN` value format and masking settings
  - Added example target entities in configuration

- **Enum Values**:
  - Updated `SharedRunnersSetting` enum with additional options: `DISABLED_AND_OVERRIDABLE`

#### Fixed
- **Error Handling**: Improved API error messages with JSON data context
- **Variable Processing**: Fixed handling of different variable input formats
- **Type Safety**: Enhanced type annotations throughout the codebase
- **Configuration Loading**: Fixed early loading and validation of config file

#### Removed
- **Deprecated Functions**:
  - Removed `get_variables_json()` helper function
  - Removed old `Variables` model class
  - Removed redundant color logging setup from `_helpers.py`

#### Notes
- This is a major breaking change that requires updating all configuration files
- The new configuration structure provides better organization and validation
- Target entities can now be specified directly in the configuration file
- Improved debugging capabilities with better error reporting

---

### [0.1.1] - 2025-12-28

#### Changed
- **CI/CD Pipeline**:
  - Removed color environment variables from GitLab CI configuration
  - Simplified cache configuration in `.gitlab-ci.yml`
  - Updated pre-commit hook versions in `.pre-commit-config.yaml`:
    - pre-commit-hooks from v6.0.0 to v4.4.0
    - black from 25.12.0 to 23.11.0
    - isort from 7.0.0 to 5.12.0
  - Removed flake8 and mypy hooks from pre-commit configuration
  - Added new pre-commit hooks: check-executables-have-shebangs, check-symlinks, mixed-line-ending

- **Code Quality**:
  - Updated type hints to use pyright-compatible syntax instead of mypy
  - Restructured models directory by merging separate model files into a single `__init__.py`
  - Removed module (`gvars`) for API configuration
  - Modified logging messages to use f-strings

- **Configuration**:
  - Updated example configuration in `config.yaml` with new test variables and settings
  - Changed default branch from unspecified to "master"

- **Dependencies**:
  - Removed type checking dependencies (mypy, types-requests, types-PyYAML, types-click)

#### Fixed
- **Type Safety**:
  - Updated `id` parameter type from `Optional[int]` to `Optional[str]` in CLI
  - Improved type handling in `_helpers.py` with pyright-compatible type annotations
  - Fixed URL construction in GitLab API client

- **Code Structure**:
  - Removed unused model files (`base_settings.py`, `group.py`, `project.py`, `variables.py`)
  - Consolidated model imports in `__init__.py`
  - Added proper module docstrings

#### Notes
- This update focuses on simplifying the codebase and transitioning from mypy to pyright for type checking
- The pre-commit configuration has been downgraded to more stable versions
- Configuration examples have been updated with more realistic test data
- The project metadata has been updated to reflect a more generic tool description

---
