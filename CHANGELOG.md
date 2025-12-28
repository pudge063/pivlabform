## Changelog

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
