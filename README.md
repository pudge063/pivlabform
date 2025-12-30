# PivLabForm - GitLab Configuration as Code

> Manage GitLab groups, projects, and settings as code using YAML configuration files

## 📑 Table of Contents
- [🌟 Overview](#-overview)
- [⚡ Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🔧 CLI Interface](#-cli-interface)
- [⚙️ Configuration Models](#️-configuration-models)
- [📊 Configuration Examples](#-configuration-examples)
- [🔌 API Reference](#-api-reference)
- [⚠️ Error Handling](#️-error-handling)
- [🛡️ Security Considerations](#-security-considerations)
- [🔧 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📜 Licensing](#-licensing)

---

## 🌟 Overview

PivLabForm is a configuration management tool for GitLab that allows you to manage GitLab groups, projects, and their settings as code using YAML configuration files.

## ⚡ Quick Start

1. **Install the tool:**
```bash
pip install pivlabform
```

2. **Set up authentication:**
```bash
export GITLAB_TOKEN="your-personal-access-token"
```

3. **Create a configuration file:**
```yaml
# config.yaml
groups:
  - "sandbox/my-group"

group_config:
  settings:
    description: "My development group"
    visibility: "private"
    default_branch: "main"
```

4. **Apply the configuration:**
```bash
pivlabform -c config.yaml
```

## 📦 Installation

### From Source
```bash
# Clone the repository
git clone https://gitlab.com/pivlab/pivlabform.git
cd pivlabform

# Install with Poetry
poetry install

# Build and install globally
poetry build
pip install dist/pivlabform-*.whl
```

### Using pip
```bash
pip install pivlabform
```

## 🔧 CLI Interface

### Basic Usage

```bash
# Show help
pivlabform --help

# Apply configuration from file
pivlabform -c configurations/templates/global_template.yaml

# Manual configuration for specific entity
pivlabform --manual --group --path "sandbox/my-group" -c config.yaml

# Validate configuration without applying
pivlabform -c config.yaml -v
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--ci` | | Run in CI mode (skip .env loading) | `False` |
| `--manual` | `-m` | Manual run for single group/project | `False` |
| `--project` | | Specify entity type as project | |
| `--group` | | Specify entity type as group | |
| `--path` | | GitLab path (e.g., `sandbox/test/project-1`) | |
| `--id` | | GitLab ID (e.g., `1001`) | |
| `--config-file` | `-c` | Configuration file path | `config.yaml` |
| `--recursive` | `-r` | Apply recursively to subgroups/projects | `False` |
| `--validate` | `-v` | Only validate, don't apply changes | `False` |
| `--gitlab-host` | | GitLab host URL | From env or default |

## ⚙️ Configuration Models

### Configuration File Structure

```yaml
# Root level configuration
group_config:
  settings:
    # Group settings (optional)
  variables:
    # Group variables (optional)

project_config:
  settings:
    # Project settings (optional)
  variables:
    # Project variables (optional)
  protected_branches:
    # Protected branches configuration (optional)

# Target entities (required)
groups:
  - "sandbox/pivlabform-tests"  # Group path
  - 1234                        # Group ID

projects:
  - "sandbox/pivlabform-tests/test-project-2"  # Project path
  - 2306                                       # Project ID
```

### Pydantic models:
- [entity settings](./src/pivlabform/gitlab/models/entity_settings.py)
- [entity config](./src/pivlabform/gitlab/models/entity_config.py)
- [config model](./src/pivlabform/gitlab/models/config_model.py)
- [variables](./src/pivlabform/gitlab/models/variables.py)

### Environment Variables

```bash
# Required for authentication
export GITLAB_TOKEN="your-personal-access-token"

# Optional: Override GitLab host
export CI_SERVER_HOST="https://gitlab.example.com"

# Optional: Enable debug logging
export DEBUG="true"
```

### Group Settings

#### Basic Settings
```yaml
group_config:
  settings:
    default_branch: "main"
    description: "My group description"
    visibility: "private"  # private, internal, public
    lfs_enabled: true
    auto_devops_enabled: false
```

#### Security Settings
```yaml
group_config:
  settings:
    require_two_factor_authentication: true
    two_factor_grace_period: 48
    prevent_sharing_groups_outside_hierarchy: true
```

#### Runner Settings
```yaml
group_config:
  settings:
    shared_runners_setting: "disabled_and_unoverridable"
    # Options:
    # - "disabled_and_unoverridable"
    # - "disabled_and_overridable"
    # - "enabled"
```

### Project Settings

#### Repository Settings
```yaml
project_config:
  settings:
    default_branch: "main"
    description: "Project description"
    visibility: "internal"
    merge_method: "merge"  # merge, rebase_merge, ff
    squash_option: "default_on"  # always, never, default_on, default_off
```

#### Pipeline Settings
```yaml
project_config:
  settings:
    ci_config_path: ".gitlab-ci.yml"
    ci_default_git_depth: 50
    auto_devops_enabled: false
    shared_runners_enabled: true
```

#### Access Levels
```yaml
project_config:
  settings:
    repository_access_level: "enabled"  # disabled, private, enabled, public
    issues_access_level: "enabled"
    merge_requests_access_level: "enabled"
    # Other access levels: wiki_access_level, snippets_access_level, etc.
```

### Variables Configuration

#### Group Variables
```yaml
group_config:
  variables:
    RELEASE_VERSION:
      key: RELEASE_VERSION
      value: "Q4_29"
      description: "Current release version"
      environment_scope: "production"
      masked: false
      protected: false
      raw: false
      variable_type: "env_var"
```

#### Project Variables
```yaml
project_config:
  variables:
    PROJECT_VERSION:
      key: PROJECT_VERSION
      value: "1.0.0"
      description: "Project version"
      environment_scope: "*"  # All environments
      masked: true
      protected: true
      raw: false
      variable_type: "env_var"
```

### Protected Branches

```yaml
project_config:
  protected_branches:
    master:
      allow_force_push: false
      merge_access_level: 40  # Maintainer (40), Developer (30)
      push_access_level: 40
      unprotect_access_level: 40
    develop:
      allow_force_push: true
      merge_access_level: 30
      push_access_level: 30
```

#### Access Level Values
- `0`: No access
- `10`: Guest
- `20`: Reporter
- `30`: Developer
- `40`: Maintainer
- `50`: Owner

## 📊 Configuration Examples

### Example 1: Basic Group Configuration

```yaml
# config.yaml
group_config:
  settings:
    description: "Development group"
    visibility: "private"
    default_branch: "main"
    auto_devops_enabled: false
  variables:
    ENVIRONMENT:
      key: ENV
      value: "development"
      masked: false

groups:
  - "development/my-team"
```

Apply configuration:
```bash
pivlabform -c config.yaml
```

### Example 2: Multi-Project Configuration

```yaml
# projects.yaml
project_config:
  settings:
    default_branch: "main"
    merge_method: "ff"
    squash_option: "default_on"
  variables:
    PROJECT_TYPE:
      key: TYPE
      value: "microservice"
      description: "Project architecture type"

projects:
  - "backend/services/api-gateway"
  - "backend/services/user-service"
  - "backend/services/auth-service"
```

Apply recursively:
```bash
pivlabform -c projects.yaml -r
```

### Example 3: Mixed Configuration

```yaml
# mixed-config.yaml
group_config:
  settings:
    description: "Infrastructure group"
    shared_runners_setting: "disabled_and_unoverridable"
  variables:
    INFRA_ENV:
      key: INFRA_ENVIRONMENT
      value: "staging"
      environment_scope: "staging"

project_config:
  settings:
    description: "Infrastructure project"
    shared_runners_enabled: false
  variables:
    TF_VERSION:
      key: TERRAFORM_VERSION
      value: "1.5.0"

groups:
  - "infrastructure"

projects:
  - "infrastructure/terraform-modules"
```

## 🔌 API Reference

### Core Classes

#### `Pivlabform`
Main class for configuration management.

```python
import os

os.environ["DEBUG"] = "true"
os.environ["CI_SERVER_HOST"] = "pivlab.space"

from pivlabform import LOGGER, GitLab
from pivlabform.gitlab.gitlab import Entity
from pivlabform.gitlab.models import GroupSettings, ProjectSettings
from pivlabform.gitlab.models.entity_settings import MergeMethod


def configure_projects_in_group(group: str) -> None:
    """
    Procedure for confugure all projects in group with settings:
        - default_branch: master
        - description: configuration from test_api.py
        - for merge needs resolve all discussions and pipeline success
        - merge strategy: fast-forward

    :param group: target group path
    :type group: str
    """
    gl = GitLab()

    project_settings_model = ProjectSettings(
        default_branch="master",
        description="configuration from test_api.py",
        only_allow_merge_if_all_discussions_are_resolved=True,
        only_allow_merge_if_pipeline_succeeds=True,
        merge_method=MergeMethod.FF,
    )

    group_settings_model = GroupSettings(
        default_branch="master",
    )

    group_id = gl.get_entity_id_from_url(group, Entity.GROUP)
    groups = gl.get_all_groups_recursive(group_id)
    projects = gl.get_all_projects_recursive(group_id)

    LOGGER.info(f"projects for config: {projects}")
    LOGGER.info(f"groups for config: {groups}")

    for group_id in groups:
        gl.confugure_entity(
            entity_id=group_id,
            entity_type=Entity.GROUP,
            config=group_settings_model.to_api_json(),
        )

    for project_id in projects:
        gl.confugure_entity(
            entity_id=project_id,
            entity_type=Entity.PROJECT,
            config=project_settings_model.to_api_json(),
        )


if __name__ == "__main__":
    configure_projects_in_group("sandbox/pivlabform-tests")
```

#### `GitLab`
GitLab API client wrapper.

```python
from pivlabform.gitlab.gitlab import GitLab

gl = GitLab("https://gitlab.example.com")

# Get entity ID from path
group_id = gl.get_entity_id_from_url("sandbox/test", "group")

# Get all projects recursively
projects = gl.get_all_projects_recursive(group_id)

# Update entity variables
gl.update_entity_variables(
    entity_id=project_id,
    entity_type="project",
    config_variables=[...]
)
```

## ⚠️ Error Handling

### Common Errors

1. **Authentication Error**: Ensure `GITLAB_TOKEN` is set correctly
2. **Permission Error**: Token needs appropriate permissions
3. **Configuration Error**: Validate YAML syntax and schema
4. **Network Error**: Check GitLab host accessibility

### Debug Mode

Enable debug logging:
```bash
export DEBUG=true
pivlabform -c config.yaml
```

## 🛡️ Security Considerations

- Store `GITLAB_TOKEN` securely (never in version control)
- Use masked variables for sensitive data
- Set appropriate access levels
- Regularly rotate access tokens
- Review permission inheritance in group hierarchies

## 🔧 Troubleshooting

### Configuration Not Applying
1. Check entity paths/IDs are correct
2. Verify token has write permissions
3. Check GitLab API rate limits
4. Validate YAML syntax

### Variables Not Updating
1. Check variable keys match exactly
2. Verify environment scope settings
3. Check for conflicting variables at different levels
4. Validate variable masking settings

### Permission Issues
1. Token must have `api` scope
2. User must have maintainer/owner access
3. Check group/project permission inheritance
4. Verify token is not expired

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Update documentation
5. Submit pull request

## 📜 Licensing

This software is available under a **dual-licensing model**:

### 1. For the Community and Open Source Projects: GNU Affero General Public License v3.0 (AGPL-3.0)
- You may **freely use, study, modify, and distribute** this library.
- **If you modify the library and make it available over a network (e.g., as a web service or SaaS), you are obligated to make the complete source code of your modifications available** to all users of your service.
- This is a classic strong copyleft free software license that ensures improvements remain open.

### 2. For Commercial and Proprietary Use: Commercial License
If the terms of the AGPL-3.0 are incompatible with your business model (for example, you do not wish to open-source your product's code), you may purchase a **commercial license** from the copyright holder.

**The commercial license grants:**
- The right to use the library in **closed-source (proprietary) products**.
- Exemption from the AGPL's source code disclosure requirements.
- Direct warranties and priority support.
- The possibility of requesting custom features.

---

**To inquire about a commercial license:**
📧 **Email:** studentq.work@yandex.ru
💬 **Telegram:** @pudge_vibes
*Please include in your email: company name, intended use case, and approximate number of developers.*

---

*Copyright (c) 2025 PivLab. All rights reserved.*
