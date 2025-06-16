import streamlit as st
import pandas as pd

st.set_page_config(page_title="Case Metadata Viewer", page_icon="📑", layout="wide")
st.title("📑 Case Metadata Viewer")
st.markdown("""
This public record viewer displays case metadata from the judgments database. Use the search box to filter cases. Click the PDF link to view the full judgment.
""")

@st.cache_data
def load_data():
    df = pd.read_csv('assets/judgments.csv')
    df['judgment_dates'] = pd.to_datetime(df['judgment_dates'], format='%d-%m-%Y', errors='coerce')
    return df

df = load_data()

# Select columns to display
columns = {
    'case_no': 'Case Number',
    'pet': 'Petitioner',
    'res': 'Respondent',
    'judgement_by': 'Judge',
    'bench': 'Bench',
    'judgment_dates': 'Date',
    'temp_link': 'Judgment PDF'
}

# Combine advocates columns for display
view_df = df.copy()
view_df['Advocates'] = view_df[['pet_adv', 'res_adv']].fillna('').agg(lambda x: ', '.join(filter(None, x)), axis=1)

# Rename columns for display
view_df = view_df.rename(columns=columns)

# Search functionality
# Display table
st.dataframe(
    view_df[[
        'Case Number', 'Petitioner', 'Respondent', 'Advocates', 'Judge', 'Bench', 'Date', 'Judgment PDF'
    ]],
    use_container_width=True
)