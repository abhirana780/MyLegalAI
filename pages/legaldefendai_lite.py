import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

st.set_page_config(
    page_title="⚖️ LegalDefendAI Lite (Metadata Matching)",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalDefendAI Lite (Metadata Matching)")
st.markdown("""
Assist lawyers in researching similar past cases by matching party or advocate names to past judgments using metadata similarity.
""")

# --- Load Judgments CSV ---
JUDGMENTS_CSV = os.path.join("assets", "judgments.csv")
if not os.path.exists(JUDGMENTS_CSV):
    st.error("Judgments CSV not found at 'assets/judgments.csv'. Please upload the file.")
    st.stop()

@st.cache_data(show_spinner=False)
def load_judgments():
    df = pd.read_csv(JUDGMENTS_CSV)
    # Standardize column names
    df.columns = [c.strip().lower() for c in df.columns]
    # Ensure 'year' column exists
    if 'year' not in df.columns:
        if 'judgment_dates' in df.columns:
            df['judgment_dates'] = pd.to_datetime(df['judgment_dates'], errors='coerce')
            df['year'] = df['judgment_dates'].dt.year
        else:
            df['year'] = None
    return df

judgments = load_judgments()

# --- Input Section ---
st.header("Search for Similar Past Cases")
input_type = st.radio("Search by:", ["Party Name", "Advocate Name"], horizontal=True)
user_query = st.text_input(f"Enter {input_type}", "")

# --- Filter Section ---
st.subheader("Filters")
years = sorted(judgments["year"].dropna().unique())
benches = sorted(judgments["bench"].dropna().unique())
col1, col2 = st.columns(2)
with col1:
    year_filter = st.multiselect("Year", years, default=years)
with col2:
    bench_filter = st.multiselect("Bench", benches, default=benches)

# --- Prepare Data for TF-IDF ---
# We'll use 'pet', 'res', 'pet_adv' columns for similarity
judgments["meta_text"] = (
    judgments["pet"].fillna("") + " " +
    judgments["res"].fillna("") + " " +
    judgments["pet_adv"].fillna("")
)

# --- Filter by Year and Bench ---
filtered = judgments[
    judgments["year"].isin(year_filter) &
    judgments["bench"].isin(bench_filter)
].copy()

# --- TF-IDF Similarity Search ---
def find_similar_cases(query, df, input_type):
    if input_type == "Party Name":
        # Search in 'pet' and 'res'
        search_text = df["pet"].fillna("") + " " + df["res"].fillna("")
    else:
        # Search in 'pet_adv'
        search_text = df["pet_adv"].fillna("")
    corpus = search_text.tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus + [query])
    query_vec = tfidf_matrix[-1]
    corpus_vecs = tfidf_matrix[:-1]
    similarities = cosine_similarity(query_vec, corpus_vecs).flatten()
    df = df.copy()
    df["similarity"] = similarities
    return df.sort_values("similarity", ascending=False)

# --- Results Section ---
if user_query.strip():
    with st.spinner("Finding similar cases..."):
        results = find_similar_cases(user_query.strip(), filtered, input_type)
        # Show only top 20 matches with similarity > 0.1
        results = results[results["similarity"] > 0.1].head(20)
        if not results.empty:
            st.success(f"Found {len(results)} similar cases.")
            st.dataframe(
                results[["year", "bench", "pet", "res", "pet_adv", "case_title", "similarity"]]
                .rename(columns={
                    "pet": "Petitioner",
                    "res": "Respondent",
                    "pet_adv": "Pet. Advocate",
                    "case_title": "Case Title",
                    "similarity": "Similarity Score"
                }),
                use_container_width=True
            )
        else:
            st.info("No similar cases found. Try a different query or relax filters.")
else:
    st.info("Enter a party or advocate name to search for similar past cases.")

st.markdown("---")
st.caption("LegalDefendAI Lite helps lawyers quickly research relevant precedents based on metadata. Powered by TF-IDF similarity on party and advocate names.")