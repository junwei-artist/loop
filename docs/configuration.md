# Configuration Guide

## Overview

This guide covers all configuration options for the Taiga Epic Auto-Creation Script.

## Basic Setup

### Taiga API Configuration

```python
# --- Taiga API config ---
TAIGA_URL = "http://10.5.216.7:8000/api/v1"  # Your Taiga backend URL
USERNAME = "shopfloor"                        # Taiga username
PASSWORD = "shopfloor"                        # Taiga password
PROJECT_ID = 63                              # Target project ID
```

### Epic Configuration

```python
# --- Custom config for Epic naming ---
PROJECT_NAME = "X3570"                       # Logical project name
LINE_NAME = "L1_AOI"                        # Production line
ERROR_TYPE = "error1"                       # Error category
ERROR_DESC = "Threshold"                   # Short description
QUANTITY = 15                              # Number of issues observed
INSPECTION_METHOD = "Automated AOI system" # Detection method
```

## Epic Naming Convention

Epic names follow this pattern:
```
{PROJECT_NAME}_{LINE_NAME}_{ERROR_TYPE}_{ERROR_DESC}_{DATE}_{UUID}
```

**Example:** `X3570_L1_AOI_error1_Threshold_20250115_a1b2`

- Spaces in `ERROR_DESC` are replaced with underscores
- `DATE` format: `YYYYMMDD`
- `UUID` is truncated to 4 characters for uniqueness

## 5W2H Description Template

The Epic description uses this standardized format:

```python
EPIC_DESCRIPTION = f"""
📌 **5W2H Problem Description**

- **What:** {ERROR_TYPE} issue – {ERROR_DESC}
- **Where:** {PROJECT_NAME} production line ({LINE_NAME})
- **When:** {datetime.now().strftime("%Y-%m-%d")}
- **Who:** Operators and quality engineers monitoring the line
- **Why:** Root cause not yet identified – requires investigation
- **How:** Detected via {INSPECTION_METHOD}
- **How many:** {QUANTITY} affected units/issues observed
"""
```

## Customization Options

### Custom Project Settings

You can modify these variables for different projects:

- **PROJECT_NAME**: Change to your project identifier
- **LINE_NAME**: Update for different production lines
- **ERROR_TYPE**: Modify error categories (e.g., "Hardware", "Software", "Parameter")
- **ERROR_DESC**: Update with specific error descriptions
- **QUANTITY**: Set actual number of affected units
- **INSPECTION_METHOD**: Update detection method

### Environment-Based Configuration

For different environments, create configuration files:

#### Development (`config_dev.py`)
```python
TAIGA_URL = "http://localhost:8000/api/v1"
USERNAME = "dev_user"
PASSWORD = "dev_pass"
PROJECT_ID = 1
PROJECT_NAME = "DEV_PROJECT"
```

#### Production (`config_prod.py`)
```python
TAIGA_URL = "http://production.taiga.io/api/v1"
USERNAME = "prod_user"
PASSWORD = os.getenv("TAIGA_PASSWORD")
PROJECT_ID = 63
PROJECT_NAME = "PROD_PROJECT"
```

## Security Best Practices

### Environment Variables

Use environment variables for sensitive data:

```python
import os

USERNAME = os.getenv("TAIGA_USERNAME", "default_user")
PASSWORD = os.getenv("TAIGA_PASSWORD")  # Required
PROJECT_ID = int(os.getenv("TAIGA_PROJECT_ID", "63"))
```

### Configuration Validation

Add validation for required settings:

```python
def validate_config):
    required_vars = ["TAIGA_URL", "USERNAME", "PASSWORD", "PROJECT_ID"]
    missing = [var for var in required_vars if not globals().get(var)]
    if missing:
        raise ValueError(f"Missing required configuration: {missing}")
```

## Multi-Project Support

To support multiple projects, modify the main function:

```python
PROJECTS = [
    {"id": 63, "name": "X3570", "line": "L1_AOI"},
    {"id": 64, "name": "X3580", "line": "L2_AOI"},
]

def create_epic_for_project(project_config, error_data):
    # Implementation for project-specific Epic creation
    pass
```

## Troubleshooting Config Issues

### Common Configuration Problems

1. **Wrong PROJECT_ID**: Verify project exists and you have access
2. **Invalid Epic naming**: Check for special characters in naming fields
3. **Authentication failure**: Verify URL format and credentials
4. **Permission denied**: Ensure user has Epic/Story creation permissions

### Configuration Testing

Test your configuration:

```python
def test_configuration():
    try:
        token = taiga_auth()
        print("✅ Authentication successful")
        
        # Test project access
        r = requests.get(f"{TAIGA_URL}/projects/{PROJECT_ID}", 
                        headers={"Authorization": f"Bearer {token}"})
        if r.status_code == 200:
            print("✅ Project access confirmed")
        else:
            print("❌ Project access failed")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
```

---

**Last Updated:** January 2025
