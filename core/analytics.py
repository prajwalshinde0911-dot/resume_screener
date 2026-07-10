import plotly.express as px
import streamlit as st

def show_score_chart(df):
    """Bar chart comparing candidates by final score."""
    fig = px.bar(
        df,
        x="Candidate",
        y="Final Score",
        color="Final Score",
        color_continuous_scale="Blues",
        text="Final Score"
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(yaxis_range=[0, 100], showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_score_breakdown(df):
    """Grouped bar chart: semantic vs skill match per candidate."""
    fig = px.bar(
        df,
        x="Candidate",
        y=["Semantic Match %", "Skill Match %"],
        barmode="group",
        height=400
    )
    fig.update_layout(yaxis_range=[0, 100], legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)