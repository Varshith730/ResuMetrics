"""
utils/database.py
Supabase integration for the AI Resume Intelligence Platform.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any

import streamlit as st


# ---------------------------------------------------------------------------
# Client factory (cached so we don't reconnect on every rerun)
# ---------------------------------------------------------------------------
def get_client():
    """Return a Supabase client or None if credentials are missing."""
    try:
        from supabase import create_client, Client  # type: ignore

        url = (
            st.secrets.get("SUPABASE_URL", "")
            if hasattr(st, "secrets")
            else os.getenv("SUPABASE_URL", "")
        )
        key = (
            st.secrets.get("SUPABASE_KEY", "")
            if hasattr(st, "secrets")
            else os.getenv("SUPABASE_KEY", "")
        )

        if not url or not key:
            return None

        return create_client(url, key)
    except ImportError:
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def authenticate_user(username: str, password: str) -> tuple[dict | None, str | None]:
    """Check credentials against the 'users' table in Supabase."""
    client = get_client()
    if client is None:
        return None, "System cannot connect to the Database. Check SUPABASE_URL."

    try:
        # Match username and password. Better approach would use hashing.
        resp = (
            client.table("users")
            .select("*")
            .eq("username", username)
            .eq("password", password)
            .execute()
        )
        if resp.data and len(resp.data) > 0:
            return resp.data[0], None
        return None, "Invalid username or password."
    except Exception as e:
        print(f"Auth error: {e}")
        return None, f"Database query failed: {str(e)}"


def save_resume_analysis(result: dict, filename: str) -> bool:
    """
    Insert one resume analysis record into the 'resumes' table.

    Returns True on success, False on any error.
    """
    client = get_client()
    if client is None:
        print("DB SAVE ERROR: No Supabase client available.")
        return False

    try:
        # Build payload with ONLY the core columns that exist in the table
        payload = {
            "filename":          filename,
            "role_selected":     result.get("selected_role", "Unknown"),
            "score":             float(result.get("final_score", 0)),
            "skills_count":      int(len(result.get("all_skills", []))),
            "experience_score":  int(result.get("exp_score", 0)),
        }

        # Try adding optional columns — these may or may not exist
        optional_fields = {
            "achievement_score": int(result.get("ach_score", 0)),
            "job_match_score":   float(result.get("job_sim", 0)),
            "created_at":        datetime.utcnow().isoformat(),
            "username":          st.session_state.get("username", "Unknown"),
        }

        # Add LLM context if generated
        llm = result.get("llm_data")
        if llm:
            optional_fields["llm_summary"]     = llm.get("llm_summary", "")
            optional_fields["llm_pros"]         = llm.get("llm_pros", [])
            optional_fields["llm_cons"]         = llm.get("llm_cons", [])
            optional_fields["llm_soft_skills"]  = llm.get("llm_soft_skills", [])

        # First attempt: full payload with optional fields
        full_payload = {**payload, **optional_fields}
        try:
            client.table("resumes").insert(full_payload).execute()
            print(f"DB SAVE OK (full): {filename}")
            return True
        except Exception as e1:
            print(f"DB SAVE WARNING (full payload failed): {e1}")
            # Fallback: insert with only core columns
            try:
                client.table("resumes").insert(payload).execute()
                print(f"DB SAVE OK (core only): {filename}")
                return True
            except Exception as e2:
                print(f"DB SAVE ERROR (core payload also failed): {e2}")
                return False

    except Exception as e:
        print(f"DB SAVE CRITICAL ERROR: {e}")
        return False


def get_all_resumes() -> list[dict[str, Any]]:
    """Return all rows from the 'resumes' table, newest first."""
    client = get_client()
    if client is None:
        return []

    try:
        resp = (
            client.table("resumes")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return resp.data or []
    except Exception:
        return []


def get_resume_stats() -> dict[str, Any]:
    """Return aggregate statistics about all stored resumes."""
    rows = get_all_resumes()
    if not rows:
        return {
            "total":      0,
            "avg_score":  0.0,
            "max_score":  0.0,
            "top_candidate": "—",
            "unique_roles": 0,
        }

    scores = [r["score"] for r in rows if r.get("score") is not None]
    max_score = max(scores) if scores else 0.0
    top_row = next(
        (r for r in rows if r.get("score") == max_score), {}
    )

    return {
        "total":         len(rows),
        "avg_score":     round(sum(scores) / len(scores), 2) if scores else 0.0,
        "max_score":     max_score,
        "top_candidate": top_row.get("filename", "—"),
        "unique_roles":  len({r.get("role_selected") for r in rows if r.get("role_selected")}),
    }


def get_role_distribution() -> dict[str, int]:
    """Return a mapping {role_name: count} from stored resumes."""
    rows = get_all_resumes()
    dist: dict[str, int] = {}
    for r in rows:
        role = r.get("role_selected", "Unknown")
        dist[role] = dist.get(role, 0) + 1
    return dist


def get_score_distribution() -> list[float]:
    """Return a flat list of final_score values for histogram plotting."""
    rows = get_all_resumes()
    return [r["score"] for r in rows if r.get("score") is not None]
