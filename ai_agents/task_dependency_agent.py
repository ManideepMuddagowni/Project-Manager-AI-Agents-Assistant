import json
from config import query_groq
from utils.json_utils import extract_json_array

def task_dependency_node(tasks):
    prompt = f"""
Given the following project tasks:

{json.dumps(tasks, indent=2)}

Your task:
1. Identify dependencies between tasks.
2. Output an array of dependency objects with "task" and "depends_on" fields.
3. "depends_on" is a list of task names that must be completed before the task.

IMPORTANT: Output ONLY valid JSON, no explanations, no extra text, no markdown formatting.

Example:
[
  {{"task": "Task B", "depends_on": ["Task A"]}},
  {{"task": "Task C", "depends_on": []}}
]

Begin output below:
"""
    response = query_groq(prompt)
    dependencies = extract_json_array(response)
    if dependencies is None:
        # fallback: try to parse whole response as JSON (strip whitespace)
        try:
            dependencies = json.loads(response.strip())
        except Exception:
            dependencies = []
    return {
        "response": response,
        "dependencies": dependencies
    }
