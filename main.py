import streamlit as st
import pandas as pd
import io

from utils.json_utils import extract_json_array
from ai_agents.task_generation_agent import task_generation_node
from ai_agents.task_allocation_agent import task_allocation_node
from ai_agents.task_dependency_agent import task_dependency_node
from ai_agents.task_scheduler_agent import task_scheduler_node
from ai_agents.risk_assesment_agent import risk_assessment_node
from ai_agents.insight_generation import insight_generation_node

# --- Utility: parse uploaded CSV ---
def parse_csv(file):
    df = pd.read_csv(file)
    team = []
    if 'Name' not in df.columns or 'Profile Description' not in df.columns:
        st.error("CSV must have columns: 'Name' and 'Profile Description'")
        return []
    for _, row in df.iterrows():
        name = str(row['Name']).strip()
        profile = str(row['Profile Description']).strip()
        skills = [skill.strip().lower() for skill in profile.split(",") if skill.strip()]
        team.append({"name": name, "skills": skills})
    return team

# --- Utility: styled box ---
def style_result_box(color):
    return f"""
        <div style="
            background-color: {color};
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            white-space: pre-wrap;
            overflow-x: auto;
        ">
    """

def close_div():
    return "</div>"

# --- Workflow steps ---
agents = [
    "Task Generation",
    "Task Dependency Identification",
    "Task Scheduling",
    "Task Allocation",
    "Risk Assessment",
    "Insight Generation"
]

def get_status_md(current_step):
    status_md = "### 🧭 Agent Workflow Progress\n"
    for idx, agent in enumerate(agents):
        if idx < current_step:
            status_md += f"✅ **{agent}** completed\n"
        elif idx == current_step:
            status_md += f"🟡 **{agent}** running...\n"
        else:
            status_md += f"⚪️ {agent} pending\n"
    return status_md

# --- Main App ---
st.set_page_config(layout="wide")
st.title("🧠 Project Management AI Agent with CSV Upload")

# CSV Upload
uploaded_file = st.file_uploader("Upload CSV with 'Name' and 'Profile Description'", type=["csv"])
if uploaded_file:
    team_data = parse_csv(uploaded_file)
    if team_data:
        st.session_state.team = team_data
        st.success(f"Loaded {len(team_data)} team members from CSV")

# Project Description Input
if "project_description" not in st.session_state:
    st.session_state.project_description = ""
st.session_state.project_description = st.text_area(
    "Enter Project Description:",
    value=st.session_state.project_description,
    height=150,
)

# Container to show workflow status
status_container = st.empty()

if st.button("🚀 Submit and Run Workflow"):
    if "team" not in st.session_state or not st.session_state.team:
        st.error("Please upload a valid CSV first.")
        st.stop()
    if not st.session_state.project_description.strip():
        st.error("Please enter a project description.")
        st.stop()

    state = {"project_description": st.session_state.project_description}

    # Step 1: Task Generation
    status_container.markdown(get_status_md(0))
    with st.container():
        st.markdown("### 🧠 Task Generation Agent")
        st.markdown(style_result_box("#FFF3CD"), unsafe_allow_html=True)
        task_data = task_generation_node(state)
        st.markdown(close_div(), unsafe_allow_html=True)
    st.session_state.tasks = task_data.get("tasks", [])

    # Step 2: Task Dependency Identification
    status_container.markdown(get_status_md(1))
    with st.container():
        st.markdown("### 🔗 Task Dependency Agent")
        st.markdown(style_result_box("#D1ECF1"), unsafe_allow_html=True)

        dep_data = task_dependency_node({"tasks": st.session_state.tasks})

        # Show raw AI response for debugging
        st.markdown("**Raw AI Response:**")
        st.code(dep_data.get("response", "No response"), language="json")

        dependencies = dep_data.get("dependencies", [])
        if not dependencies:
            st.warning("No dependencies extracted or parsing failed.")
        else:
            # Display parsed dependencies nicely
            df_deps = pd.DataFrame(dependencies)
            st.dataframe(df_deps)

        st.markdown(close_div(), unsafe_allow_html=True)

    st.session_state.dependencies = dependencies

    # Step 3: Task Scheduling
    status_container.markdown(get_status_md(2))
    with st.container():
        st.markdown("### 📅 Task Scheduler Agent")
        st.markdown(style_result_box("#CCE5FF"), unsafe_allow_html=True)
        sched_data = task_scheduler_node({
            "tasks": st.session_state.tasks,
            "dependencies": st.session_state.dependencies,
        })
        st.json(sched_data.get("schedule", []))
        st.markdown(close_div(), unsafe_allow_html=True)
    st.session_state.schedule = sched_data.get("schedule", [])

    # Step 4: Task Allocation
    status_container.markdown(get_status_md(3))
    with st.container():
        st.markdown("### 👥 Task Allocation Agent")
        st.markdown(style_result_box("#D4EDDA"), unsafe_allow_html=True)
        alloc_data = task_allocation_node({
            "tasks": st.session_state.tasks,
            "team": st.session_state.team,
        })
        st.json(alloc_data.get("task_allocations", []))
        st.markdown(close_div(), unsafe_allow_html=True)
    st.session_state.task_allocations = alloc_data.get("task_allocations", [])

    # Step 5: Risk Assessment
    status_container.markdown(get_status_md(4))
    with st.container():
        st.markdown("### ⚠️ Risk Assessment Agent")
        st.markdown(style_result_box("#F8D7DA"), unsafe_allow_html=True)

        risk_data = risk_assessment_node({
            "tasks": st.session_state.tasks,
            "task_allocations": st.session_state.task_allocations,
        })

        # Show raw response for debugging
        st.markdown("**Raw AI Response:**")
        st.code(risk_data.get("response", "No response"), language="json")

        # Show parsed JSON risks and score
        st.json(risk_data.get("risks", []))
        st.write(f"**Overall Project Risk Score:** {risk_data.get('project_risk_score', 0)}")

        st.markdown(close_div(), unsafe_allow_html=True)

    st.session_state.risks = risk_data.get("risks", [])
    st.session_state.project_risk_score = risk_data.get("project_risk_score", 0)

    # Step 6: Insight Generation
    status_container.markdown(get_status_md(5))
    with st.container():
        st.markdown("### 📊 Insight Generation Agent")
        st.markdown(style_result_box("#E2E3E5"), unsafe_allow_html=True)
        insights = insight_generation_node({
            "project_description": st.session_state.project_description,
            "tasks": st.session_state.tasks,
            "schedule": st.session_state.schedule,
            "task_allocations": st.session_state.task_allocations,
            "risks": st.session_state.risks,
        })
        st.write(insights)
        st.markdown(close_div(), unsafe_allow_html=True)
    st.session_state.insights = insights

    # Final step complete - show completion after all done
    status_container.markdown(get_status_md(len(agents)))
    st.success("🎉 Workflow completed successfully!")
    st.balloons()

# --- Tabs to show persistent results ---
tabs = st.tabs([
    "🧠 Task Generation",
    "🔗 Task Dependencies",
    "📅 Scheduling",
    "👥 Allocation",
    "⚠️ Risk Assessment",
    "📊 Insights"
])

with tabs[0]:
    st.header("Task Generation Agent Results")
    if "tasks" in st.session_state:
        st.json(st.session_state.tasks)
    else:
        st.info("Run the workflow to generate tasks.")

with tabs[1]:
    st.header("Task Dependency Agent Results")
    if "dependencies" in st.session_state:
        df_deps = pd.DataFrame(st.session_state.dependencies)
        st.dataframe(df_deps)
    else:
        st.info("Run the workflow to identify dependencies.")

with tabs[2]:
    st.header("Task Scheduler Agent Results")
    if "schedule" in st.session_state:
        st.json(st.session_state.schedule)
    else:
        st.info("Run the workflow to get schedule.")

with tabs[3]:
    st.header("Task Allocation Agent Results")
    if "task_allocations" in st.session_state:
        st.json(st.session_state.task_allocations)
    else:
        st.info("Run the workflow to allocate tasks.")

with tabs[4]:
    st.header("Risk Assessment Agent Results")
    if "risks" in st.session_state and "project_risk_score" in st.session_state:
        st.json(st.session_state.risks)
        st.write(f"**Overall Project Risk Score:** {st.session_state.project_risk_score}")
    else:
        st.info("Run the workflow to assess risks.")

with tabs[5]:
    st.header("Insight Generation Agent Results")
    if "insights" in st.session_state:
        st.write(st.session_state.insights)
    else:
        st.info("Run the workflow to generate insights.")
