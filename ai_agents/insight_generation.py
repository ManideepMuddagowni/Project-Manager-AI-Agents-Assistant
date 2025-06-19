import streamlit as st
from config import query_groq

def insight_generation_node(state):
    project_description = state.get("project_description", "")
    tasks = state.get("tasks", [])
    schedule = state.get("schedule", [])
    allocations = state.get("task_allocations", [])
    risks = state.get("risks", [])

    prompt = f"""
You are a project analyst. Provide insights based on:

Project description:
{project_description}

Tasks:
{tasks}

Schedule:
{schedule}

Task allocations:
{allocations}

Risk assessment:
{risks}

Provide concise insights on potential bottlenecks, team utilization, risk hotspots, and recommendations.

Respond ONLY with plain text insights, no JSON.
"""
    insights = query_groq(prompt)
    return insights
