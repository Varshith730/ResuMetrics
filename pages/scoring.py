import streamlit as st
from styles.theme import page_header
from components.charts import gauge_chart, score_breakdown_bar
from utils.scoring import score_label


def _score_card(label, value, icon):
    color = "#10B981" if value >= 7 else "#F59E0B" if value >= 5 else "#EF4444"
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:18px;
                box-shadow:0 2px 8px rgba(10,35,66,0.08);text-align:center;margin-bottom:12px;">
        <div style="font-size:22px;margin-bottom:6px;">{icon}</div>
        <div style="font-size:11px;font-weight:600;color:#64748B;text-transform:uppercase;
                    letter-spacing:.7px;margin-bottom:6px;">{label}</div>
        <div style="font-size:28px;font-weight:800;color:{color};">{value:.1f}<span style="font-size:14px;color:#94A3B8;">/10</span></div>
    </div>
    """, unsafe_allow_html=True)


def show():
    page_header("Candidate Scoring Dashboard", "AI-computed multi-dimensional resume intelligence score")

    if "result" not in st.session_state:
        st.info("⬅️  Please upload a resume on the **Resume Upload** page first.")
        return

    r = st.session_state["result"]

    # ── Hire Recommendation Banner ──
    if r.get("final_score", 0) >= 7.0:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #059669, #10B981);
                    padding:16px 20px;border-radius:12px;color:#FFFFFF !important;
                    display:flex;align-items:center;gap:12px;margin-bottom:20px;
                    box-shadow:0 4px 15px rgba(16, 185, 129, 0.3);">
            <div style="font-size:32px;">🌟</div>
            <div>
                <div style="font-size:16px;font-weight:900;letter-spacing:0.5px;color:#FFFFFF !important;">HIRE RECOMMENDATION: EXCELLENT</div>
                <div style="font-size:13px;color:#FFFFFF !important;opacity:0.95;">This candidate strongly aligns with the <strong>{r.get('selected_role', 'role')}</strong> requirements and is highly recommended for progression.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    label, color = score_label(r["final_score"])
    badge_class = {
        "Excellent": "badge-excellent", "Good": "badge-good",
        "Average": "badge-average",     "Poor": "badge-poor"
    }.get(label, "badge-good")

    col_gauge, col_breakdown = st.columns([1.2, 1])

    with col_gauge:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:24px;
                    box-shadow:0 2px 12px rgba(10,35,66,0.08);text-align:center;margin-bottom:16px;">
            <div style="font-size:48px;font-weight:900;color:{color};line-height:1;">
                {r['final_score']}
            </div>
            <div style="font-size:18px;font-weight:700;color:#0A2342;margin:4px 0;">
                out of 9.0
            </div>
            <span class="score-badge {badge_class}" style="margin-top:10px;display:inline-block;">
                {label}
            </span>
            <div style="font-size:12px;color:#94A3B8;margin-top:10px;">
                Target Role: <strong style="color:#0A2342;">{r['selected_role']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(gauge_chart(r["final_score"]), use_container_width=True,
                        config={"displayModeBar": False})

    with col_breakdown:
        st.markdown('<div class="section-header">Score Breakdown</div>', unsafe_allow_html=True)
        breakdown = {
            "Skills Strength":    r["skills_score"],
            "Experience Depth":   r["exp_score"],
            "Achievement Impact": r["ach_score"],
            "Job Similarity":     r["job_sim"],
        }
        st.plotly_chart(score_breakdown_bar(breakdown), use_container_width=True,
                        config={"displayModeBar": False})

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            _score_card("Skills",      r["skills_score"], "⚡")
            _score_card("Achievement", r["ach_score"],    "🏆")
        with c2:
            _score_card("Experience",  r["exp_score"],    "🏢")
            _score_card("Job Match",   r["job_sim"],      "🎯")

    # ── Summary row ───────────────────────────────────────────────────────────
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Experience Years",   f"{r['exp_years']:.0f} yrs")
    m2.metric("Skills Detected",    len(r["all_skills"]))
    m3.metric("Job Match %",        f"{r['job_match_pct']}%")
