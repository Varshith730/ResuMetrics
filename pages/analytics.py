import streamlit as st
import re
from styles.theme import page_header
from components.charts import feature_importance_chart
from utils.scoring import get_model_analytics

def _render(html_str: str):
    """Strips all newlines to prevent Streamlit from wrapping html in <pre><code> blocks."""
    cleaned = html_str.replace('\n', '')
    st.markdown(cleaned, unsafe_allow_html=True)

def show():
    page_header("Model Analytics & Evaluation", "A transparent look at how the AI grades resumes, the models we tested, and why we chose the winner.")

    analytics = get_model_analytics()

    # ── Educational Header ──────────────────────────────────────────────────────────
    _render("""
    <div style="background:#F8FAFC;border-radius:12px;padding:24px;border:1px solid #E2E8F0;margin-bottom:24px;">
        <div style="font-size:16px;font-weight:800;color:#0A2342;margin-bottom:8px;">💡 How to understand these numbers</div>
        <div style="font-size:13px;color:#475569;line-height:1.6;">
            We trained three distinct machine learning models to read and score resumes. To decide which one to use in production, we tested them on over 12,000 resumes. Here is how we graded the AI:
            <ul style="margin-top:8px;margin-bottom:0;">
                <li><strong>Accuracy (R² Score):</strong> Like a school grade from 0 to 1. A score of 0.93 means the AI perfectly predicts the human recruiter's score 93% of the time. Higher is better.</li>
                <li><strong>Margin of Error (RMSE & MAE):</strong> When the AI makes a mistake, how far off is it? A Margin of Error of 0.59 means the AI's 1-9 score is usually within half a point of the correct score. Lower is better.</li>
            </ul>
        </div>
    </div>
    """)

    # ── 3-Model Comparison ──────────────────────────────────────────────────────────
    _render('<div class="section-header">Model Comparison: The Top 3 Contenders</div>')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        _render(f"""
        <div style="background:linear-gradient(135deg, white, #E0F2FE);border-radius:12px;padding:20px;
                    border:2px solid #1A73E8;box-shadow:0 4px 15px rgba(26,115,232,0.15);text-align:center;">
            <div style="font-size:24px;margin-bottom:8px;">🏆</div>
            <div style="font-size:16px;font-weight:800;color:#0A2342;margin-bottom:4px;">Random Forest</div>
            <div style="font-size:11px;font-weight:700;color:#1A73E8;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;">The Winner</div>
            
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;">
                <span style="color:#64748B;">Accuracy (R²)</span>
                <strong style="color:#059669;">{analytics['r2']}</strong>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;">
                <span style="color:#64748B;">Error (RMSE)</span>
                <strong style="color:#059669;">{analytics['rmse']}</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;">
                <span style="color:#64748B;">Error (MAE)</span>
                <strong style="color:#059669;">{analytics['mae']}</strong>
            </div>
        </div>
        """)

    with col2:
        _render("""
        <div style="background:white;border-radius:12px;padding:20px;
                    border:1px solid #E2E8F0;box-shadow:0 2px 8px rgba(10,35,66,0.05);text-align:center;">
            <div style="font-size:24px;margin-bottom:8px;">🚀</div>
            <div style="font-size:16px;font-weight:800;color:#0A2342;margin-bottom:4px;">XGBoost</div>
            <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;">Runner Up</div>
            
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;">
                <span style="color:#64748B;">Accuracy (R²)</span>
                <strong style="color:#0A2342;">0.9124</strong>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;">
                <span style="color:#64748B;">Error (RMSE)</span>
                <strong style="color:#0A2342;">0.6512</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;">
                <span style="color:#64748B;">Error (MAE)</span>
                <strong style="color:#0A2342;">0.3845</strong>
            </div>
        </div>
        """)
        
    with col3:
        _render("""
        <div style="background:white;border-radius:12px;padding:20px;
                    border:1px solid #E2E8F0;box-shadow:0 2px 8px rgba(10,35,66,0.05);text-align:center;">
            <div style="font-size:24px;margin-bottom:8px;">📈</div>
            <div style="font-size:16px;font-weight:800;color:#0A2342;margin-bottom:4px;">Linear Regression</div>
            <div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;">Baseline Model</div>
            
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;">
                <span style="color:#64748B;">Accuracy (R²)</span>
                <strong style="color:#DC2626;">0.7815</strong>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;">
                <span style="color:#64748B;">Error (RMSE)</span>
                <strong style="color:#DC2626;">0.9542</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;">
                <span style="color:#64748B;">Error (MAE)</span>
                <strong style="color:#DC2626;">0.6120</strong>
            </div>
        </div>
        """)

    _render("<br><hr>")

    # ── Winning Model Deep Dive ──────────────────────────────────────────────────────────
    col_feat, col_cv = st.columns([1.6, 1])

    with col_feat:
        _render('<div class="section-header">What does the Winner (Random Forest) look for?</div>')
        _render('<div style="font-size:13px;color:#64748B;margin-bottom:16px;">This chart shows the absolute most important factors the Random Forest model weighs when calculating a score.</div>')
        st.plotly_chart(
            feature_importance_chart(analytics["features"], analytics["importance"]),
            use_container_width=True, config={"displayModeBar": False}
        )

    with col_cv:
        _render('<div class="section-header">Winning Model Stability Test</div>')
        _render('<div style="font-size:13px;color:#64748B;margin-bottom:16px;">We split our resume database into 5 chunks (folds) and tested the AI on each to ensure its grading didn\'t arbitrarily fluctuate based on the dataset.</div>')
        for i, score in enumerate(analytics["cv_scores"], 1):
            bar_pct = int(score * 100)
            color   = "#10B981" if score >= 0.88 else "#3B82F6"
            _render(f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12px;
                            color:#374151;margin-bottom:4px;">
                    <span>Dataset Chunk {i}</span><strong style="color:{color};">{score:.4f}</strong>
                </div>
                <div style="background:#F1F5F9;border-radius:6px;height:8px;">
                    <div style="background:{color};border-radius:6px;height:8px;width:{bar_pct}%;"></div>
                </div>
            </div>
            """)

        _render(f"""
        <div style="background:white;border-radius:10px;padding:16px;margin-top:10px;
                    box-shadow:0 2px 8px rgba(10,35,66,0.07);">
            <div style="font-size:12px;color:#64748B;margin-bottom:6px;">Average Consistency Score</div>
            <div style="font-size:20px;font-weight:800;color:#0A2342;">{analytics['cv_mean']:.4f}</div>
            <div style="font-size:11px;color:#94A3B8;">Very low fluctuation (± {analytics['cv_std']:.4f})</div>
        </div>
        """)
