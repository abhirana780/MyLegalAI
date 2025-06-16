import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from notification_service import send_hearing_reminder
from notification_service import send_case_update
from court_jurisdiction_data import court_jurisdiction_data

st.set_page_config(
    page_title="Hearing Scheduler - Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("Hearing Scheduler")
st.markdown("### Manage Court Hearings, Deadlines, and Judge Information")

# Sidebar for navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Back to Home"):
    st.switch_page("app.py")

# Initialize session state for storing hearings and deadlines
if 'hearings' not in st.session_state:
    st.session_state.hearings = []

# Tab layout for different features
tabs = st.tabs(["Calendar View", "Document Templates"])

# Calendar View Tab
with tabs[0]:
    st.markdown("## Court Calendar")
    
    # Form for adding new hearing
    with st.expander("Schedule New Hearing"):
        col1, col2 = st.columns(2)
        
        with col1:
            hearing_date = st.date_input("Hearing Date")
            hearing_time = st.time_input("Hearing Time")
            court_name = st.selectbox(
                "Select Court",
                options=[court['name'] for court in court_jurisdiction_data.values() if isinstance(court, dict) and 'name' in court]
            )
            
        with col2:
            case_number = st.text_input("Case Number")
            case_title = st.text_input("Case Title")
            hearing_type = st.selectbox(
                "Hearing Type",
                ["Initial Hearing", "Motion Hearing", "Trial", "Pre-Trial Conference", "Status Conference", "Sentencing"]
            )
        
        if st.button("Add Hearing"):
            hearing = {
                'date': hearing_date,
                'time': hearing_time,
                'court': court_name,
                'case_number': case_number,
                'case_title': case_title,
                'type': hearing_type
            }
            st.session_state.hearings.append(hearing)
            # Schedule reminder notification
            reminder_date = datetime.combine(hearing_date, hearing_time) - timedelta(days=1)
            send_hearing_reminder(
                to_phone_number="",  # TODO: Add phone number field in the form
                case_ref=case_number,
                date=hearing_date.strftime("%Y-%m-%d"),
                time=hearing_time.strftime("%H:%M"),
                court=court_name,
                notes=f"Hearing Type: {hearing_type}"
            )
            st.success("Hearing scheduled successfully!")
    
    # Display upcoming hearings
    if st.session_state.hearings:
        st.markdown("### Upcoming Hearings")
        hearing_df = pd.DataFrame(st.session_state.hearings)
        hearing_df = hearing_df.sort_values(by=['date', 'time'])
        st.dataframe(hearing_df)
    else:
        st.info("No upcoming hearings scheduled.")

# Document Templates Tab
with tabs[1]:
    st.markdown("## Document Templates")
    st.markdown("### Access court-approved filing formats and templates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        template_type = st.selectbox(
            "Select Document Type",
            ["Plaint", "Written Statement", "Interim Application", "Affidavit", 
             "Vakalatnama", "Miscellaneous Application", "Appeal Memo"]
        )
    
    with col2:
        court_level = st.selectbox(
            "Select Court Level",
            ["High Court", "District Court", "Sub-Divisional Court"]
        )
    
    # Display template information
    if template_type and court_level:
        st.markdown(f"### {template_type} Template for {court_level}")
        st.markdown("#### Required Components:")
        
        # Template-specific requirements
        requirements = {
            "Plaint": [
                "Title of the case",
                "Jurisdiction clause",
                "Cause of action",
                "Relief sought",
                "Court fees details",
                "Verification and signature"
            ],
            "Written Statement": [
                "Preliminary objections",
                "Reply to allegations",
                "Additional facts",
                "Documents relied upon",
                "Prayer"
            ],
            "Affidavit": [
                "Deponent details",
                "Verification clause",
                "Notary attestation",
                "Identification proof"
            ]
        }
        
        if template_type in requirements:
            for req in requirements[template_type]:
                st.markdown(f"- {req}")
        
        # District-specific requirements
        st.markdown("#### Additional District Requirements:")
        st.markdown("- Number of copies required: 3")
        st.markdown("- Paper size: Legal (8.5\" × 14\")")
        st.markdown("- Font: Times New Roman, 14pt")
        st.markdown("- Line spacing: 1.5")
        
        # Download template button (placeholder)
        st.button("Download Template", type="primary")
