# Troubleshooting Guide

## Common Issues and Solutions

### Authentication Problems

#### Issue: HTTP 401 Unauthorized
```
Error: HTTP 401 Unauthorized
```

**Solutions:**
1. **Verify credentials**: Check username and password
2. **Check URL format**: Ensure Taiga URL ends with `/api/v1`
3. **Account status**: Verify account is active and not locked
4. **Server access**: Confirm Taiga server is accessible

**Debug steps:**
```python
# Test basic connectivity
import requests
try:
    response = requests.get(f"{TAIGA_URL}/")
    print(f"Server response: {response.status_code}")
except Exception as e:
    print(f"Connection error: {e}")
```

#### Issue: HTTP 403 Forbidden
```
Error: HTTP 403 Forbidden
```

**Solutions:**
1. **Check permissions**: Ensure user has Epic/Story creation rights
2. **Project access**: Verify access to target project
3. **Role verification**: Check user role in project

### Epic Creation Issues

#### Issue: HTTP 400 Bad Request on Epic Creation
```
Error: HTTP 400 Bad Request
Response: {"subject": ["This field is required."]}
```

**Solutions:**
1. **Check Epic name**: Ensure `EPIC_NAME` is not empty
2. **Special characters**: Remove invalid characters from naming fields
3. **Name length**: Check Epic name doesn't exceed Taiga limits
4. **Project validation**: Verify PROJECT_ID is valid

**Debug Epic name:**
```python
print(f"Epic name: '{EPIC_NAME}'")
print(f"Name length: {len(EPIC_NAME)}")
print(f"Has special chars: {not EPIC_NAME.replace('_', '').replace('-', '').isalnum()}")
*/

#### Issue: Epic Created But User Stories Failed
```
✅ Epic created (ID 123)
❌ Failed creating story: HTTP 500
```

**Solutions:**
1. **Project configuration**: Check if project allows User Story creation
2. **Permissions**: Verify user can create stories in project
3. **Epic existence**: Confirm Epic was actually created

### User Story Linking Issues

#### Issue: HTTP 500 on Story Linking
```
❌ Failed linking (HTTP 500)
Response: {"epic": ["This epic doesn't exist."]}
```

**Solutions:**
1. **Epic verification**: Check Epic ID is correct and Epic exists
2. **Project consistency**: Ensure Epic and Stories are in same project
3. **Timing issues**: Add delay before linking if using rapid creation

**Fix with delay:**
```python
import time

# Add delay between Epic creation and linking
epic = create_epic(token, PROJECT_ID, EPIC_NAME, EPIC_DESCRIPTION)
time.sleep(2)  # Wait 2 seconds
epic_id = epic["id"]
```

#### Issue: Story Linking Returns Wrong Order
```
✅ Linked successfully (HTTP 200)
# But order appears incorrect in Taiga UI
```

**Solutions:**
1. **Order field**: Verify `order` parameter is being set correctly
2. **Taiga configuration**: Check project settings for story ordering
3. **Manual adjustment**: Set orders explicitly after creation

**Explicit order setting:**
```python
for i, (subject, description) in enumerate(USER_STORIES, start=100):
    story = create_user_story(token, PROJECT_ID, subject, description)
    link_story_to_epic(token, epic_id, story["id"], order=i)
```

### Network and Connection Issues

#### Issue: Connection Timeout
```
Error: requests.exceptions.ConnectTimeout
```

**Solutions:**
1. **Network connectivity**: Check internet/VPN connection
2. **Firewall settings**: Verify firewall allows connection to Taiga
3. **Server status**: Confirm Taiga server is running
4. **Increase timeout**: Add longer timeout values

**Network debugging:**
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure retry strategy
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)
```

#### Issue Response Parsing Errors
```
Error: 'Response' object has no attribute 'json'
```

**Solutions:**
1. **Check response**: Verify API returned valid JSON
2. **Handle empty responses**: Add null checks
3. **Parse errors**: Implement better error handling

**Safer response parsing:**
```python
def safe_json_response(response):
    """Safely parse JSON response with error handling"""
    try:
        if response.status_code in (200, 201):
            return response.json()
        else:
            print(f"HTTP {response.status_code}: {response.text}")
            return None
    except ValueError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response content: {response.text}")
        return None
```

## Debugging Techniques

### Enable Detailed Logging

```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Setup HTTP request logging
import http.client
http.client.HTTPConnection.debuglevel = 1
```

### Test Individual Components

```python
def test_auth_only():
    """Test only authentication"""
    try:
        token = taiga_auth()
        print(f"✅ Auth successful, token: {token[:10]}...")
        return token
    except Exception as e:
        print(f"❌ Auth failed: {e}")
        return None

def test_project_access(token):
    """Test project access without creation"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{TAIGA_URL}/projects/{PROJECT_ID}", headers=headers)
        if response.status_code == 200:
            project_data = response.json()
            print(f"✅ Project access: {project_data['name']}")
            return True
        else:
            print(f"❌ Project access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Project test error: {e}")
        return False
```

### Validate Configuration

```python
def validate_configuration():
    """Validate all configuration settings"""
    checks = [
        ("TAIGA_URL", TAIGA_URL, lambda x: x.startswith("http")),
        ("USERNAME", USERNAME, lambda x: len(x) > 0),
        ("PASSWORD", PASSWORD, lambda x: len(x) > 0),
        ("PROJECT_ID", PROJECT_ID, lambda x: isinstance(x, int) and x > 0),
        ("PROJECT_NAME", PROJECT_NAME, lambda x: len(x) > 0),
        ("LINE_NAME", LINE_NAME, lambda x: len(x) > 0),
    ]
    
    all_valid = True
    for name, value, check in checks:
        if check(value):
            print(f"✅ {name}: OK")
        else:
            print(f"❌ {name}: Invalid value '{value}'")
            all_valid = False
    
    return all_valid
```

## Performance Issues

### Rate Limiting

```python
import time

def with_rate_limit(func, *args, **kwargs):
    """Add rate limiting to API calls"""
    result = func(*args, **kwargs)
    time.sleep(1)  # Wait 1 second between calls
    return result

# Usage
story = with_rate_limit(create_user_story, token, PROJECT_ID, subject, description)
```

### Memory Optimization

```python
def create_stories_batch(token, project_id, stories_data):
    """Create multiple stories in a single request"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Prepare batch data
    batch_data = []
    for subject, description in stories_data:
        batch_data.append({
            "project": project_id,
            "subject": subject,
            "description": description
        })
    
    # Send batch request (if supported by Taiga API)
    response = requests.post(f"{TAIGA_URL}/userstories/bulk", 
                           json=batch_data, headers=headers)
    return response.json()
```

## Error Recovery

### Retry Mechanism

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """Decorator to retry failed operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"Attempt {attempt + 1} failed: {e}, retrying...")
                        time.sleep(delay * (attempt + 1))
                    else:
                        raise e
            return None
        return wrapper
    return decorator

# Usage
@retry_on_failure(max_retries=3, delay=2)
def create_epic_with_retry(token, project_id, subject, description):
    return create_epic(token, project_id, subject, description)
```

### Partial Recovery

```python
def create_epic_with_graceful_degradation():
    """Create Epic and as many stories as possible"""
    token = taiga_auth()
    epic = create_epic(token, PROJECT_ID, EPIC_NAME, EPIC_DESCRIPTION)
    epic_id = epic["id"]
    
    successful_stories = []
    failed_stories = []
    
    for i, (subject, description) in enumerate(USER_STORIES):
        try:
            story = create_user_story(token, PROJECT_ID, subject, description)
            link_story_to_epic(token, epic_id, story["id"], order=i+1)
            successful_stories.append(story["subject"])
        except Exception as e:
            failed_stories.append({"subject": subject, "error": str(e)})
    
    return {
        "epic": epic,
        "successful": successful_stories,
        "failed": failed_stories
    }
```

---

**Last Updated:** January 2025
