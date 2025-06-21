from config import query_groq
import json
def risk_assessment_node(state):
    schedule = state.get("schedule", [])
    allocations = state.get("task_allocations", [])

    prompt = f"""
You are a seasoned project risk analyst tasked with evaluating the risks associated with the current project plan.

Given the following information:


Allocations:
{allocations}

Schedule:
{schedule}



Your objectives are to:

1. **Assess Risks:**
   - Analyze each task based on its complexity, assigned team member(s), and scheduled timeline.
   - Identify potential risks due to tight schedules, back-to-back assignments, overbooking, or dependency issues.

2. **Assign Risk Scores:**
   - Assign a risk score from 0 (no risk) to 10 (high risk) for each task.
   - If the same task was previously assigned to the same person/team with the same schedule, retain the previous risk score for consistency.
   - If a team member has more buffer time between tasks, reduce the risk score.
   - If a task is assigned to a more senior or experienced team member, reduce the risk score.

3. **Calculate Overall Project Risk:**
   - Sum all individual task risk scores to determine the overall project risk score.

IMPORTANT: Output must be plain text only — no JSON, no markdown, no bullet points.

Begin output below:
"""


    response = query_groq(prompt)

    # Return only the raw response text, no parsing or keys except response
    return {
        "response": response,
        "risks": [],
        "project_risk_score": None,
    }
