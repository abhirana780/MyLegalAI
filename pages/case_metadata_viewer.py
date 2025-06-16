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
search = st.text_input("Search by Case Number, Party, Advocate, or Judge")
if search:
    mask = (
        view_df['Case Number'].astype(str).str.contains(search, case=False, na=False) |
        view_df['Petitioner'].astype(str).str.contains(search, case=False, na=False) |
        view_df['Respondent'].astype(str).str.contains(search, case=False, na=False) |
        view_df['Advocates'].astype(str).str.contains(search, case=False, na=False) |
        view_df['Judge'].astype(str).str.contains(search, case=False, na=False)
    )
    view_df = view_df[mask]

# Sort functionality
sort_col = st.selectbox("Sort by", ['Case Number', 'Petitioner', 'Respondent', 'Advocates', 'Judge', 'Bench', 'Date'], index=6)
view_df = view_df.sort_values(by=sort_col, ascending=True)

# Format PDF link as clickable
def make_link(url):
    if pd.isna(url) or not str(url).startswith('http'):
        return ""
    return f'<a href="{url}" target="_blank">Open PDF</a>'

view_df['Judgment PDF'] = view_df['Judgment PDF'].apply(make_link)

# Display table
st.write(
    view_df[[
        'Case Number', 'Petitioner', 'Respondent', 'Advocates', 'Judge', 'Bench', 'Date', 'Judgment PDF'
    ]].to_html(escape=False, index=False), unsafe_allow_html=True
)