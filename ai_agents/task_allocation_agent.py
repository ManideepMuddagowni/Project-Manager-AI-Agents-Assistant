import json
from config import query_groq
from utils.json_utils import extract_json_array

def task_allocation_node(state):
    tasks = state.get("tasks", [])
    team = state.get("team", [])
    schedule = state.get("schedule", [])
    insights = state.get("insights", [])

    prompt = f"""
You are a proficient project manager responsible for allocating tasks to team members efficiently.

Given the following:

Tasks:
{json.dumps(tasks, indent=2)}

Schedule:
{json.dumps(schedule, indent=2)}

Team members and their skills:
{json.dumps(team, indent=2)}

Previous Insights:
{insights}



Your objectives:
1. Allocate each task to one or more team members:
   - Match tasks with appropriate skills.
   - Ensure no overlapping task assignments for a team member in the same time period.
   - Only assign one task at a time to any team member.

2. Optimize assignments:
   - Use previous insights to improve task distribution.
   - Balance workload fairly to prevent overloading team members.
   **Constraints:** 
                    - Each team member can handle only one task at a time. 
                    - Assignments should respect the skills and experience of each team member.

Output:
A JSON array of task assignments with the following fields:
  - "task": task name
  - "assigned_to": list of team member names

IMPORTANT: Output ONLY valid JSON, no explanations.

Example:
[
  {{"task": "Task A", "assigned_to": ["Alice", "Bob"]}},
  {{"task": "Task B", "assigned_to": ["Charlie"]}}
]

Begin output below:
"""

    response = query_groq(prompt)
    allocations = extract_json_array(response)
    if allocations is None:
        allocations = []

    return {
        "response": response,
        "task_allocations": allocations
    }
