import json
from config import query_groq
from utils.json_utils import extract_json_array

def task_allocation_node(state):
    tasks = state.get("tasks", [])
    team = state.get("team", [])

    prompt = f"""
Given the tasks and the team below:

Tasks:
{json.dumps(tasks, indent=2)}

Team members and their skills:
{json.dumps(team, indent=2)}

Your task:
1. Allocate each task to one or more team members with matching skills.
2. Output a JSON array with objects containing:
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
