# utils.py
import pandas as pd
import json
import re

def parse_skills(profile_desc):
    if pd.isna(profile_desc):
        return []
    skills = [skill.strip().lower() for skill in profile_desc.replace(";", ",").split(",") if skill.strip()]
    return skills

def extract_json_array(text):
    # Use regex to find the first JSON array in the text
    pattern = re.compile(r'(\[.*\])', re.DOTALL)
    match = pattern.search(text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None

def json_to_csv_bytes(data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')
