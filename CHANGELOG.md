## Changelog

### [0.5.0] - 2025-12-31

#### Breaking Changes
- **License Change**: Switched from PivLab Proprietary License to GNU Affero General Public License v3.0 (AGPLv3)

#### Added
- **GNU AGPLv3 License**: Full license text removed
- **AGPL Compliance Documentation**: All references to AGPL requirements
- **Source Code Sharing Mandates**: AGPL's network use and source distribution requirements

#### Removed
- **Proprietary License**: Added PivLab Software License Agreement
  - Dual-license model: Free for non-commercial use, paid for commercial use
  - Clear definitions of Commercial vs. Non-Commercial use
  - Intellectual property retention by PivLab
  - Russian Federation governing law (Moscow jurisdiction)
  - Contact information for licensing inquiries

- **Commercial Licensing Information**:
  - Contact email: `studentq.work@yandex.ru`
  - Telegram contact: `@pudge_vibes`
  - Explicit commercial license requirement for business use

- **New License Sections**:
  - Grant of License (separate commercial/non-commercial terms)
  - Usage restrictions and intellectual property rights
  - Support tiers (community vs. priority)
  - Export controls and termination conditions

#### Changed
- **README.md**: Completely restructured and simplified
  - Removed extensive AGPL licensing explanation
  - Replaced with link to new LICENSE.md
  - Simplified installation instructions (removed pip install method)
  - Streamlined documentation structure
  - Removed detailed contributing guidelines
  - Updated API reference examples

- **Project Documentation**:
  - Removed "Table of Contents" with 15+ sections
  - Simplified "Overview" section
  - Consolidated configuration examples
  - Removed detailed troubleshooting guides
  - Updated support information

- **Source Code**:
  - Updated internal references and imports

#### Notes
- **For Existing Users**:
  - Non-commercial users can continue using the software freely
  - Commercial users must contact PivLab for licensing
  - All modifications contributed back become PivLab property

- **For Contributors**:
  - By contributing, you grant PivLab perpetual rights to your contributions
  - Community contributions remain welcome for non-commercial improvements

- **Legal Implications**:
  - Software is no longer copyleft/open source in the traditional sense
  - Proprietary license with controlled commercial distribution
  - PivLab retains all intellectual property rights

- **Support**:
  - Community support via GitLab issues continues
  - Priority support available with commercial licenses
  - Security updates provided to all users

**Important**: This release represents a fundamental change in licensing and business model. Users should review the new license terms carefully before continuing use.

---

### [0.4.1] - [2025-12-30]

#### Added
- **Enhanced Entity Enum System**:
  - Added `Entity.from_string()` method for flexible entity type parsing
  - Added `Entity.lname` property for lowercase string representation
  - Support for aliases (g/p/s) for entity type specification
  - Automatic error handling for unknown entity types

- **Enhanced Variable Validation**:
  - Added comprehensive `Variable` model validation with regex patterns
  - Implemented key format validation (A-Z, a-z, 0-9, _ only)
  - Added reserved key detection (CI, GITLAB, KUBERNETES)
  - Length validation for keys (max 255 characters)

- **Public API Exports**:
  - Exposed `LOGGER` in package's public interface for external use
  - Made all core configuration models publicly accessible
  - Enhanced library usability for programmatic integration

- **Enhanced Protected Branch Documentation**:
  - Added detailed docstrings to `ProtectedBranch` model fields
  - Clarified access level defaults and behaviors
  - Improved documentation for premium/ultimate features

#### Changed
- **BREAKING**: Renamed `entiry_settings.py` to `entity_settings.py` and `entity_config.py`
- **BREAKING**: Split monolithic model file into logical modules:
  - `entity_settings.py` → Entity settings models
  - `entity_config.py` → Configuration container models
- **Type System**:
  - Replaced `typing_extensions.Self` with `Self` import
  - Standardized imports from `typing_extensions`
  - Improved type hints throughout the codebase
- **CI/CD Integration**:
  - Added `--ci` flag to GitLab CI validation job
  - Ensured proper CI environment handling
- **Model Organization**:
  - Separated entity settings from configuration containers
  - Improved import structure and module dependencies
- **Logging Improvements**:
  - Changed configuration success messages from `info` to `debug` level
  - Enhanced entity processing logs with type information
  - Added conditional logging for configuration sections

#### Removed
- **Deprecated Functions**:
  - Removed `get_resource_from_entity_type()` helper function
  - Eliminated dependency on legacy `_consts` module
- **Legacy Code**:
  - Deleted monolithic `entiry_settings.py` file
  - Removed obsolete type hints and imports

#### Fixed
- **Configuration Processing**:
  - Fixed entity type detection in manual configuration
  - Added proper validation for recursive operations
  - Fixed conditional configuration application logic
- **Model Validation**:
  - Added comprehensive validation for Variable keys
  - Fixed field default specifications in Pydantic models
- **API Endpoints**:
  - Standardized endpoint construction using Entity enum
  - Fixed URL encoding for entity paths

#### Technical Improvements
- **Code Quality**:
  - Added `field_validator` decorators for robust input validation
  - Implemented proper error messages for validation failures
  - Enhanced model documentation with practical examples
- **Error Handling**:
  - Added graceful error handling for unknown entity types
  - Improved user feedback for configuration errors
- **Module Structure**:
  ```python
  # Before: from .entiry_settings import GroupConfig, ProjectConfig
  # After: from .entity_config import GroupConfig, ProjectConfig
  # After: from .entity_settings import GroupSettings, ProjectSettings
  ```

#### Example Configuration Update:
```yaml
# Configuration now properly organized
group_config:
  settings:  # GroupSettings model
    default_branch: "main"

  variables:  # List of Variable models
    - key: "ENV_VAR"
      value: "production"

  protected_branches:  # ProtectedBranch models
    main:
      merge_access_level: 40
```

#### CLI Improvements:
```bash
# Enhanced entity type parsing
pivlabform --group sandbox/my-group  # Full name
pivlabform -g sandbox/my-group       # Alias support
pivlabform --project 1234            # Project by ID
```

#### Notes
- This release significantly improves the code organization and maintainability
- The split model structure follows single responsibility principle
- Enhanced validation prevents common configuration errors
- Better public API enables advanced integration scenarios
- Entity enum system provides type safety and developer experience improvements

---

### [0.4.0] - [2025-12-30]

#### Added
- **Enum-Based Entity Management**:
  - Introduced `Entity` enum (`GROUP`, `PROJECT`, `SUBGROUP`) for type-safe entity handling
  - Added enum-based API endpoints throughout the codebase
  - Improved type safety in all entity-related operations

- **Public API Exports**:
  - Exposed `GitLab` class in package's public interface (`__init__.py`)
  - Made core models (`ProjectConfig`, `ProjectSettings`, `GroupConfig`, `GroupSettings`) publicly accessible
  - Enhanced library usability for external integration

- **Enhanced Model Field Definitions**:
  - Added `default=None` to Pydantic `Field` definitions for better serialization
  - Updated type hints for boolean fields (`bool | None` syntax)
  - Improved model consistency and validation

#### Changed
- **BREAKING**: All entity type parameters changed from `str` to `Entity` enum
- **BREAKING**: Updated method signatures to use `Entity` enum instead of string literals
- **API Endpoint Construction**:
  - Replaced hardcoded endpoint strings with enum values (`Entity.GROUP.value`, `Entity.PROJECT.value`)
  - Improved endpoint consistency across all GitLab API calls
- **Conditional Configuration Application**:
  - Added null checks before applying variables and protected branches configurations
  - Prevented unnecessary API calls when configurations are empty
- **Improved Logging**:
  - Added entity type names in configuration success messages
  - Enhanced debugging information

#### Fixed
- **Type Safety**: Eliminated string-based entity type comparisons in favor of enum
- **Code Quality**: Removed deprecated `get_resource_from_entity_type()` helper function
- **Configuration Processing**: Fixed conditional logic for empty configurations
- **Recursive Validation**: Improved validation for recursive operations on projects

#### Technical Improvements
- **Endpoint Constants**:
  ```python
  # Before: "groups/{id}/projects"
  # After: f"{Entity.GROUP.value}/{target_group}/{Entity.PROJECT.value}"
  ```
- **Entity Type Handling**:
  ```python
  # Before: entity_type == "group"
  # After: entity_type == Entity.GROUP
  ```
- **Model Field Defaults**:
  ```python
  # Before: Optional[int] = Field(None, ge=0)
  # After: Optional[int] = Field(default=None, ge=0)
  ```

#### Example Changes:
```python
# Before:
self.gl.get_entity_id_from_url("sandbox/test", "group")

# After:
self.gl.get_entity_id_from_url("sandbox/test", Entity.GROUP)

# Before:
self._process_entity_configuration(groups, "group")

# After:
self._process_entity_configuration(groups, Entity.GROUP)
```

#### Benefits
1. **Type Safety**: Compile-time checking of entity types
2. **Code Completion**: IDE support for enum values
3. **Reduced Errors**: Eliminated string typos in entity type handling
4. **Better Documentation**: Clear entity type options
5. **Consistency**: Uniform API endpoint construction

#### Migration Notes
- Update all calls to `GitLab` methods to use `Entity` enum instead of strings
- Import `Entity` from `pivlabform.gitlab.gitlab` when needed
- String comparisons for entity types need to be updated:
  ```python
  # Old: if entity_type == "group"
  # New: if entity_type == Entity.GROUP
  # Or for CLI string inputs: if entity_type == Entity.GROUP.name.lower()
  ```

#### Notes
- This release significantly improves the type safety and maintainability of the codebase
- The enum-based approach prevents common errors with string-based entity type handling
- Public API exposure enables better integration with external tools and scripts
- Conditional configuration application reduces unnecessary API calls and improves performance

---

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
  - Changed default image for validate job from `python:3.11` to `pre-commit:6.0.0`
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
  - Added color environment variables from GitLab CI configuration
  - Removed cache configuration in `.gitlab-ci.yml`
  - Updated pre-commit hook versions in `.pre-commit-config.yaml`:
    - pre-commit-hooks from v4.4.0 to v6.0.0
    - black from 23.11.0 to 25.12.0
    - isort from 5.12.0 to 7.0.0
  - Added flake8 and mypy hooks from pre-commit configuration
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
  - Added type checking dependencies (mypy, types-requests, types-PyYAML, types-click)

#### Fixed
- **Type Safety**:
  - Updated `id` parameter type from `Optional[str]` to `Optional[int]` in CLI
  - Improved type handling in `_helpers.py` with pyright-compatible type annotations
  - Fixed URL construction in GitLab API client

- **Code Structure**:
  - Added model files (`base_settings.py`, `group.py`, `project.py`, `variables.py`)
  - Consolidated model imports in `__init__.py`
  - Added proper module docstrings

#### Notes
- This update focuses on simplifying the codebase and transitioning from mypy to pyright for type checking
- The pre-commit configuration has been downgraded to more stable versions
- Configuration examples have been updated with more realistic test data
- The project metadata has been updated to reflect a more generic tool description

---
