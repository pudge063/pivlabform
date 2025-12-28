## Changelog

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

### Fixed
- **Type Safety**:
  - Updated `id` parameter type from `Optional[int]` to `Optional[str]` in CLI
  - Improved type handling in `_helpers.py` with pyright-compatible type annotations
  - Fixed URL construction in GitLab API client

- **Code Structure**:
  - Removed unused model files (`base_settings.py`, `group.py`, `project.py`, `variables.py`)
  - Consolidated model imports in `__init__.py`
  - Added proper module docstrings

### Notes
- This update focuses on simplifying the codebase and transitioning from mypy to pyright for type checking
- The pre-commit configuration has been downgraded to more stable versions
- Configuration examples have been updated with more realistic test data
- The project metadata has been updated to reflect a more generic tool description
