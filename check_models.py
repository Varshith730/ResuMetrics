import requests
import streamlit as st

key = st.secrets.get("GEMINI_API_KEY", "")
res = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={key}").json()
import json
with open("available_models.json", "w") as f:
    json.dump(res, f, indent=2)
print("Saved models to available_models.json")
