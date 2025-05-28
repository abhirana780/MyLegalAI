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
if 'deadlines' not in st.session_state:
    st.session_state.deadlines = []

# Tab layout for different features
tabs = st.tabs(["Calendar View", "Filing Deadlines", "Judge Roster", "Timeline Visualizer", "Document Templates"])

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

# Filing Deadlines Tab
with tabs[1]:
    st.markdown("## Filing Deadlines")
    
    # Form for adding new deadline
    with st.expander("Add New Filing Deadline"):
        col1, col2 = st.columns(2)
        
        with col1:
            deadline_date = st.date_input("Deadline Date")
            case_number_deadline = st.text_input("Case Number", key="deadline_case")
            filing_type = st.selectbox(
                "Filing Type",
                ["Motion", "Response", "Reply", "Brief", "Petition", "Appeal", "Other Documents"]
            )
            
        with col2:
            description = st.text_area("Description")
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        if st.button("Add Deadline"):
            deadline = {
                'date': deadline_date,
                'case_number': case_number_deadline,
                'filing_type': filing_type,
                'description': description,
                'priority': priority
            }
            st.session_state.deadlines.append(deadline)
            # Schedule reminder notification
            reminder_date = deadline_date - timedelta(days=3)
            send_case_update(
                to_phone_number="",  # TODO: Add phone number field in the form
                case_ref=case_number_deadline,
                update_message=f"Filing Deadline: {filing_type} due on {deadline_date.strftime('%Y-%m-%d')}",
                notes=description,
                date=deadline_date.strftime("%Y-%m-%d")
            )
            st.success("Deadline added successfully!")
    
    # Display deadlines
    if st.session_state.deadlines:
        st.markdown("### Upcoming Deadlines")
        deadline_df = pd.DataFrame(st.session_state.deadlines)
        deadline_df = deadline_df.sort_values(by='date')
        st.dataframe(deadline_df)
    else:
        st.info("No upcoming filing deadlines.")

# Judge Roster Tab
with tabs[2]:
    st.markdown("## Judge Roster")
    
    # Search functionality for judges
    search_court = st.selectbox(
        "Select Court",
        options=[court['name'] for court in court_jurisdiction_data.values() if isinstance(court, dict) and 'name' in court],
        key="judge_roster_court_select"
    )
    
    # Display court information
    if search_court:
        court_info = next((court for court in court_jurisdiction_data.values() 
                         if isinstance(court, dict) and 'name' in court and court['name'] == search_court), None)
        if court_info:
            st.markdown(f"### {court_info['name']}")
            st.markdown(f"**Type:** {court_info['type']}")
            st.markdown(f"**Address:** {court_info['address']}")
            if 'contact' in court_info:
                st.markdown(f"**Contact:** {court_info['contact']}")
            if 'powers' in court_info:
                st.markdown("**Powers and Jurisdiction:**")
                for power in court_info['powers']:
                    st.markdown(f"- {power}")

# Timeline Visualizer Tab
with tabs[3]:
    st.markdown("## Case Timeline Visualizer")
    st.markdown("### Track case progression and important deadlines")
    
    # Case selection
    case_number_timeline = st.text_input("Enter Case Number for Timeline")
    
    if case_number_timeline:
        # Find all events for this case
        case_events = []
        
        # Add hearings for this case
        for hearing in st.session_state.hearings:
            if hearing['case_number'] == case_number_timeline:
                case_events.append({
                    'date': hearing['date'],
                    'event_type': 'Hearing',
                    'description': f"{hearing['type']} at {hearing['court']}"
                })
        
        # Add deadlines for this case
        for deadline in st.session_state.deadlines:
            if deadline['case_number'] == case_number_timeline:
                case_events.append({
                    'date': deadline['date'],
                    'event_type': 'Deadline',
                    'description': f"{deadline['filing_type']} - {deadline['description']}"
                })
        
        if case_events:
            # Convert to DataFrame and sort by date
            timeline_df = pd.DataFrame(case_events)
            timeline_df = timeline_df.sort_values(by='date')
            
            # Display timeline
            st.markdown("### Case Timeline")
            for _, event in timeline_df.iterrows():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"**{event['date'].strftime('%Y-%m-%d')}**")
                with col2:
                    st.markdown(f"**{event['event_type']}**: {event['description']}")
        else:
            st.info("No events found for this case number.")
    
    # District-specific processing times
    st.markdown("### District Court Processing Times")
    district = st.selectbox(
        "Select District",
        ["Shimla", "Mandi", "Kangra", "Kullu", "Solan", "Una", "Bilaspur", "Hamirpur", "Chamba", "Sirmaur", "Kinnaur", "Lahaul and Spiti"]
    )
    
    if district:
        st.markdown(f"#### Estimated Processing Times for {district} District Court:")
        processing_times = {
            "Civil Cases": "4-6 months",
            "Criminal Cases": "3-4 months",
            "Family Matters": "2-3 months",
            "Property Disputes": "6-8 months"
        }
        for case_type, duration in processing_times.items():
            st.markdown(f"- **{case_type}**: {duration}")

# Document Templates Tab
with tabs[4]:
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