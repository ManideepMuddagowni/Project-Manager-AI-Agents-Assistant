import streamlit as st
from config import query_groq

def insight_generation_node(state):
    schedule = state.get("schedule", [])
    allocations = state.get("task_allocations", [])
    risks = state.get("risks", [])

    prompt = f"""
        You are an expert project manager responsible for generating actionable insights to enhance the project plan.
        **Given:**
            - **Task Allocations:** {allocations}
            - **Schedule:** {schedule}
            - **Risk Analysis:** {risks}
        **Your objectives are to:**
            1. **Generate Critical Insights:**
            - Analyze the current task allocations, schedule, and risk assessments to identify areas for improvement.
            - Highlight any potential bottlenecks, resource conflicts, or high-risk tasks that may jeopardize project success.
            2. **Recommend Enhancements:**
            - Suggest adjustments to task assignments or scheduling to mitigate identified risks.
            - Propose strategies to optimize resource utilization and streamline workflow.
                **Requirements:**
                - Ensure that all recommendations aim to reduce the overall project risk score.
                - Provide clear and actionable suggestions that can be implemented in subsequent iterations.
    
Provide concise insights on potential bottlenecks, team utilization, risk hotspots, and recommendations.

Respond ONLY with plain text insights, no JSON.
"""
    insights = query_groq(prompt)
    return insights
