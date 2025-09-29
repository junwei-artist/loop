#!/usr/bin/env python3
import requests
import uuid
from datetime import datetime

# --- Taiga API config ---
TAIGA_URL = "http://10.5.216.7:8000/api/v1"
USERNAME = "shopfloor"
PASSWORD = "shopfloor"
PROJECT_ID = 63   # existing project

# --- Custom config for Epic naming ---
PROJECT_NAME = "X3570"                   # logical project name
LINE_NAME = "L1_AOI"                  # production line
ERROR_TYPE = "error1"                 # e.g. "Parameter", "Hardware", "Software"
ERROR_DESC = "Threshold"        # short description
QUANTITY = 15                            # how many units/issues observed
INSPECTION_METHOD = "Automated AOI system"  # how the problem was detected

# --- Generate Epic name dynamically ---
DATE_STR = datetime.now().strftime("%Y%m%d")
UUID_STR = uuid.uuid4().hex[:4]
# sanitize error desc for the name (replace spaces with _)
ERROR_DESC_NAME = ERROR_DESC.replace(" ", "_")
EPIC_NAME = f"{PROJECT_NAME}_{LINE_NAME}_{ERROR_TYPE}_{ERROR_DESC_NAME}_{DATE_STR}_{UUID_STR}"

# --- Generate Epic description (5W2H) ---
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

# --- D0–D8 as User Stories ---
USER_STORIES = [
    ("D0: Plan", "Plan for solving the problem and determine the prerequisites."),
    ("D1: Establish a team", "Select a team with product/process knowledge."),
    ("D2: Define and describe the problem",
     "Define and describe the problem—Specify the problem by identifying in quantifiable terms "
     "the who, what, where, when, why, how, and how many (5W2H) of the problem."),
    ("D3: Develop and execute an interim containment plan",
     "Define and implement containment actions to isolate the problem."),
    ("D4: Determine, identify, and verify root causes",
     "Identify all applicable causes that could explain why the problem occurred. Also identify why "
     "the problem went unnoticed when it occurred. All causes should be verified or proved, not "
     "determined by fuzzy brainstorming. Five whys and cause and effect diagrams can be used to map "
     "causes against the identified effect or problem."),
    ("D5: Choose and verify permanent corrections",
     "Identify the corrective action and, through preproduction programs, quantitatively confirm "
     "the selected correction will resolve the problem."),
    ("D6: Implement and validate corrective actions",
     "Implement the selected corrective action and verify its effectiveness."),
    ("D7: Congratulate the team",
     "Modify the management systems, operation systems, practices, and procedures to prevent "
     "recurrence of this as well as all similar problems."),
    ("D8: Congratulate your team",
     "Recognize the team’s collective efforts. The team must be thanked formally by the organization."),
]

# --- Auth ---
def taiga_auth():
    r = requests.post(f"{TAIGA_URL}/auth", json={
        "type": "normal",
        "username": USERNAME,
        "password": PASSWORD
    })
    r.raise_for_status()
    return r.json()["auth_token"]

# --- Create Epic ---
def create_epic(token, project_id, subject, description=""):
    headers = {"Authorization": f"Bearer {token}"}
    epic_data = {
        "project": project_id,
        "subject": subject,
        "description": description
    }
    r = requests.post(f"{TAIGA_URL}/epics", json=epic_data, headers=headers)
    r.raise_for_status()
    return r.json()

# --- Create User Story ---
def create_user_story(token, project_id, subject, description):
    headers = {"Authorization": f"Bearer {token}"}
    story_data = {
        "project": project_id,
        "subject": subject,
        "description": description
    }
    r = requests.post(f"{TAIGA_URL}/userstories", json=story_data, headers=headers)
    r.raise_for_status()
    return r.json()

# --- Link User Story to Epic (debug enabled) ---
def link_story_to_epic(token, epic_id, story_id, order):
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "epic": epic_id,
        "user_story": story_id,
        "order": order
    }
    url = f"{TAIGA_URL}/epics/{epic_id}/related_userstories"

    print(f"\n➡️ Linking Story {story_id} to Epic {epic_id} with payload: {data}")
    r = requests.post(url, json=data, headers=headers)

    if r.status_code not in (200, 201):
        print(f"❌ Failed linking (HTTP {r.status_code})")
        print("Response:", r.text)
    else:
        print(f"✅ Linked successfully (HTTP {r.status_code})")

    r.raise_for_status()
    return r.json()

# --- Main ---
def main():
    print(f"🔑 Authenticating as {USERNAME}...")
    token = taiga_auth()
    print("✅ Auth success")

    print(f"📦 Creating epic: {EPIC_NAME} in project {PROJECT_ID}...")
    epic = create_epic(token, PROJECT_ID, EPIC_NAME, EPIC_DESCRIPTION)
    epic_id = epic["id"]
    print(f"✅ Epic created (ID {epic_id}, Ref {epic['ref']})")

    print("📌 Creating and linking user stories...")
    for i, (subject, description) in enumerate(USER_STORIES, start=1):
        story = create_user_story(token, PROJECT_ID, subject, description)
        link_story_to_epic(token, epic_id, story["id"], order=i)
        print(f"   → Story created and attempted link: {story['subject']} (Story ID {story['id']})")

    print("\n🎉 Done! Check above logs for link status.")

if __name__ == "__main__":
    main()