import json
from config import query_groq
from utils.json_utils import extract_json_array

def task_scheduler_node(state):
    tasks = state.get("tasks", [])
    dependencies = state.get("dependencies", [])
    insights = state.get("insights", [])

    prompt = f"""
You are an experienced project scheduler tasked with creating an optimized project timeline.

Given:
Tasks:
{json.dumps(tasks, indent=2)}

Dependencies:
{json.dumps(dependencies, indent=2)}

Previous Insights:
{insights}

Your task:
1. Develop a task schedule that:
   - Assigns "start_day" and "end_day" to each task.
   - Respects all task dependencies.
   - Minimizes the overall project duration by parallelizing tasks where possible.
   - Avoids increasing total duration compared to previous iterations.
   - Incorporates lessons from previous insights to address scheduling inefficiencies.

2. Output a JSON array of scheduled tasks with the following fields:
   - "name": task name
   - "start_day": integer, day number task starts
   - "end_day": integer, day number task ends

IMPORTANT: Output ONLY valid JSON, no explanations, no extra text.

Example:
[
  {{ "name": "Task A", "start_day": 1, "end_day": 3 }},
  {{ "name": "Task B", "start_day": 2, "end_day": 4 }}
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


