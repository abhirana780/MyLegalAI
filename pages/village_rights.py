import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from legal_data import get_jurisdiction_info

st.set_page_config(
    page_title="My Village, My Rights - Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    /* Global Styles */
    @keyframes pageLoad {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
        color: #2c3e50;
        transition: all 0.3s ease;
        animation: pageLoad 0.8s ease-out;
    }

    /* Village Card */
    @keyframes cardReveal {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .village-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 51, 102, 0.1);
        animation: cardReveal 0.6s ease-out;
        transition: all 0.3s ease;
    }

    .village-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }

    /* Stats Section */
    @keyframes statsSlide {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stats-section {
        background: linear-gradient(to right, #f8f9fa, #ffffff);
        border-left: 4px solid #003366;
        border-radius: 0 8px 8px 0;
        padding: 15px;
        margin-bottom: 15px;
        animation: statsSlide 0.5s ease-out;
        transition: all 0.3s ease;
    }

    .stats-section:hover {
        background: linear-gradient(to right, #f0f2f5, #ffffff);
        transform: scale(1.01);
    }
</style>
""", unsafe_allow_html=True)

st.title("My Village, My Rights")
st.markdown("### Explore Legal History and Rights of Your Village")

# Sidebar for navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Back to Home"):
    st.switch_page("app.py")

# Load jurisdiction data
jurisdictions = get_jurisdiction_info()

# State and District Selection
col1, col2 = st.columns(2)

with col1:
    # Only Himachal Pradesh state
    selected_state = "Himachal Pradesh"

with col2:
    # Himachal Pradesh districts and their tehsils
    districts = {
        "Bilaspur": ["Bilaspur Sadar", "Ghumarwin", "Jhandutta", "Naina Devi", "Kot Kehloor"],
        "Chamba": ["Chamba", "Dalhousie", "Bharmour", "Pangi", "Tissa", "Salooni", "Churah"],
        "Hamirpur": ["Hamirpur", "Barsar", "Nadaun", "Bhoranj", "Sujanpur"],
        "Kangra": ["Dharamshala", "Palampur", "Nurpur", "Dehra", "Kangra", "Jawali", "Jaisinghpur", "Fatehpur", "Indora", "Baijnath", "Nagrota Bagwan"],
        "Kinnaur": ["Kalpa", "Nichar", "Pooh", "Sangla"],
        "Kullu": ["Kullu", "Manali", "Banjar", "Anni", "Nirmand", "Sainj"],
        "Lahaul and Spiti": ["Keylong", "Kaza", "Udaipur", "Spiti", "Sissu"],
        "Mandi": ["Mandi Sadar", "Sundernagar", "Jogindernagar", "Sarkaghat", "Karsog", "Dharampur", "Padhar", "Balh", "Gohar", "Chachyot", "Aut"],
        "Shimla": ["Shimla Urban", "Shimla Rural", "Theog", "Rampur", "Rohru", "Chopal", "Kumarsain", "Kotkhai", "Jubbal", "Nankhari", "Seoni"],
        "Sirmaur": ["Nahan", "Paonta Sahib", "Rajgarh", "Shillai", "Sangrah", "Renuka"],
        "Solan": ["Solan", "Nalagarh", "Arki", "Kandaghat", "Kasauli", "Baddi", "Darlaghat"],
        "Una": ["Una", "Amb", "Gagret", "Haroli", "Bangana", "Chintpurni"]
    }
    selected_district = st.selectbox("Select District", ["Select District"] + list(districts.keys()))

# Village/Tehsil Selection
if selected_district != "Select District" and selected_state != "Select State":
    # Get tehsils for selected district
    tehsils = districts.get(selected_district, [])
    selected_tehsil = st.selectbox("Select Tehsil", ["Select Tehsil"] + tehsils)

    if selected_tehsil != "Select Tehsil":
        # Display village information
        st.markdown("## Village Legal Profile")

        # Generate comprehensive village data
        def generate_village_data(selected_district, selected_tehsil):
            import numpy as np
            import random
            # Case categories with detailed breakdown
            categories = [
                "Land Disputes", "Family Matters", "Criminal Cases", 
                "Civil Disputes", "Revenue Cases", "Panchayat Matters",
                "Environmental Issues", "Public Interest Litigation",
                "Consumer Disputes", "Labor Disputes"
            ]
            # Seed for reproducibility based on district/tehsil
            seed = hash(f"{selected_district}-{selected_tehsil}") % (2**32)
            random.seed(seed)
            np.random.seed(seed)
            # Generate unique case counts and stats
            base = random.randint(10, 60)
            case_counts = pd.DataFrame({
                'Category': categories,
                'Count': [base + random.randint(-10, 20) for _ in categories],
                'Severity': random.choices(['High', 'Medium', 'Low'], k=len(categories)),
                'Resolution_Rate': [random.randint(40, 95) for _ in categories]
            })
            # Generate monthly trends
            months = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
            new_cases = np.abs(np.random.normal(loc=15 + base//5, scale=3, size=len(months))).astype(int)
            resolved_cases = np.abs(new_cases - np.random.randint(0, 5, size=len(months)))
            pending_cases = np.cumsum(new_cases - resolved_cases) + random.randint(10, 30)
            avg_resolution_time = np.abs(np.random.normal(loc=35, scale=5, size=len(months))).astype(int)
            monthly_trends = pd.DataFrame({
                'Month': months,
                'New Cases': new_cases,
                'Resolved Cases': resolved_cases,
                'Pending Cases': pending_cases,
                'Average Resolution Time (days)': avg_resolution_time
            })
            # Generate land revenue data
            years = range(2020, 2024)
            total_revenue = [random.randint(100, 200) for _ in years]
            collection_rate = [random.randint(80, 99) for _ in years]
            disputes = [random.randint(5, 20) for _ in years]
            land_revenue = pd.DataFrame({
                'Year': years,
                'Total Revenue (Lakhs)': total_revenue,
                'Collection Rate (%)': collection_rate,
                'Disputes': disputes
            })
            # Generate Lok Adalat schedule
            venues = ['District Court', 'Tehsil Office', 'Panchayat Bhawan', 'Mobile Court', 'Community Center']
            case_types = ['All Types', 'Revenue Cases', 'Family Matters', 'Civil Disputes', 'Consumer Cases']
            lok_adalat = pd.DataFrame({
                'Date': pd.date_range(start='2024-01-01', periods=6, freq='M'),
                'Venue': random.choices(venues, k=6),
                'Case Types': random.choices(case_types, k=6),
                'Expected Cases': [random.randint(20, 120) for _ in range(6)],
                'Registration Status': random.choices(['Open', 'Closed', 'Closing Soon'], k=6)
            })
            # Add more data points for richer experience
            # Example: Legal aid camps, awareness drives, digital case filings
            legal_aid_camps = pd.DataFrame({
                'Date': pd.date_range(start='2024-02-01', periods=4, freq='2M'),
                'Location': random.choices(venues, k=4),
                'Beneficiaries': [random.randint(30, 200) for _ in range(4)],
                'Focus Area': random.choices(['Women', 'Farmers', 'Senior Citizens', 'Youth'], k=4)
            })
            return case_counts, monthly_trends, land_revenue, lok_adalat, legal_aid_camps

        case_counts, monthly_trends, land_revenue, lok_adalat, legal_aid_camps = generate_village_data(selected_district, selected_tehsil)

        # Display case statistics with enhanced visualization
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Case Statistics")
            fig = px.pie(case_counts, values='Count', names='Category',
                        title='Distribution of Legal Cases',
                        hover_data=['Severity', 'Resolution_Rate'],
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        with col2:
            st.markdown("### Case Resolution Trends")
            fig = px.line(monthly_trends, x='Month',
                         y=['New Cases', 'Resolved Cases', 'Pending Cases'],
                         title='Monthly Case Trends',
                         color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c'])
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig)

        # Display resolution time trends
        st.markdown("### Case Resolution Time Analysis")
        fig = px.line(monthly_trends, x='Month', y='Average Resolution Time (days)',
                     title='Average Case Resolution Time Trends',
                     color_discrete_sequence=['#9b59b6'])
        st.plotly_chart(fig)

        # Display land revenue analysis
        st.markdown("### Land Revenue Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Revenue Collection Trends")
            fig = px.bar(land_revenue, x='Year', y='Total Revenue (Lakhs)', color='Collection Rate (%)',
                        title='Yearly Land Revenue Collection',
                        color_continuous_scale=px.colors.sequential.Blues)
            st.plotly_chart(fig)
        with col2:
            st.markdown("#### Revenue Disputes")
            fig = px.bar(land_revenue, x='Year', y='Disputes', color='Disputes',
                        title='Land Revenue Disputes by Year',
                        color_continuous_scale=px.colors.sequential.Reds)
            st.plotly_chart(fig)
        # Display Lok Adalat schedule
        st.markdown("### Lok Adalat Schedule")
        st.dataframe(lok_adalat)
        # Display Legal Aid Camps
        st.markdown("### Legal Aid Camps & Awareness Drives")
        st.dataframe(legal_aid_camps)

        # Common Legal Issues with Enhanced Information
        st.markdown("### Common Legal Issues and Resolution Pathways")
        common_issues = [
            {
                "issue": "Land Boundary Disputes",
                "frequency": "High",
                "resolution_time": "3-6 months",
                "resolution_steps": [
                    "File complaint with Revenue Department",
                    "Land survey and demarcation",
                    "Mediation through Gram Panchayat",
                    "Appeal to SDM if needed"
                ],
                "required_documents": [
                    "Land ownership papers",
                    "Revenue records (Khatauni)",
                    "Previous court orders if any",
                    "Survey maps"
                ]
            },
            {
                "issue": "Water Rights and Distribution",
                "frequency": "Medium",
                "resolution_time": "2-4 months",
                "resolution_steps": [
                    "Register complaint with Irrigation Department",
                    "Assessment by technical team",
                    "Community consultation",
                    "Implementation of water sharing schedule"
                ],
                "required_documents": [
                    "Water connection details",
                    "Previous water usage records",
                    "Land holding documents"
                ]
            },
            {
                "issue": "Agricultural Contract Disputes",
                "frequency": "Medium",
                "resolution_time": "1-3 months",
                "resolution_steps": [
                    "File case in Gram Nyayalaya",
                    "Document verification",
                    "Mediation process",
                    "Final settlement"
                ],
                "required_documents": [
                    "Contract agreement",
                    "Crop records",
                    "Payment receipts",
                    "Market rate documents"
                ]
            },
            {
                "issue": "Family Property Division",
                "frequency": "High",
                "resolution_time": "6-12 months",
                "resolution_steps": [
                    "Family consultation",
                    "Property valuation",
                    "Legal documentation",
                    "Registration of division"
                ],
                "required_documents": [
                    "Property ownership papers",
                    "Family tree documentation",
                    "Previous partition deeds if any",
                    "Tax records"
                ]
            },
            {
                "issue": "Environmental Violations",
                "frequency": "Medium",
                "resolution_time": "2-5 months",
                "resolution_steps": [
                    "Report to Pollution Control Board",
                    "Site inspection",
                    "Corrective action plan",
                    "Compliance verification"
                ],
                "required_documents": [
                    "Photographic evidence",
                    "Environmental impact reports",
                    "Previous notices if any",
                    "Local authority permissions"
                ]
            }
        ]

        for issue in common_issues:
            with st.expander(f"{issue['issue']} (Frequency: {issue['frequency']}):"):
                st.markdown(f"**Average Resolution Time:** {issue['resolution_time']}")
                
                st.markdown("**Resolution Steps:**")
                for step in issue['resolution_steps']:
                    st.markdown(f"- {step}")
                
                st.markdown("**Required Documents:**")
                for doc in issue['required_documents']:
                    st.markdown(f"- {doc}")
                
                # Add a button to download resolution guidelines
                if st.button(f"Download {issue['issue']} Guidelines", key=f"download_{issue['issue'].replace(' ', '_')}"):
                    st.markdown(f"Guidelines for {issue['issue']} will be downloaded (Feature coming soon)")

        # Land Revenue Mutation History
        st.markdown("### Land Revenue Mutation History")
        mutations = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=5, freq='M'),
            'Type': ['Sale', 'Inheritance', 'Division', 'Mortgage', 'Release'],
            'Area (Acres)': [2.5, 1.8, 3.2, 1.5, 2.0],
            'Status': ['Completed', 'Pending', 'Completed', 'Under Review', 'Completed']
        })
        st.dataframe(mutations)

        # Upcoming Lok Adalat Sessions
        st.markdown("### Upcoming Lok Adalat Sessions")
        lok_adalat = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', periods=3, freq='M'),
            'Venue': ['District Court Complex', 'Tehsil Office', 'Panchayat Bhawan'],
            'Cases Type': ['Civil & Revenue', 'Family Matters', 'Land Disputes'],
            'Registration Status': ['Open', 'Open', 'Closing Soon']
        })
        st.dataframe(lok_adalat)

        # Legal Resources and Contacts
        st.markdown("### Legal Resources & Important Contacts")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Legal Aid Clinic")
            st.markdown("""
            - **Location**: Tehsil Office Complex
            - **Timing**: Monday to Friday, 10 AM - 4 PM
            - **Services**: Free Legal Consultation, Document Review
            - **Contact**: +91-XXXXXXXXXX
            """)

        with col2:
            st.markdown("#### Emergency Contacts")
            st.markdown("""
            - **Police Station**: 100, +91-XXXXXXXXXX
            - **Revenue Officer**: +91-XXXXXXXXXX
            - **Gram Pradhan**: +91-XXXXXXXXXX
            - **Legal Aid Cell**: +91-XXXXXXXXXX
            """)

        # Download Reports Section
        st.markdown("### Download Reports")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="📊 Case Statistics Report",
                data="Sample Report Data",
                file_name="case_statistics.pdf",
                mime="application/pdf"
            )

        with col2:
            st.download_button(
                label="📜 Land Revenue Report",
                data="Sample Report Data",
                file_name="land_revenue.pdf",
                mime="application/pdf"
            )

        with col3:
            st.download_button(
                label="📋 Legal Issues Summary",
                data="Sample Report Data",
                file_name="legal_issues.pdf",
                mime="application/pdf"
            )