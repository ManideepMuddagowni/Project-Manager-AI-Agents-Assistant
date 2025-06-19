from groq import Groq
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def query_groq(prompt):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
    )
    return completion.choices[0].message.content

def parse_skills(profile_desc):
    if not profile_desc:
        return []
    skills = [skill.strip().lower() for skill in profile_desc.replace(";", ",").split(",") if skill.strip()]
    return skills



def generate_complete_project_csv(state):
    tasks_df = pd.DataFrame(state.get("tasks", []))
    dependencies_df = pd.DataFrame(state.get("dependencies", []))
    schedule_df = pd.DataFrame(state.get("schedule", []))
    allocations_df = pd.DataFrame(state.get("task_allocations", []))
    risks_df = pd.DataFrame(state.get("risks", []))

    tasks_df = tasks_df.rename(columns={"name": "task"})
    schedule_df = schedule_df.rename(columns={"name": "task"})

    merged_df = tasks_df.merge(dependencies_df, left_on="task", right_on="task", how="left")
    merged_df = merged_df.merge(schedule_df, on="task", how="left")
    merged_df = merged_df.merge(allocations_df, left_on="task", right_on="task", how="left")
    merged_df = merged_df.merge(risks_df, on=["task", "member"], how="left")

    for col in ["blocking_tasks", "dependent_tasks"]:
        if col not in merged_df.columns:
            merged_df[col] = ""
    for col in ["start_day", "end_day", "duration_days", "score"]:
        if col not in merged_df.columns:
            merged_df[col] = None
    if "member" not in merged_df.columns:
        merged_df["member"] = ""

    cols_order = [
        "task",
        "duration_days",
        "start_day",
        "end_day",
        "member",
        "score",
        "blocking_tasks",
        "dependent_tasks",
    ]
    merged_df = merged_df[cols_order]

    member_files = {}
    for member, group_df in merged_df.groupby("member"):
        filename = f"{member.lower().replace(' ', '_')}_tasks.csv" if member else "unassigned_tasks.csv"
        csv_bytes = group_df.to_csv(index=False).encode("utf-8")
        member_files[filename] = csv_bytes

    return member_files
