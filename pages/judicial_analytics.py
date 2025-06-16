import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from itertools import combinations

st.set_page_config(
    page_title="Judicial Analytics - Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("📊 Judicial Analytics Dashboard")
st.markdown("### Insights and trends from legal judgments")

# Load and preprocess the judgments data
@st.cache_data
def load_judgments_data():
    df = pd.read_csv('assets/judgments.csv')
    # Convert judgment_dates to datetime
    df['judgment_dates'] = pd.to_datetime(df['judgment_dates'], format='%d-%m-%Y', errors='coerce')
    df['year'] = df['judgment_dates'].dt.year
    df['month'] = df['judgment_dates'].dt.month
    return df

# Load data
df = load_judgments_data()

# Create tabs for different analytics views
tab1, tab2, tab3, tab4 = st.tabs(["📈 Judgment Trends", "👨‍⚖️ Judge Analytics", 
                                 "🧑‍🤝‍🧑 Bench Combinations", "🧑‍💼 Party Analytics"])

with tab1:
    st.markdown("### Judgment Trends Over Time")
    
    # Judgments per year
    yearly_counts = df.groupby('year').size().reset_index(name='count')
    fig_yearly = px.line(yearly_counts, x='year', y='count',
                        title='Number of Judgments per Year',
                        labels={'count': 'Number of Judgments', 'year': 'Year'})
    st.plotly_chart(fig_yearly, use_container_width=True)
    
    # Judgments by type
    judgment_types = df['Judgement_type'].value_counts()
    fig_types = px.pie(values=judgment_types.values, names=judgment_types.index,
                      title='Distribution of Judgment Types')
    st.plotly_chart(fig_types, use_container_width=True)

with tab2:
    st.markdown("### Judge Activity Analysis")
    
    # Most active judges
    judge_counts = df['judgement_by'].value_counts().head(10)
    fig_judges = px.bar(x=judge_counts.index, y=judge_counts.values,
                       title='Top 10 Most Active Judges',
                       labels={'x': 'Judge', 'y': 'Number of Judgments'})
    st.plotly_chart(fig_judges, use_container_width=True)
    
    # Judge activity over time
    judge_timeline = df.groupby(['year', 'judgement_by']).size().reset_index(name='count')
    top_judges = df['judgement_by'].value_counts().head(5).index
    
    fig_timeline = go.Figure()
    for judge in top_judges:
        judge_data = judge_timeline[judge_timeline['judgement_by'] == judge]
        fig_timeline.add_trace(go.Scatter(x=judge_data['year'], y=judge_data['count'],
                                        mode='lines+markers', name=judge))
    
    fig_timeline.update_layout(title='Judge Activity Timeline (Top 5 Judges)',
                              xaxis_title='Year',
                              yaxis_title='Number of Judgments')
    st.plotly_chart(fig_timeline, use_container_width=True)

with tab3:
    st.markdown("### Bench Combination Analysis")
    
    # Function to get bench combinations
    def get_bench_combinations(bench_str):
        if pd.isna(bench_str):
            return []
        judges = [j.strip() for j in bench_str.split(',')]
        return list(combinations(sorted(judges), 2))
    
    # Calculate bench combinations
    all_combinations = []
    for bench in df['bench']:
        all_combinations.extend(get_bench_combinations(bench))
    
    # Get top combinations
    top_combinations = Counter(all_combinations).most_common(10)
    
    # Create visualization
    combo_df = pd.DataFrame(top_combinations, columns=['Combination', 'Count'])
    combo_df['Judges'] = combo_df['Combination'].apply(lambda x: ' & '.join(x))
    
    fig_combos = px.bar(combo_df, x='Judges', y='Count',
                        title='Top 10 Common Bench Combinations',
                        labels={'Judges': 'Judge Combination', 'Count': 'Number of Cases Together'})
    st.plotly_chart(fig_combos, use_container_width=True)

with tab4:
    st.markdown("### Party Analytics")
    
    # Most frequent petitioners
    pet_counts = df['pet'].value_counts().head(10)
    fig_pet = px.bar(x=pet_counts.index, y=pet_counts.values,
                     title='Top 10 Most Frequent Petitioners',
                     labels={'x': 'Petitioner', 'y': 'Number of Cases'})
    st.plotly_chart(fig_pet, use_container_width=True)
    
    # Most frequent respondents
    res_counts = df['res'].value_counts().head(10)
    fig_res = px.bar(x=res_counts.index, y=res_counts.values,
                     title='Top 10 Most Frequent Respondents',
                     labels={'x': 'Respondent', 'y': 'Number of Cases'})
    st.plotly_chart(fig_res, use_container_width=True)

# Display some key statistics
st.markdown("### 📈 Key Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Judgments", len(df))

with col2:
    st.metric("Unique Judges", df['judgement_by'].nunique())

with col3:
    st.metric("Average Cases/Year", 
              round(len(df) / df['year'].nunique(), 2))

with col4:
    st.metric("Judgment Types", df['Judgement_type'].nunique())