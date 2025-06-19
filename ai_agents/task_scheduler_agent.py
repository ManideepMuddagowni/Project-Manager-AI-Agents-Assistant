import json
from config import query_groq
from utils.json_utils import extract_json_array

def task_scheduler_node(state):
    tasks = state.get("tasks", [])
    dependencies = state.get("dependencies", [])

    prompt = f"""
Given the tasks and dependencies below:

Tasks:
{json.dumps(tasks, indent=2)}

Dependencies:
{json.dumps(dependencies, indent=2)}

Your task:
1. Schedule tasks considering dependencies.
2. Output a JSON array of scheduled tasks with fields:
   - "name": task name
   - "start_day": integer, day number task starts
   - "end_day": integer, day number task ends

IMPORTANT: Output ONLY valid JSON, no explanations.

Example:
[
  {{"name": "Task A", "start_day": 1, "end_day": 3}},
  {{"name": "Task B", "start_day": 4, "end_day": 7}}
]

Begin output below:
"""
    response = query_groq(prompt)
    schedule = extract_json_array(response)
    if schedule is None:
        schedule = []

    return {
        "response": response,
        "schedule": schedule
    }
