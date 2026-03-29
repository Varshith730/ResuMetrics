import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def gauge_chart(score: float, max_score: float = 9.0) -> go.Figure:
    pct = score / max_score
    if pct >= 0.83:
        color = "#10B981"
    elif pct >= 0.61:
        color = "#3B82F6"
    elif pct >= 0.39:
        color = "#F59E0B"
    else:
        color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={"reference": 5.0, "increasing": {"color": "#10B981"}, "decreasing": {"color": "#EF4444"}},
        number={"font": {"size": 52, "color": "#0A2342", "family": "Inter"}, "suffix": "/9"},
        gauge={
            "axis": {"range": [0, 9], "tickwidth": 1, "tickcolor": "#CBD5E1",
                     "tickfont": {"size": 11, "color": "#64748B"}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#F8FAFC",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 3.5],  "color": "#FEE2E2"},
                {"range": [3.5, 5.5],"color": "#FEF3C7"},
                {"range": [5.5, 7.5],"color": "#DBEAFE"},
                {"range": [7.5, 9],  "color": "#D1FAE5"},
            ],
            "threshold": {"line": {"color": "#0A2342", "width": 3}, "thickness": 0.8, "value": score},
        },
        title={"text": "Resume Intelligence Score", "font": {"size": 14, "color": "#64748B", "family": "Inter"}},
    ))
    fig.update_layout(
        height=280, margin=dict(t=40, b=20, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", font_color="#0A2342"),
    )
    return fig


def score_breakdown_bar(scores: dict) -> go.Figure:
    labels = list(scores.keys())
    values = list(scores.values())
    colors = ["#3B82F6" if v >= 7 else "#F59E0B" if v >= 5 else "#EF4444" for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation='h',
        marker_color=colors,
        text=[f"{v:.1f}/10" for v in values],
        textposition='outside',
        textfont={"size": 12, "family": "Inter"},
    ))
    fig.update_layout(
        height=220, margin=dict(t=10, b=10, l=10, r=60),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 11.5], showgrid=True, gridcolor="#F1F5F9",
                   tickfont={"size": 11}, zeroline=False),
        yaxis=dict(tickfont={"size": 12, "color": "#374151"}),
        showlegend=False, font={"family": "Inter"},
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", font_color="#0A2342"),
    )
    return fig


def skill_match_bar(matching: list, missing: list) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Matched", x=["Matched"], y=[len(matching)],
        marker_color="#10B981", text=[len(matching)], textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="Missing", x=["Missing"], y=[len(missing)],
        marker_color="#EF4444", text=[len(missing)], textposition="outside",
    ))
    fig.update_layout(
        height=220, barmode='group',
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", x=0, y=1.15),
        margin=dict(t=40, b=10, l=10, r=10),
        font={"family": "Inter"},
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", font_color="#0A2342"),
    )
    return fig


def feature_importance_chart(features: list, importance: list) -> go.Figure:
    df = pd.DataFrame({"Feature": features, "Importance": importance})
    df = df.sort_values("Importance", ascending=True)
    fig = go.Figure(go.Bar(
        x=df["Importance"], y=df["Feature"], orientation='h',
        marker=dict(
            color=df["Importance"],
            colorscale=[[0,"#DBEAFE"],[0.5,"#3B82F6"],[1,"#1D4ED8"]],
            showscale=False,
        ),
        text=[f"{v:.2%}" for v in df["Importance"]],
        textposition='outside',
    ))
    fig.update_layout(
        height=320, margin=dict(t=10, b=10, l=10, r=60),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickformat=".0%", showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        yaxis=dict(tickfont={"size": 11}),
        font={"family": "Inter"},
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", font_color="#0A2342"),
    )
    return fig


def score_distribution_chart(scores: list) -> go.Figure:
    fig = go.Figure(go.Histogram(
        x=scores, nbinsx=9,
        marker_color="#3B82F6",
        marker_line=dict(color="white", width=1),
        opacity=0.85,
    ))
    fig.update_layout(
        height=200, margin=dict(t=10, b=30, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Score", range=[1, 9], showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="Count", showgrid=True, gridcolor="#F1F5F9"),
        font={"family": "Inter", "size": 11},
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", font_color="#0A2342"),
    )
    return fig
