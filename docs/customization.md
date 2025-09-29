# Customization Guide

## Overview

This guide explains how to customize the Taiga Epic Auto-Creation Script for your specific needs.

## Epic Customization

### Custom Epic Templates

Create different Epic templates for various error types:

```python
EPIC_TEMPLATES = {
    "hardware_error": {
        "description_template": """
🔧 **Hardware Issue - 5W2H Analysis**

- **What:** Hardware malfunction – {ERROR_DESC}
- **Where:** {PROJECT_NAME} production line ({LINE_NAME})
- **When:** {date}
- **Who:** Hardware engineers and maintenance team
- **Why:** Equipment failure causing production issues
- **How:** Detected via {INSPECTION_METHOD}
- **How many:** {QUANTITY} affected units
        """,
        "error_types": ["Hardware", "Equipment", "Component"]
    },
    
    "software_error": {
        "description_template": """
💻 **Software Issue - 5W2H Analysis**

- **What:** Software problem – {ERROR_DESC}
- **Where:** {PROJECT_NAME} production line ({LINE_NAME})
- **When:** {date}
- **Who:** Software engineers and developers
- **Why:** Application or system malfunction
- **How:** Detected via {INSPECTION_METHOD}
- **How many:** {QUANTITY} affected units
        """,
        "error_types": ["Software", "Application", "System"]
    }
}
```

### Dynamic Epic Selection

```python
def select_epic_template(error_type):
    for template_name, template_data in EPIC_TEMPLATES.items():
        if error_type in template_data["error_types"]:
            return template_data["description_template"]
    return EPIC_DESCRIPTION  # Default template

# Usage
selected_template = select_epic_template(ERROR_TYPE)
custom_description = selected_template.format(
    ERROR_DESC=ERROR_DESC,
    PROJECT_NAME=PROJECT_NAME,
    LINE_NAME=LINE_NAME,
    date=datetime.now().strftime("%Y-%m-%d"),
    INSPECTION_METHOD=INSPECTION_METHOD,
    QUANTITY=QUANTITY
)
```

## User Story Customization

### Custom User Story Templates

Modify the USER_STORIES list for different methodologies:

```python
# Agile Development Stories
AGILE_STORIES = [
    ("Planning", "Analyze requirements and plan implementation"),
    ("Design", "Create technical design and architecture"),
    ("Development", "Implement the solution"),
    ("Testing", "Perform comprehensive testing"),
    ("Deployment", "Deploy to production environment"),
    ("Monitoring", "Monitor system performance and stability"),
]

# Custom Manufacturing Workflow
MANUFACTURING_STORIES = [
    ("Initial Detection", "Identify and document the problem"),
    ("Impact Assessment", "Assess impact on production line"),
    ("Root Cause Analysis", "Investigate underlying causes"),
    ("Containment Plan", "Implement immediate containment measures"),
    ("Corrective Action", "Develop and implement permanent fix"),
    ("Verification", "Verify solution effectiveness"),
    ("Process Update", "Update procedures to prevent recurrence"),
    ("Team Recognition", "Recognize team efforts"),
]

# Replace USER_STORIES with your custom template
USER_STORIES = MANUFACTURING_STORIES
```

### Dynamic Story Selection

```python
def get_stories_for_error_type(error_type):
    story_mapping = {
        "hardware": MANUFACTURING_STORIES,
        "software": AGILE_STORIES,
        "parameter": USER_STORIES  # Default 8D methodology
    }
    return story_mapping.get(error_type.lower(), USER_STORIES)

# Usage
selected_stories = get_stories_for_error_type(ERROR_TYPE)
```

## Advanced Customization

### Custom Fields Integration

Add custom fields to Epics and User Stories:

```python
def create_epic_with_custom_fields(token, project_id, subject, description, custom_fields=None):
    headers = {"Authorization": f"Bearer {token}"}
    epic_data = {
        "project": project_id,
        "subject": subject,
        "description": description
    }
    
    # Add custom fields if provided
    if custom_fields:
        epic_data.update(custom_fields)
    
    r = requests.post(f"{TAIGA_URL}/epics", json=epic_data, headers=headers)
    r.raise_for_status()
    return r.json()

# Usage with custom fields
custom_fields = {
    "custom_field_1": ERROR_TYPE,
    "custom_field_2": QUANTITY,
    "custom_field_3": INSPECTION_METHOD
}

epic = create_epic_with_custom_fields(
    token, PROJECT_ID, EPIC_NAME, EPIC_DESCRIPTION, custom_fields
)
```

### Priority and Tags Customization

```python
def create_epic_with_priority(token, project_id, subject, description, priority=None, tags=None):
    headers = {"Authorization": f"Bearer {token}"}
    epic_data = {
        "project": project_id,
        "subject": subject,
        "description": description
    }
    
    if priority:
        epic_data["priority"] = priority
    
    if tags:
        epic_data["tags"] = tags
    
    r = requests.post(f"{TAIGA_URL}/epics", json=epic_data, headers=headers)
    r.raise_for_status()
    return r.json()

# Usage with priority and tags
priority_level = "High" if QUANTITY > 10 else "Medium"
tags = [ERROR_TYPE, LINE_NAME, "Manufacturing"]

epic = create_epic_with_priority(
    token, PROJECT_ID, EPIC_NAME, EPIC_DESCRIPTION, priority_level, tags
)
```

## File-Based Configuration

### Configuration File Support

Create a `config.json` file:

```json
{
    "taiga": {
        "url": "http://10.5.216.7:8000/api/v1",
        "username": "shopfloor",
        "password": "shopfloor",
        "project_id": 63
    },
    "epic": {
        "project_name": "X3570",
        "line_name": "L1_AOI",
        "error_type": "error1",
        "error_desc": "Threshold",
        "quantity": 15,
        "inspection_method": "Automated AOI system"
    },
    "templates": {
        "epic_description": "custom_template.md",
        "user_stories": "manufacturing_stories.json"
    }
}
```

### Load Configuration Function

```python
import json

def load_config(config_path="config.json"):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Configuration file {config_path} not found. Using defaults.")
        return None

# Usage
config = load_config()
if config:
    TAIGA_URL = config["taiga"]["url"]
    USERNAME = config["taiga"]["username"]
    # ... load other settings
```

## Multi-Environment Support

### Environment-Specific Configuration

```python
import os

def get_environment_config():
    env = os.getenv("ENVIRONMENT", "dev").lower()
    
    configs = {
        "dev": {
            "taiga_url": "http://dev.taiga.io/api/v1",
            "project_id": 1,
            "inspection_method": "Manual inspection"
        },
        "test": {
            "taiga_url": "http://test.taiga.io/api/v1",
            "project_id": 2,
            "inspection_method": "Automated testing"
        },
        "prod": {
            "taiga_url": "http://prod.taiga.io/api/v1",
            "project_id": 63,
            " the method from config

ENVIRONMENT_CONFIG = get_environment_config()
# Update global variables
if ENVIRONMENT_CONFIG:
    TAIGA_URL = ENVIRONMENT_CONFIG["taiga_url"]
    PROJECT_ID = ENVIRONMENT_CONFIG["project_id"]
```

## Output Customization

### Custom Logging Format

```python
import logging

# Setup custom logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('taiga_epic_creation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Replace print statements with logger
logger.info(f"🔑 Authenticating as {USERNAME}...")
logger.info(f"✅ Created Epic: {epic['subject']}")
```

### Custom Output Reports

```python
def generate_report(epic, stories):
    """Generate a report of created Epic and User Stories"""
    report = f"""
# Epic Creation Report
## Epic Details
- **Name:** {epic['subject']}
- **ID:** {epic['id']}
- **Reference:** {epic['ref']}
- **Project:** {epic['project']}

## Created User Stories ({len(stories)})
"""
    
    for i, story in enumerate(stories, 1):
        report += f"{i}. **{story['subject']}** (ID: {story['id']})\n"
    
    return report

# Save report to file
with open(f"epic_report_{EPIC_NAME}.md", "w") as f:
    f.write(generate_report(epic, created_stories))
```

## Testing Customizations

### Configuration Testing Framework

```python
def test_custom_configuration():
    """Test all configuration customizations"""
    tests = [
        test_epic_naming_convention,
        test_description_template,
        test_user_story_creation,
        test_linking_functionality
    ]
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__} passed")
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")

def test_epic_naming_convention():
    """Test Epic naming pattern"""
    expected_pattern = f"{PROJECT_NAME}_{LINE_NAME}_{ERROR_TYPE}_{ERROR_DESC_NAME}_{DATE_STR}_"
    assert expected_pattern in EPIC_NAME
    assert len(EPIC_NAME.split("_")) == 6  # Should have 6 parts
```

---

**Last Updated:** January 2025
