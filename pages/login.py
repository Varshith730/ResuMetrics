"""
pages/login.py
Enterprise login page for the AI Resume Intelligence Platform.

Demo accounts (no Supabase Auth required):
  admin      / admin123  → role: admin
  recruiter  / pass123   → role: recruiter
"""

import streamlit as st

def _authenticate(username: str, password: str) -> tuple[dict | None, str | None]:
    from utils.database import authenticate_user
    
    try:
        # Check DB
        result = authenticate_user(username.strip(), password)
        
        # In Python 3.10+, if result is a tuple, we map it:
        if isinstance(result, tuple) and len(result) == 2:
            user_record, err = result
        else:
            # Fallback for weird caches
            user_record, err = result, None
            
        # At this point, user_record should be a dictionary holding the Supabase row
        if user_record and hasattr(user_record, "get"):
            return {
                "role": user_record.get("role", "recruiter"),
                "name": user_record.get("username", username).title()
            }, None
            
        if err:
            return None, err
            
        return None, "Invalid username or password"
        
    except Exception as e:
        return None, f"Internal Auth Error: {str(e)}"


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------
def show():
    # Inject login-specific styles
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0A2342 0%, #103361 40%, #1A4A8A 100%);
        min-height: 100vh;
    }

    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }
    section[data-testid="stSidebar"] { display: none; }

    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4A9FF5 !important;
        box-shadow: 0 0 0 3px rgba(74,159,245,0.25) !important;
    }
    .stTextInput label { color: rgba(255,255,255,0.75) !important; font-size: 13px !important; }

    /* Login button */
    .stButton button {
        background: linear-gradient(135deg, #1A73E8, #0D47A1) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-size: 15px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 20px rgba(26,115,232,0.4) !important;
    }
    .stButton button p {
        color: white !important;
    }
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 24px rgba(26,115,232,0.5) !important;
    }

    /* Error / warn messages */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        background-color: rgba(239, 68, 68, 0.2) !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        backdrop-filter: blur(10px);
    }
    [data-testid="stAlert"] * {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Centered card layout ────────────────────────────────────────────────
    _, col, _ = st.columns([1, 1.2, 1])

    with col:
        # Logo block
        st.markdown("""
        <div style="text-align:center;padding:48px 0 32px;">
            <div style="width:72px;height:72px;
                        background:linear-gradient(135deg,#1A73E8,#0D47A1);
                        border-radius:20px;margin:0 auto 16px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:36px;
                        box-shadow:0 8px 32px rgba(26,115,232,0.4);">🧠</div>
            <div style="font-size:24px;font-weight:800;color:#FFFFFF;letter-spacing:0.3px;">
                ResuMetrics
            </div>
            <div style="font-size:11px;color:#7096B8;text-transform:uppercase;
                        letter-spacing:1.5px;margin-top:4px;">
                AI Recruitment Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Card
        st.markdown("""
        <div style="background:rgba(255,255,255,0.07);
                    backdrop-filter:blur(20px);
                    -webkit-backdrop-filter:blur(20px);
                    border:1px solid rgba(255,255,255,0.12);
                    border-radius:20px;
                    padding:36px 32px 28px;
                    box-shadow:0 24px 64px rgba(0,0,0,0.3);">
            <div style="font-size:20px;font-weight:700;color:#FFFFFF;margin-bottom:4px;">
                Sign in to your account
            </div>
            <div style="font-size:13px;color:#7096B8;margin-bottom:28px;">
                Enter your credentials to access the platform
            </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter username", key="login_user")
        password = st.text_input("Password", placeholder="Enter password",
                                 type="password", key="login_pass")

        if st.button("🔐  Sign In", key="login_btn", use_container_width=True):
            if not username or not password:
                st.error("Please fill in both fields.")
            else:
                user, err_msg = _authenticate(username, password)
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["role"] = user["role"]
                    st.session_state["username"] = user["name"]
                    st.session_state.setdefault("active_page", "overview")
                    st.rerun()
                else:
                    st.error(f"❌ Login Failed: {err_msg}")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center;margin-top:24px;
                    font-size:10px;color:#3D6080;padding-bottom:40px;">
            v2.4.1 · Enterprise Edition &nbsp;·&nbsp; © 2026 ResuMetrics Inc.
        </div>
        """, unsafe_allow_html=True)
