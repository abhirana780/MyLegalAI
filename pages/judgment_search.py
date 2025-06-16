import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Judgment Search - Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("🔍 Judgment Search")
st.markdown("### Search and filter through legal judgments")

# Load the judgments data
@st.cache_data
def load_judgments_data():
    df = pd.read_csv('assets/judgments.csv')
    # Convert judgment_dates to datetime
    df['judgment_dates'] = pd.to_datetime(df['judgment_dates'], format='%d-%m-%Y', errors='coerce')
    return df

# Load data
df = load_judgments_data()

# Create search form
with st.form("search_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Judge/Bench search
        judge_search = st.text_input("🧑‍⚖️ Search by Judge/Bench", 
                                   placeholder="Enter judge or bench member name")
        
        # Judgment type filter
        judgment_types = ['All'] + sorted(df['Judgement_type'].unique().tolist())
        selected_type = st.selectbox("⚖️ Judgment Type", judgment_types)
        
        # Language filter
        languages = ['All'] + sorted(df['language'].dropna().unique().tolist())
        selected_language = st.selectbox("🗣️ Language", languages)
    
    with col2:
        # Party search (multi-party support)
        party_search = st.text_input("👥 Search by Petitioner/Respondent (comma-separated for multi-party)", 
                                   placeholder="Enter party names, separated by commas")
        # Advocate + Bench combo search
        adv_bench_search = st.text_input("🧑‍💼🔎 Search by Advocate + Bench Combo", placeholder="e.g. Adv. Name, Bench Name")
        # Date range filter
        date_range = st.date_input(
            "📅 Judgment Date Range",
            value=(df['judgment_dates'].min(), df['judgment_dates'].max()),
            min_value=df['judgment_dates'].min(),
            max_value=df['judgment_dates'].max()
        )
    
    submitted = st.form_submit_button("🔍 Search", use_container_width=True)

if submitted:
    # Filter data based on search criteria
    filtered_df = df.copy()
    # Apply judge/bench filter
    if judge_search:
        filtered_df = filtered_df[
            filtered_df['bench'].str.contains(judge_search, case=False, na=False) |
            filtered_df['judgement_by'].str.contains(judge_search, case=False, na=False)
        ]
    # Apply judgment type filter
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['Judgement_type'] == selected_type]
    # Apply language filter
    if selected_language != 'All':
        filtered_df = filtered_df[filtered_df['language'] == selected_language]
    # Apply multi-party search
    if party_search:
        parties = [p.strip() for p in party_search.split(',') if p.strip()]
        if parties:
            party_mask = False
            for p in parties:
                party_mask = party_mask | filtered_df['pet'].str.contains(p, case=False, na=False) | filtered_df['res'].str.contains(p, case=False, na=False)
            filtered_df = filtered_df[party_mask]
    # Advocate + Bench combo search
    if adv_bench_search:
        adv_bench_parts = [x.strip() for x in adv_bench_search.split(',') if x.strip()]
        if len(adv_bench_parts) == 2:
            adv, bench = adv_bench_parts
            adv_mask = filtered_df['pet_adv'].str.contains(adv, case=False, na=False) | filtered_df['res_adv'].str.contains(adv, case=False, na=False)
            bench_mask = filtered_df['bench'].str.contains(bench, case=False, na=False)
            filtered_df = filtered_df[adv_mask & bench_mask]
        elif len(adv_bench_parts) == 1:
            adv = adv_bench_parts[0]
            adv_mask = filtered_df['pet_adv'].str.contains(adv, case=False, na=False) | filtered_df['res_adv'].str.contains(adv, case=False, na=False)
            filtered_df = filtered_df[adv_mask]
    # Apply date range filter
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df['judgment_dates'] >= start_date) &
        (filtered_df['judgment_dates'] <= end_date)
    ]
    # Display results
    st.markdown(f"### Found {len(filtered_df)} matching judgments")
    # Display results in an expandable format
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['case_no']} - {row['pet']} vs {row['res']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Case Number:** {row['case_no']}")
                st.markdown(f"**Judgment Type:** {row['Judgement_type']}")
                st.markdown(f"**Judgment Date:** {row['judgment_dates'].strftime('%d-%m-%Y')}")
                st.markdown(f"**Language:** {row['language'] if pd.notna(row['language']) else 'Not specified'}")
            with col2:
                st.markdown(f"**Bench:** {row['bench']}")
                st.markdown(f"**Judgment By:** {row['judgement_by']}")
                st.markdown(f"**Petitioner:** {row['pet']}")
                st.markdown(f"**Respondent:** {row['res']}")
            # Add link to judgment if available
            if pd.notna(row['temp_link']):
                st.markdown(f"[View Judgment PDF]({row['temp_link']})")
    # Judge Language Bias Analysis Section
    st.markdown("---")
    st.markdown("## 🧑‍⚖️ Judge Language Bias Analysis")
    judge_lang_stats = df.groupby(['judgement_by', 'language']).size().reset_index(name='count')
    judge_totals = df['judgement_by'].value_counts().to_dict()
    judge_bias = []
    for judge in judge_lang_stats['judgement_by'].unique():
        judge_data = judge_lang_stats[judge_lang_stats['judgement_by'] == judge]
        total = judge_totals.get(judge, 1)
        lang_dist = {row['language']: row['count']/total for _, row in judge_data.iterrows()}
        if len(lang_dist) > 1:
            judge_bias.append({'Judge': judge, 'Language Distribution': lang_dist})
    if judge_bias:
        st.markdown("### Judges with Multiple Language Judgments")
        for jb in judge_bias:
            st.markdown(f"**{jb['Judge']}**: {jb['Language Distribution']}")
    else:
        st.info("No significant language bias detected among judges.")
else:
    # Display some statistics
    st.markdown("### Quick Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Judgments", len(df))
    
    with col2:
        st.metric("Judgment Types", len(df['Judgement_type'].unique()))
    
    with col3:
        st.metric("Languages", len(df['language'].dropna().unique()))