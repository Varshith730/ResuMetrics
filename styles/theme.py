def apply_theme():
    import streamlit as st

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #0A2342 !important;
    }

    /* Main background */
    .main { background-color: #F8FAFC; }
    .stApp { background-color: #F8FAFC; }

    /* Headings */
    h1, h2, h3, h4, h5 {
        color: #0A2342 !important;
        font-weight: 700;
    }

    /* Paragraph text */
    p, span, div {
        color: #334155;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A2342 0%, #1A3A5C 60%, #163355 100%);
        border-right: 1px solid #1E4A7A;
    }

    section[data-testid="stSidebar"] * {
        color: #CBD5E1 !important;
    }

    section[data-testid="stSidebar"] .sidebar-header {
        color: #FFFFFF !important;
        font-weight: 700;
    }

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 24px 20px;
        box-shadow: 0 2px 12px rgba(10,35,66,0.08);
        border-left: 4px solid #1A73E8;
        margin-bottom: 16px;
    }

    .kpi-card .label {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }

    .kpi-card .value {
        font-size: 32px;
        font-weight: 800;
        color: #0A2342;
        line-height: 1;
    }

    .kpi-card .sub {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 6px;
    }

    /* Section Header */
    .section-header {
        font-size: 20px;
        font-weight: 800;
        color: #0A2342;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #CBD5E1;
    }

    /* Score badges */
    .score-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    .badge-excellent { background:#D1FAE5; color:#065F46; }
    .badge-good      { background:#DBEAFE; color:#1E40AF; }
    .badge-average   { background:#FEF3C7; color:#92400E; }
    .badge-poor      { background:#FEE2E2; color:#991B1B; }

    /* Risk cards */
    .risk-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(10,35,66,0.07);
        margin-bottom: 14px;
        border-left: 4px solid #E74C3C;
    }

    .risk-card.medium { border-left-color: #F39C12; }
    .risk-card.low { border-left-color: #3498DB; }

    /* Skill tags */
    .skill-tag-match {
        display:inline-block;
        background:#D1FAE5;
        color:#065F46;
        border-radius:6px;
        padding:4px 12px;
        margin:3px;
        font-size:12px;
        font-weight:600;
    }

    .skill-tag-miss {
        display:inline-block;
        background:#FEE2E2;
        color:#991B1B;
        border-radius:6px;
        padding:4px 12px;
        margin:3px;
        font-size:12px;
        font-weight:600;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg,#1A73E8,#0D47A1) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 28px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(26,115,232,0.3) !important;
    }

    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(26,115,232,0.4) !important;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 16px !important;
        box-shadow: 0 2px 8px rgba(10,35,66,0.08);
        border: 1px solid #E2E8F0;
    }

    [data-testid="stMetricValue"] {
        color: #0A2342 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
    }

    /* Plotly chart text */
    .js-plotly-plot text {
        fill: #0A2342 !important;
    }

    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 12px !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 12px;
        border: 2px dashed #93C5FD;
        padding: 20px;
    }
    [data-testid="stFileUploader"] button {
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }

    /* Select box */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: white !important;
    }
    
    /* Dropdown list popover */
    div[data-baseweb="popover"] {
        background-color: #1A3A5C !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="popover"] *, ul[role="listbox"] li {
        color: white !important;
    }

    /* Hide Streamlit menu */
    #MainMenu { visibility:hidden; }
    footer { visibility:hidden; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #F1F5F9; }
    ::-webkit-scrollbar-thumb { background: #94A3B8; border-radius: 3px; }

    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    import streamlit as st

    st.markdown(f"""
    <div style="margin-bottom:28px;">
        <h1 style="font-size:26px;font-weight:800;color:#0A2342;margin:0;">{title}</h1>
        {"<p style='font-size:14px;color:#64748B;margin-top:6px;'>"+subtitle+"</p>" if subtitle else ""}
        <div style="height:3px;background:linear-gradient(90deg,#1A73E8,#6BA3F5);
                    border-radius:2px;margin-top:10px;width:60px;"></div>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "", accent: str = "#1A73E8"):
    import streamlit as st

    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:{accent};">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        {"<div class='sub'>"+sub+"</div>" if sub else ""}
    </div>
    """, unsafe_allow_html=True)