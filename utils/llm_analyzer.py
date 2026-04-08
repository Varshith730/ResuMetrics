"""
utils/llm_analyzer.py
Gemini LLM integration for contextual resume insights.
"""

from __future__ import annotations

import os
import json
import requests
import streamlit as st

def analyze_resume_context(resume_text: str, target_role: str) -> dict | None:
    """
    Passes the parsed raw resume text to Gemini to receive a structured JSON 
    about the candidate's holistic context using the raw REST API.
    """
    api_key = (
        st.secrets.get("GEMINI_API_KEY", "")
        if hasattr(st, "secrets")
        else os.getenv("GEMINI_API_KEY", "")
    )
    
    if not api_key:
        print("No API key found")
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    
    prompt = f"""
    You are an expert Executive IT Recruiter evaluating a candidate for the role of '{target_role}'.
    Review the following parsed resume text and provide a structured JSON response evaluating their fit.
    
    Respond STRICTLY with valid JSON matching this schema:
    {{
        "llm_summary": "A 2-3 sentence executive summary of the candidate's career trajectory and overall strength.",
        "llm_pros": ["Strong bullet 1", "Strong bullet 2", "Strong bullet 3"],
        "llm_cons": ["Weakness 1", "Weakness 2", "Weakness 3"],
        "llm_soft_skills": ["Skill 1", "Skill 2", "Skill 3"]
    }}
    
    Resume Text:
    {resume_text[:4000]}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }
    
    try:
        req = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        if req.status_code != 200:
            print(f"Gemini API Error: {req.text}")
            return None
            
        data = req.json()
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Super-simple JSON cleanup
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())
        
    except Exception as e:
        print(f"Gemini Fetch Error: {e}")
        return None
