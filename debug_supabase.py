import os
import streamlit as st
from datetime import datetime
from supabase import create_client, Client

url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))

print(f"URL: {url}")
client = create_client(url, key)

payload = {
    "filename":          "Debug_Resume.pdf",
    "role_selected":     "Data Scientist",
    "score":             8.5,
    "skills_count":      10,
    "experience_score":  7,
}

print("Attempting to insert payload:", payload)
try:
    resp = client.table("resumes").insert(payload).execute()
    print("Success:", resp)
except Exception as e:
    print("Exception details:")
    print(e)
    if hasattr(e, '__dict__'):
        print(e.__dict__)
