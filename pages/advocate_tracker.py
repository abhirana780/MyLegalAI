import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title="🧾 Advocate Tracker Module",
    page_icon="🧾",
    layout="wide"
)

st.title("🧾 Advocate Tracker Module")
st.markdown("""
Track the most frequent appearing advocates (petitioner and respondent) and visualize their activity over time. Filter by case type for deeper insights.
""")

# --- Load Judgments CSV ---
JUDGMENTS_CSV = os.path.join("assets", "judgments.csv")
if not os.path.exists(JUDGMENTS_CSV):
    st.error("Judgments CSV not found at 'assets/judgments.csv'. Please upload the file.")
    st.stop()

@st.cache_data(show_spinner=False)
def load_judgments():
    df = pd.read_csv(JUDGMENTS_CSV)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

judgments = load_judgments()

# --- Filter by Case Type ---
case_types = ['All'] + sorted(judgments['judgement_type'].dropna().unique())
selected_case_type = st.selectbox("📋 Filter by Case Type", case_types)

if selected_case_type != 'All':
    filtered = judgments[judgments['judgement_type'] == selected_case_type].copy()
else:
    filtered = judgments.copy()

# --- Prepare Advocate Data ---
# Combine petitioner and respondent advocates
advocate_data = pd.concat([
    filtered[['pet_adv']].rename(columns={'pet_adv': 'Advocate'}),
    filtered[['res_adv']].rename(columns={'res_adv': 'Advocate'})
], ignore_index=True)

advocate_data = advocate_data.dropna()
advocate_data['Advocate'] = advocate_data['Advocate'].str.strip()

# Count frequency
advocate_counts = advocate_data['Advocate'].value_counts().reset_index()
advocate_counts.columns = ['Advocate', 'Appearances']

# --- Most Frequent Advocates ---
st.subheader("🏆 Most Frequent Appearing Advocates")
if advocate_counts.empty:
    st.info("No advocate data available for the selected case type.")
else:
    top_n = st.slider("Show Top N Advocates", min_value=5, max_value=30, value=10)
    st.dataframe(advocate_counts.head(top_n), use_container_width=True)
    fig = px.bar(advocate_counts.head(top_n), x='Advocate', y='Appearances',
                 title='Top Advocates by Number of Appearances',
                 labels={'Advocate': 'Advocate', 'Appearances': 'Number of Appearances'})
    fig.update_layout(xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- Timeline of Appearances ---
st.subheader("⏱️ Timeline of Advocate Appearances")
if 'judgment_dates' in filtered.columns:
    filtered['judgment_dates'] = pd.to_datetime(filtered['judgment_dates'], errors='coerce')
    timeline_data = pd.concat([
        filtered[['judgment_dates', 'pet_adv']].rename(columns={'pet_adv': 'Advocate'}),
        filtered[['judgment_dates', 'res_adv']].rename(columns={'res_adv': 'Advocate'})
    ], ignore_index=True)
    timeline_data = timeline_data.dropna(subset=['Advocate', 'judgment_dates'])
    timeline_data['Advocate'] = timeline_data['Advocate'].str.strip()
    # Option to select specific advocate(s)
    unique_advocates = timeline_data['Advocate'].value_counts().index.tolist()
    selected_advocates = st.multiselect(
        "Select Advocate(s) for Timeline (leave blank for top 5)",
        unique_advocates,
        default=unique_advocates[:5]
    )
    if selected_advocates:
        timeline_data = timeline_data[timeline_data['Advocate'].isin(selected_advocates)]
    else:
        timeline_data = timeline_data[timeline_data['Advocate'].isin(unique_advocates[:5])]
    # Group by month
    timeline_data['Month'] = timeline_data['judgment_dates'].dt.to_period('M').dt.to_timestamp()
    timeline_grouped = timeline_data.groupby(['Month', 'Advocate']).size().reset_index(name='Appearances')
    if not timeline_grouped.empty:
        fig2 = px.line(
            timeline_grouped,
            x='Month',
            y='Appearances',
            color='Advocate',
            markers=True,
            title='Timeline of Advocate Appearances'
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No timeline data available for the selected advocates.")
else:
    st.info("Judgment date information is not available in the data.")

st.markdown("---")
st.caption("Advocate Tracker Module: Analyze advocate activity and trends across cases. Data source: judgments.csv")