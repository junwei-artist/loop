# API Reference Documentation

## Overview

This document provides detailed API reference for the Taiga Epic + User Story Auto-Creation Script.

## Authentication

### `taiga_auth()`

Authenticates with the Taiga API and returns an authentication token.

**Parameters:** None

**Returns:** `str` - Authentication token

**Example:**
```python
token = taiga_auth()
```

**API Endpoint:** `POST {TAIGA_URL}/auth`

**Request Body:**
```json
{
    "type": "normal",
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "auth_token": "abc123...",
    "refresh": "def456..."
}
```

## Epic Operations

### `create_epic(token, project_id, subject, description="")`

Creates a new Epic in the specified Taiga project.

**Parameters:**
- `token` (str): Authentication token
- `project_id` (int): Project ID where Epic will be created
- `subject` (str): Epic title/name
- `description` (str, optional): Epic description (default: empty)

**Returns:** `dict` - Created Epic data

**Example:**
```python
epic = create_epic(
    token=token,
    project_id=63,
    subject="Production_Issue_20250115",
    description="Detailed problem description..."
)
```

**API Endpoint:** `POST {TAIGA_URL}/epics`

**Request Body:**
```json
{
    "project": 63,
    "subject": "Production_Issue_20250115",
    "description": "Detailed problem description..."
}
```

**Response:**
```json
{
    "id": 123,
    "ref": 456,
    "subject": "Production_Issue_20250115",
    "description": "Detailed problem description...",
    "project": 63,
    "created_date": "2025-01-15T10:30:00Z"
}
```

## User Story Operations

### `create_user_story(token, project_id, subject, description)`

Creates a new User Story in the specified Taiga project.

**Parameters:**
- `token` (str): Authentication token
- `project_id` (int): Project ID where User Story will be created
- `subject` (str): User Story title/name
- `description` (str): User Story description

**Returns:** `dict` - Created User Story data

**Example:**
```python
story = create_user_story(
    token=token,
    project_id=63,
    subject="D0: Plan",
    description="Plan for solving the problem and determine prerequisites."
)
```

**API Endpoint:** `POST {TAIGA_URL}/userstories`

**Request Body:**
```json
{
    "project": 63,
    "subject": "D0: Plan",
    "description": "Plan for solving the problem and determine prerequisites."
}
```

**Response:**
```json
{
    "id": 789,
    "ref": 101,
    "subject": "D0: Plan",
    "description": "Plan for solving the problem...",
    "project": 63,
    "created_date": "2025-01-15T10:30:00Z"
}
```

### `link_story_to_epic(token, epic_id, story_id, order)`

Links a User Story to an Epic with a specific order.

**Parameters:**
- `token` (str): Authentication token
- `epic_id` (int): ID of the Epic to link to
- `story_id` (int): ID of the User Story to link
- `order` (int): Order position for the User Story

**Returns:** `dict` - Link creation response

**Example:**
```python
link = link_story_to_epic(
    token=token,
    epic_id=123,
    story_id=789,
    order=1
)
```

**API Endpoint:** `POST {TAIGA_URL}/epics/{epic_id}/related_userstories`

**Request Body:**
```json
{
    "epic": 123,
    "user_story": 789,
    "order": 1
}
```

**Response:**
```json
{
    "epic": 123,
    "user_story": 789,
    "order": 787
}
```

## Configuration Variables

### Taiga API Configuration

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `TAIGA_URL` | str | Base URL for Taiga API | `"http://10.5.216.7:8000/api/v1"` |
| `USERNAME` | str | Taiga username for authentication | `"your_username"` |
| `PASSWORD` | str | Taiga password for authentication | `"your_password"` |
| `PROJECT_ID` | int | Target project ID where Epic/Stories will be created | `63` |

### Epic Configuration

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `PROJECT_NAME` | str | Logical project name (used in Epic naming) | `"X3570"` |
| `LINE_NAME` | str | Production line identifier | `"L1_AOI"` |
| `ERROR_TYPE` | str | Error category/type | `"error1"` or `"Parameter"` |
| `ERROR_DESC` | str | Short error description | `"Threshold"` or `"Threshold exceeded"` |
| `QUANTITY` | int | Number of affected units/issues | `15` |
| `INSPECTION_METHOD` | str | How the problem was detected | `"Automated AOI system"` |

## Data Structures

### Epic Structure
```python
{
    "id": 123,                              # Unique Epic ID
    "ref": 456,                            # Epic reference number
    "subject": "Epic_Name_20250115_a1b2",   # Epic title
    "description": "5W2H formatted text",   # Epic description
    "project": 63,                         # Project ID
    "created_date": "2025-01-15T10:30:00Z", # Creation timestamp
    "modified_date": "2025-01-15T10:30:00Z" # Last modification timestamp
}
```

### User Story Structure
```python
{
    "id": 789,                             # Unique Story ID
    "ref": 101,                           # Story reference number
    "subject": "D0: Plan",                 # Story title
    "description": "Story description text", # Story description
    "project": 63,                        # Project ID
    "created_date": "2025-01-15T10:30:00Z", # Creation timestamp
    "modified_date": "2025-01-15T10:30:00Z" # Last modification timestamp
}
```

### User Stories Template (D0-D8)

The script creates 9 User Stories following the 8D methodology:

| D# | Title | Description |
|----|-------|-------------|
| D0 | Plan | Plan for solving the problem and determine the prerequisites |
| D1 | Establish a team | Select a team with product/process knowledge |
| D2 | Define and describe the problem | Specify the problem using 5W2H methodology |
| D3 | Develop and execute interim containment plan | Define and implement containment actions |
| D4 | Determine, identify, and verify root causes | Identify all applicable causes and verification methods |
| D5 | Choose and verify permanent corrections]

Generate the next part of the completion:

```python
{
    "id": 789,                             # Unique Story ID  
    "ref": 101,                           # Story reference number
    "subject": "D5: Choose and verify permanent corrections]", # Story title
    "description": "Identify the corrective action and, through preproduction programs, quantitatively confirm the selected correction will resolve the problem.", # Story description
    "project": 63,                        # Project ID
    "created_date": "2025-01-15T10:30:00Z", # Creation timestamp
    "modified_date": "2025-01-15T10:30:00Z" # Last modification timestamp
}
```

## Error Handling

### HTTP Status Codes

The script handles various HTTP status codes:

- **200/201**: Success
- **400**: Bad Request (check Epic naming, project configuration)
- **401**: Unauthorized (check credentials)
- **403**: Forbidden (check permissions)
- **404**: Not Found (check project ID, Epic/Story IDs)
- **500**: Internal Server Error (check Taiga server status)

### Exception Handling

All API calls use `raise_for_status()` to catch HTTP errors:

```python
r.raise_for_status()  # Raises HTTPError for bad status codes
```

### Debug Logging

The `link_story_to_epic()` function includes debug output:

```python
print(f"\n➡️ Linking Story {story_id} to Epic {epic_id} with payload: {data}")
# ... API call ...
if r.status_code not in (200, 201):
    print(f"❌ Failed linking (HTTP {r.status_code})")
    print("Response:", r.text)
else:
    print(f"✅ Linked successfully (HTTP {r.status_code})")
```

## Rate Limiting

Currently, the script does not implement rate limiting. If you encounter rate limiting issues:

1. Add delays between API calls
2. Implement exponential backoff
3. Check Taiga server configuration for API limits

## Security Considerations

### Credential Storage

⚠️ **Security Warning**: The current implementation stores credentials in plain text. For production use:

1. Use environment variables
2. Implement secure credential vault
3. Avoid committing credentials to version control

### API Token Management

- Tokens are session-based and expire
- Store tokens securely if reusing sessions
- Implement token refresh for long-running processes

## Examples

### Complete Workflow Example

```python
# 1. Authenticate
token = taiga_auth()

# 2. Create Epic
epic_data = {
    "project": 63,
    "subject": "X3570_L1_AOI_error1_Threshold_20250115_a1b2",
    "description": "📌 **5W2H Problem Description**..."
}
epic = requests.post(f"{TAIGA_URL}/epics", json=epic_data, headers={
    "Authorization": f"Bearer {token}"
})

# 3. Create User Stories
stories = []
for title, desc in USER_STORIES:
    story_data = {
        "project": 63,
        "subject": title,
        "description": desc
    }
    story = requests.post(f"{TAIGA_URL}/userstories", json=story_data, headers={
        "Authorization": f"Bearer {token}"
    })
    stories.append(story.json())

# 4. Link Stories to Epic
for i, story in enumerate(stories, 1):
    link_data = {
        "epic": epic.json()["id"],
        "user_story": story["id"],
        "order": i
    }
    requests.post(f"{TAIGA_URL}/epics/{epic.json()['id']}/related_userstories", 
                 json=link_data, headers={"Authorization": f"Bearer {token}"})
```

---

**Last Updated:** January 2025
