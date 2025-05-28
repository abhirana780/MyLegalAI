import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from legal_data import get_offense_details
from amendment_data import get_amendment_history, get_latest_amendment, get_recent_amendments

def main():
    st.set_page_config(
        page_title="Amendment Tracker - Indian Legal Assistant",
        page_icon="⚖️",
        layout="wide"
    )

    st.markdown("""
    <style>
        .amendment-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(0,51,102,0.1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        .amendment-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        .date-badge {
            background: #003366;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
            margin-bottom: 10px;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("📜 Legal Amendment Tracker")
    st.subheader("Track and analyze legal amendments in real-time")

# Sidebar for navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Back to Home"):
        st.switch_page("app.py")

# Recent Amendments Section
    st.markdown("## Recent Amendments")

# Allow user to select time period for recent amendments
    time_period = st.selectbox(
        "Show amendments from last:",
        ["30 days", "90 days", "180 days", "365 days"],
        index=1
    )

# Convert selection to number of days
    days = int(time_period.split()[0])

# Get live amendments
    from amendment_scraper import scrape_india_code

    with st.spinner("Fetching latest amendments..."):
        recent_amendments = scrape_india_code()

        if not recent_amendments:
            st.warning("Unable to fetch live amendments. Please try again later.")
        else:
            st.success(f"Found {len(recent_amendments)} recent amendments")

# Sort amendments by date in descending order
    recent_amendments = sorted(recent_amendments, key=lambda x: datetime.strptime(x['implementation_date'], '%Y-%m-%d'), reverse=True)

    if recent_amendments:
        for amendment in recent_amendments:
            with st.expander(f"{amendment['act']} Section {amendment['section']} - {amendment['implementation_date']}"):
                st.markdown(f"**Implementation Date:** {amendment['implementation_date']}")
                st.markdown(f"**Summary:** {amendment['summary']}")

            # Get full amendment details
                full_details = get_amendment_history(amendment['act'], amendment['section'])
                latest = get_latest_amendment(amendment['act'], amendment['section'])

                if latest:
                # Create columns for old vs new comparison
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### Previous Version")
                        st.markdown(f"""```
{latest['old_text']}
```""")

                    with col2:
                        st.markdown("### Current Version")
                        st.markdown(f"""```
{latest['new_text']}
```""")

                    st.markdown(f"**Amendment Act:** {latest['amendment_act']}")
    else:
        st.info(f"No amendments found in the last {days} days.")

# Amendment History Search
    st.markdown("## Search Amendment History")

# Create two columns for act and section selection
    col1, col2 = st.columns(2)

    with col1:
        act = st.selectbox(
            "Select Act",
            ["IPC", "CrPC", "CPC", "Evidence Act", "IT Act", "MV Act"]
        )

    with col2:
    # Get section based on selected act
        section = st.text_input(
            "Enter Section Number",
            help="Enter the section number to view its amendment history"
        )

    if act and section:
        history = get_amendment_history(act, section)

        if history:
            st.markdown(f"### Amendment History for {act} Section {section}")

        # Create a timeline of amendments
            for amendment in sorted(history, key=lambda x: x['implementation_date']):
                with st.expander(f"Amendment on {amendment['implementation_date']}"):
                    st.markdown(f"**Implementation Date:** {amendment['implementation_date']}")
                    st.markdown(f"**Amendment Act:** {amendment['amendment_act']}")
                    st.markdown(f"**Summary:** {amendment['summary']}")

                # Show the changes
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### Previous Version")
                        st.markdown(f"""```
{amendment['old_text']}
```""")

                    with col2:
                        st.markdown("### Current Version")
                        st.markdown(f"""```
{amendment['new_text']}
```""")
        else:
            st.info(f"No amendment history found for {act} Section {section}.")

if __name__ == "__main__":
    main()