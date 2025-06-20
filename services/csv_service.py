import pandas as pd
import streamlit as st

def parse_csv(file):
    df = pd.read_csv(file)
    team = []
    if 'Name' not in df.columns or 'Profile Description' not in df.columns:
        st.error("CSV must have columns: 'Name' and 'Profile Description'")
        return []
    for _, row in df.iterrows():
        name = str(row['Name']).strip()
        profile = str(row['Profile Description']).strip()
        skills = [skill.strip() for skill in profile.split(",") if skill.strip()]
        team.append({"name": name, "skills": skills})
    return team

def create_output_csv(team_data, airtable_table):
    output_data = []
    for member in team_data:
        name = member["name"]
        record = airtable_table.all(formula=f"{{Name}}='{name}'")
        if not record:
            continue
        fields = record[0]["fields"]
        output_data.append({
            "Name": name,
            "Profile Description": ", ".join(member["skills"]),
            "Assigned Tasks": fields.get("Assigned Tasks", ""),
            "Schedule": fields.get("Schedule", ""),
            "Dependencies": fields.get("Dependencies", ""),
            "Risk": fields.get("Risk", ""),
            "Insights": fields.get("Insights", ""),
        })
    return pd.DataFrame(output_data)
