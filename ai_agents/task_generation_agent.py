import json
import streamlit as st
from config import query_groq
from utils.json_utils import extract_json_array

def task_generation_node(state):
    description = state.get("project_description", "")
    prompt = f"""
You are an expert project manager analyzing the following project description:

{description}

Your task:
1. Extract actionable and realistic tasks necessary to complete the project.
2. Provide an estimated number of days required to complete each task.
3. Break down any task longer than 5 days into smaller, independent sub-tasks.

IMPORTANT: Output ONLY valid JSON, nothing else. No explanations, no text, no commentary.

Output a JSON array of task objects with these fields:
- "name": string, task name
- "duration_days": integer, estimated duration

Example:
[
  {{"name": "Task A", "duration_days": 3}},
  {{"name": "Task B", "duration_days": 7}}
]

If no tasks, output an empty array [].

Begin output below:
"""
    response = query_groq(prompt)
    st.code(response, language='json')

    tasks = extract_json_array(response)
    if tasks is None:
        tasks = []

    return {"tasks": tasks}
