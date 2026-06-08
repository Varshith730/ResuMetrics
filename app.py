import streamlit as st
from styles.theme import apply_theme
import pages.overview         as pg_overview
import pages.upload           as pg_upload
import pages.scoring          as pg_scoring
import pages.alignment        as pg_alignment
import pages.risks            as pg_risks
import pages.analytics        as pg_analytics
import pages.report           as pg_report
import pages.admin_dashboard  as pg_admin
import pages.history          as pg_history


# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ── Sidebar ────────────────────────────────────────────────────────────────
role = st.session_state.get("role", "admin")
username = st.session_state.get("username", "Public User")

with st.sidebar:
    # Logo / branding block
    st.markdown(f"""
    <div style="padding:20px 10px 10px;text-align:center;">
        <div style="width:56px;height:56px;background:linear-gradient(135deg,#1A73E8,#0D47A1);
                    border-radius:14px;margin:0 auto 12px;display:flex;align-items:center;
                    justify-content:center;font-size:26px;">🧠</div>
        <div style="font-size:15px;font-weight:800;color:#FFFFFF;letter-spacing:.3px;">
            ResuMetrics
        </div>
        <div style="font-size:10px;color:#7096B8;margin-top:2px;text-transform:uppercase;
                    letter-spacing:1px;">AI Recruitment Intelligence</div>
    </div>
    <hr style="border:none;border-top:1px solid #1E4A7A;margin:0 0 12px;">
    """, unsafe_allow_html=True)

    # ── User badge ────────────────────────────────────────────────────────
    badge_color = "#1A73E8" if role == "admin" else "#10B981"
    badge_label = "Admin" if role == "admin" else "Recruiter"
    st.markdown(f"""
    <div style="padding:10px 12px;background:rgba(255,255,255,0.06);
                border-radius:10px;border:1px solid rgba(255,255,255,0.1);
                margin-bottom:14px;display:flex;align-items:center;gap:10px;">
        <div style="width:32px;height:32px;background:{badge_color};
                    border-radius:50%;display:flex;align-items:center;
                    justify-content:center;font-size:14px;flex-shrink:0;">👤</div>
        <div>
            <div style="font-size:12px;font-weight:700;color:#FFFFFF;">{username}</div>
            <div style="font-size:10px;color:{badge_color};font-weight:600;
                        text-transform:uppercase;letter-spacing:.8px;">{badge_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────────────
    BASE_NAV = {
        "🏠  Executive Overview":       "overview",
        "📂  Resume Upload":            "upload",
        "📊  Candidate Scoring":        "scoring",
        "🎯  Job Alignment Analysis":   "alignment",
        "⚠️  Risk & Weakness Insights": "risks",
        "📈  Model Analytics":          "analytics",
        "📄  Generate Report":          "report",
        "🕑  Candidate History":        "history",
    }

    ADMIN_NAV = {
        "🛡️  Admin Dashboard": "admin",
    }

    NAV_ITEMS = dict(BASE_NAV)
    if role == "admin":
        NAV_ITEMS.update(ADMIN_NAV)

    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "overview"

    for label, key in NAV_ITEMS.items():
        is_active = st.session_state["active_page"] == key
        btn_style = (
            "background:linear-gradient(135deg,#1A73E8,#0D47A1);color:white;"
            "font-weight:700;border-radius:8px;"
        ) if is_active else (
            "background:transparent;color:#CBD5E1;"
            "font-weight:500;border-radius:8px;"
        )
        if st.button(label, key=f"nav_{key}",
                     use_container_width=True,
                     help=f"Go to {label.strip()}"):
            st.session_state["active_page"] = key
            st.rerun()

    # ── Session status ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border:none;border-top:1px solid #1E4A7A;'>",
                unsafe_allow_html=True)

    if "result" in st.session_state:
        r = st.session_state["result"]
        from utils.scoring import score_label
        lbl, clr = score_label(r["final_score"])
        st.markdown(f"""
        <div style="padding:14px;background:rgba(26,115,232,0.12);border-radius:10px;
                    border:1px solid rgba(26,115,232,0.25);">
            <div style="font-size:10px;color:#7096B8;text-transform:uppercase;
                        letter-spacing:.8px;margin-bottom:6px;">Active Candidate</div>
            <div style="font-size:22px;font-weight:900;color:white;">{r['final_score']}/9</div>
            <div style="font-size:11px;color:{clr};font-weight:600;">{lbl}</div>
            <div style="font-size:10px;color:#7096B8;margin-top:4px;">{r['selected_role']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding:12px;background:rgba(255,255,255,0.05);border-radius:8px;
                    border:1px solid #1E4A7A;text-align:center;">
            <div style="font-size:11px;color:#7096B8;">No resume analysed yet</div>
        </div>
        """, unsafe_allow_html=True)



    st.markdown("""
    <div style="margin-top:12px;font-size:9px;color:#3D6080;text-align:center;padding-bottom:10px;">
        v2.4.1 · Enterprise Edition<br>© 2026 ResuMetrics Inc.
    </div>
    """, unsafe_allow_html=True)

# ── Route to active page ────────────────────────────────────────────────────
page = st.session_state.get("active_page", "overview")

st.markdown("""
<div style="padding: 8px 0 0 0; margin-bottom: -10px;">
</div>
""", unsafe_allow_html=True)

ROUTER = {
    "overview":  pg_overview.show,
    "upload":    pg_upload.show,
    "scoring":   pg_scoring.show,
    "alignment": pg_alignment.show,
    "risks":     pg_risks.show,
    "analytics": pg_analytics.show,
    "report":    pg_report.show,
    "history":   pg_history.show,
    "admin":     pg_admin.show,
}

# Guard admin page from non-admin users
if page == "admin" and role != "admin":
    st.warning("⛔ Access restricted to administrators only.")
else:
    ROUTER.get(page, pg_overview.show)()
