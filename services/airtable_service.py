# airtable_utils.py
import os
from dotenv import load_dotenv
from pyairtable import Table
import streamlit as st

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY") or "your_api_key_here"
BASE_ID = os.getenv("AIRTABLE_BASE_ID") or "your_base_id_here"
TABLE_NAME = "Team Members"

def get_airtable_table():
    return Table(API_KEY, BASE_ID, TABLE_NAME)

def save_team_to_airtable(team_data):
    table = get_airtable_table()
    for member in team_data:
        existing = table.all(formula=f"{{Name}}='{member['name']}'")
        if existing:
            st.info(f"Member {member['name']} already exists, skipping creation.")
            continue
        try:
            table.create({
                "Name": member["name"],
                "Profile Description": ", ".join(member["skills"]),
            })
            st.success(f"Saved member {member['name']} to Airtable.")
        except Exception as e:
            st.error(f"Failed to save member {member['name']}: {e}")

def update_team_with_tasks(task_allocations, schedule, dependencies, risk_text, insights_text):
    table = get_airtable_table()
    member_updates = {}

    for task in task_allocations:
        assigned_to = task.get("assigned_to", [])
        if isinstance(assigned_to, str):
            assigned_to_list = [assigned_to] if assigned_to else []
        elif isinstance(assigned_to, list):
            assigned_to_list = assigned_to
        else:
            assigned_to_list = []

        for member_name in assigned_to_list:
            if member_name not in member_updates:
                member_updates[member_name] = {
                    "tasks": [],
                    "schedules": [],
                    "dependencies": []
                }
            member_updates[member_name]["tasks"].append(task.get("task", ""))

            sched_item = next(
                (item for item in schedule if item.get("task", "") == task.get("task", "")),
                {}
            )
            sched_str = sched_item.get("schedule", "")
            if sched_str:
                member_updates[member_name]["schedules"].append(sched_str)

            dep_list = [
                dep.get("depends_on", "") for dep in dependencies if dep.get("task", "") == task.get("task", "")
            ]
            flat_dep_list = []
            for d in dep_list:
                if isinstance(d, list):
                    flat_dep_list.extend(d)
                else:
                    flat_dep_list.append(d)
            member_updates[member_name]["dependencies"].extend(flat_dep_list)

    for member_name, info in member_updates.items():
        records = table.all(formula=f"{{Name}}='{member_name}'")
        if not records:
            st.warning(f"Member {member_name} not found in Airtable for update.")
            continue
        record_id = records[0]["id"]

        update_data = {
            "Assigned Tasks": ", ".join(sorted(set(info["tasks"]))),
            "Schedule": ", ".join(sorted(set(info["schedules"]))),
            "Dependencies": ", ".join(sorted(set(info["dependencies"]))),
            "Risk": risk_text,
            "Insights": insights_text,
        }
        try:
            table.update(record_id, update_data)
            st.success(f"Updated member {member_name} with tasks, schedule, dependencies, risk, and insights.")
        except Exception as e:
            st.error(f"Failed to update member {member_name}: {e}")

def clear_airtable_table():
    table = get_airtable_table()
    records = table.all()
    for record in records:
        try:
            table.delete(record['id'])
        except Exception as e:
            st.error(f"Failed to delete record {record['id']}: {e}")
