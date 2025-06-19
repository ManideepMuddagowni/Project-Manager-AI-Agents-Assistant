from config import query_groq

def risk_assessment_node(state):
    tasks = state.get("tasks", [])
    allocations = state.get("task_allocations", [])

    prompt = f"""
Given the tasks and their allocations:

Tasks:
{tasks}

Allocations:
{allocations}

Your task:
1. Assess potential risks and bottlenecks.
2. Provide a risk score between 1 (low) and 10 (high) for each task.
3. Output your answer as plain text only (no JSON).

IMPORTANT: No JSON, no markdown, just plain text explanation.

Begin output below:
"""

    response = query_groq(prompt)

    # Return only the raw response text, no parsing or keys except response
    return {
        "response": response,
        "risks": [],
        "project_risk_score": None,
    }
