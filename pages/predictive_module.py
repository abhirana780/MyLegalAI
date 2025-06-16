import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from datetime import timedelta
import plotly.express as px
st.set_page_config(page_title="Predictive Module (ML-based)", page_icon="📈", layout="wide")
st.title("📈 Predictive Module (ML-based)")
st.markdown("""
This module predicts:
- **Judgment type** based on parties
- **Judge likely to deliver a decision**
- **Case outcome date**

*Powered by simple ML models trained on your judgments CSV.*
""")

# Load data
def load_data():
    df = pd.read_csv('assets/judgments.csv')
    # Convert judgment_dates to datetime
    df['judgment_dates'] = pd.to_datetime(df['judgment_dates'], format='%d-%m-%Y', errors='coerce')
    return df

df = load_data()

# Feature engineering
def prepare_features(df):
    data = df.copy()
    # Fill missing values
    data['pet'] = data['pet'].fillna('Unknown')
    data['res'] = data['res'].fillna('Unknown')
    data['judgement_by'] = data['judgement_by'].fillna('Unknown')
    data['Judgement_type'] = data['Judgement_type'].fillna('Other')
    # Encode parties (petitioner/respondent) as categorical features
    le_pet = LabelEncoder()
    le_res = LabelEncoder()
    data['pet_encoded'] = le_pet.fit_transform(data['pet'])
    data['res_encoded'] = le_res.fit_transform(data['res'])
    # Encode judge
    le_judge = LabelEncoder()
    data['judge_encoded'] = le_judge.fit_transform(data['judgement_by'])
    # Encode judgment type
    le_type = LabelEncoder()
    data['type_encoded'] = le_type.fit_transform(data['Judgement_type'])
    # Outcome date as days since earliest date
    min_date = data['judgment_dates'].min()
    data['days_since_start'] = (data['judgment_dates'] - min_date).dt.days
    return data, le_pet, le_res, le_judge, le_type, min_date

data, le_pet, le_res, le_judge, le_type, min_date = prepare_features(df)

# Sidebar for user input
st.sidebar.header("Prediction Input")
pet_input = st.sidebar.selectbox("Petitioner", sorted(df['pet'].dropna().unique()))
res_input = st.sidebar.selectbox("Respondent", sorted(df['res'].dropna().unique()))

# Predict Judgment Type
st.markdown("## 🏷️ Predict Judgment Type")
X_type = data[['pet_encoded', 'res_encoded']]
y_type = data['type_encoded']
clf_type = RandomForestClassifier(n_estimators=100, random_state=42)
clf_type.fit(X_type, y_type)

pet_val = le_pet.transform([pet_input])[0] if pet_input in le_pet.classes_ else 0
res_val = le_res.transform([res_input])[0] if res_input in le_res.classes_ else 0
pred_type_encoded = clf_type.predict([[pet_val, res_val]])[0]
pred_type = le_type.inverse_transform([pred_type_encoded])[0]
st.success(f"**Predicted Judgment Type:** {pred_type}")

# Predict Judge
st.markdown("## 👨‍⚖️ Predict Likely Judge")
X_judge = data[['pet_encoded', 'res_encoded', 'type_encoded']]
y_judge = data['judge_encoded']
clf_judge = RandomForestClassifier(n_estimators=100, random_state=42)
clf_judge.fit(X_judge, y_judge)

pred_judge_encoded = clf_judge.predict([[pet_val, res_val, pred_type_encoded]])[0]
pred_judge = le_judge.inverse_transform([pred_judge_encoded])[0]
st.info(f"**Likely Judge:** {pred_judge}")

# Predict Outcome Date
st.markdown("## 📅 Predict Case Outcome Date")
X_date = data[['pet_encoded', 'res_encoded', 'type_encoded', 'judge_encoded']]
y_date = data['days_since_start']
reg_date = RandomForestRegressor(n_estimators=100, random_state=42)
reg_date.fit(X_date, y_date)

pred_days = int(reg_date.predict([[pet_val, res_val, pred_type_encoded, pred_judge_encoded]])[0])
pred_date = min_date + timedelta(days=pred_days)
st.warning(f"**Estimated Outcome Date:** {pred_date.strftime('%d-%m-%Y')}")

# Show feature importances (optional)
with st.expander("Show Feature Importances"):
    st.write("Judgment Type Model:")
    st.bar_chart(pd.Series(clf_type.feature_importances_, index=['pet', 'res']))
    st.write("Judge Model:")
    st.bar_chart(pd.Series(clf_judge.feature_importances_, index=['pet', 'res', 'type']))
    st.write("Outcome Date Model:")
    st.bar_chart(pd.Series(reg_date.feature_importances_, index=['pet', 'res', 'type', 'judge']))

# BONUS: Placeholder for NLP modules
st.markdown("---")
st.markdown("### 💡 BONUS: NLP Modules (Coming Soon)")
st.markdown("""
- Download full judgments using temp_link
- Auto-summarize case
- Extract IPC sections
- Power a chatbot
""")