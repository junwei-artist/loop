# Taiga Epic + User Story Auto-Creation Script

This Python script automates the creation of an **Epic** in Taiga and generates a set of **standardized User Stories (D0–D8)** linked to that Epic. It is designed for **manufacturing/production error tracking**, following an **8D problem-solving process**.

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Customization](#-customization)
- [Documentation](#-documentation)
- [Troubleshooting](#-troubleshooting)

## 🚀 Features

- ✅ Creates a new **Epic** in a specified project
- ✅ Epic **name** auto-generated from multiple parameters
- ✅ Epic **description** auto-generated using a **5W2H template**
- ✅ Creates **User Stories (D0–D8)** with predefined descriptions
- ✅ Automatically links each User Story to the Epic
- ✅ Debug logs show API requests and responses
- ✅ Unique Epic naming with UUID and timestamp

## ⚙️ Requirements

- Python 3.9+
- `requests` library

### Installation

Install the required dependencies:

```bash
pip install requests
```

## 🔧 Configuration

### Basic Configuration

Edit the configuration section in `api.py`:

```python
# --- Taiga API config ---
TAIGA_URL = "http://10.5.216.7:8000/api/v1"  # Your Taiga backend URL
USERNAME = "your_username"                   # Your Taiga username
PASSWORD = "your_password"                   # Your Taiga password
PROJECT_ID = 63                              # Target project ID

# --- Custom config for Epic naming ---
PROJECT_NAME = "X3570"                       # Logical project name
LINE_NAME = "L1_AOI"                        # Production line
ERROR_TYPE = "error1"                       # Error category
ERROR_DESC = "Threshold"                   # Short description
QUANTITY = 15                              # Number of issues observed
INSPECTION_METHOD = "Automated AOI system" # Detection method
```

### Epic Name Generation

Epic names are automatically generated using this formula:
```
{PROJECT_NAME}_{LINE_NAME}_{ERROR_TYPE}_{ERROR_DESC}_{YYYYMMDD}_{UUID}
```

Example: `X3570_L1_AOI_error1_Threshold_20250115_a1b2`

### 5W2H Description Template

The Epic description follows a standardized 5W2H format:

- **What:** Error type and description
- **Where:** Project and line location
- **When:** Current date
- **Who:** Responsible team members
- **Why:** Investigation requirement note
- **How:** Detection method
- **How many:** Affected quantity

## 📖 Usage

### Basic Usage

1. **Configure the script** by editing the configuration variables in `api.py`
2. **Run the script**:

```bash
python api.py
```

### Example Output

```
🔑 Authenticating as your_username...
✅ Auth success
📦 Creating epic: X3570_L1_AOI_error1_Threshold_20250115_a1b2 in project 63...
✅ Epic created (ID 123, Ref EPIC-456)
📌 Creating and linking user stories...
   → Story created and attempted link: D0: Plan (Story ID 789)
   → Story created and attempted link: D1: Establish a team (Story ID 790)
   → Story created and attempted link: D2: Define and describe the problem (Story ID 791)
   ...
🎉 Done! Check above logs for link status.
```

## 🛠️ Customization

### Customizing User Stories (D0-D8)

The script creates 9 predefined User Stories following the 8D methodology. You can customize these by modifying the `USER_STORIES` list in the script:

```python
USER_STORIES = [
    ("D0: Plan", "Your custom description for planning phase"),
    ("D1: Establish a team", "Your custom description for team formation"),
    # ... modify other entries
]
```

### Customizing Epic Description Format

Modify the `EPIC_DESCRIPTION` template to match your organization's standards:

```python
EPIC_DESCRIPTION = f"""
📌 **Your Custom Problem Description Format**

- **Issue:** {ERROR_TYPE} – {ERROR_DESC}
- **Location:** {PROJECT_NAME} production line ({LINE_NAME})
- **Date:** {datetime.now().strftime("%Y-%m-%d")}
- **Team:** Your team description
- **Root Cause:** Investigation required
- **Detection:** {INSPECTION_METHOD}
- **Impact:** {QUANTITY} affected units/issues
"""
```

### Adding Custom Fields

To add custom fields to your Epic or User Stories, modify the data structures in the creation functions:

```python
def create_epic(token, project_id, subject, description="", custom_field=None):
    # ... existing code ...
    epic_data = {
        "project": project_id,
        "subject": subject,
        "description": description,
        "custom_field": custom_field  # Add your custom field
    }
    # ... rest of function ...
```

## 📚 Documentation

Detailed documentation is available in the [docs/](docs/) directory:

- [API Reference](docs/api-reference.md) - Complete API documentation
- [Configuration Guide](docs/configuration.md) - Detailed configuration options
- [Customization Guide](docs/customization.md) - Advanced customization options
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions
- [8D Methodology](docs/8d-methodology.md) - Background on the 8D process

## 🐛 Troubleshooting

### Common Issues

#### Authentication Failed
```
Error: HTTP 401 Unauthorized
```
**Solution:** Verify your Taiga URL, username, and password are correct.

#### Project Not Found
```
Error: HTTP 404 Not Found
```
**Solution:** Check that the PROJECT_ID exists and you have access to it.

#### Epic Creation Failed
```
Error: HTTP 400 Bad Request
```
**Solution:** 
- Ensure Epic naming doesn't contain invalid characters
- Check project configuration allows Epic creation
- Verify your account has sufficient permissions

#### User Story Linking Failed
```
❌ Failed linking (HTTP 500)
```
**Solution:**
- Check Epic exists and is valid
- Verify project configuration allows User Story linking
- Check user permissions for Epic modifications

### Debug Mode

The script includes built-in debug logging. Check the console output for:
- Authentication status
- API request/response details
- Linking attempt results

### Getting Help

1. Check the [Troubleshooting Guide](docs/troubleshooting.md)
2. Review the [API Reference](docs/api-reference.md)
3. Enable debug mode and check console logs
4. Verify Taiga project configuration

## 📝 License

This script is provided as-is for manufacturing and production error tracking purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests to improve this automation script.

---

**Last Updated:** January 2025
