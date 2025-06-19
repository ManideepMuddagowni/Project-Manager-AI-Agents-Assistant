import json
from config import query_groq
from utils.json_utils import extract_json_array

def risk_assessment_node(state):
    tasks = state.get("tasks", [])
    allocations = state.get("task_allocations", [])

    prompt = f"""
Given the tasks and their allocations:

Tasks:
{json.dumps(tasks, indent=2)}

Allocations:
{json.dumps(allocations, indent=2)}

Your task:
1. Assess potential risks and bottlenecks.
2. Provide a risk score between 1 (low) and 10 (high) for each task.
3. Output a JSON object with two keys:
   - "risks": array of objects with "task" and "risk_score"
   - "project_risk_score": integer between 1 and 10

IMPORTANT: Output ONLY valid JSON with two keys:
- "risks": array of task risk objects
- "project_risk_score": integer
No explanations, no markdown formatting, only JSON.

Example:
{{
  "risks": [
    {{"task": "Task A", "risk_score": 4}},
    {{"task": "Task B", "risk_score": 7}}
  ],
  "project_risk_score": 6
}}

Begin output below:
"""
    response = query_groq(prompt)

    risk_data = extract_json_array(response)
    if risk_data is None:
        try:
            risk_data = json.loads(response.strip())
        except json.JSONDecodeError:
            risk_data = {"risks": [], "project_risk_score": 0}

    return {
        "response": response,
        "risks": risk_data.get("risks", []),
        "project_risk_score": risk_data.get("project_risk_score", 0)
    }
