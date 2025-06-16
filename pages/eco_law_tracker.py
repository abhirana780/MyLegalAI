import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import MarkerCluster

@st.cache_data(show_spinner=False)
def load_eco_cases():
    # Enhanced sample data generation for richer analytics
    import numpy as np
    np.random.seed(42)
    num_cases = 5000 # Reduced for faster loading during development earlier 5000
    case_types = [
        'Forest Encroachment', 'Wildlife Offense', 'Hydropower Litigation', 'Pollution Case', 'Illegal Mining',
        'Poaching', 'Deforestation', 'River Pollution', 'Industrial Waste', 'Protected Area Violation',
        'Wetland Destruction', 'Mangrove Loss', 'Air Pollution', 'Noise Pollution', 'Soil Erosion',
        'Climate Change Litigation', 'Biodiversity Loss', 'Hazardous Waste', 'Overfishing', 'Urban Expansion'
    ]
    locations = [
        'Karnataka', 'Maharashtra', 'Uttarakhand', 'Gujarat', 'Tamil Nadu', 'Assam', 'Kerala', 'Madhya Pradesh',
        'Rajasthan', 'West Bengal', 'Odisha', 'Chhattisgarh', 'Jharkhand', 'Goa', 'Punjab', 'Delhi', 'Haryana',
        'Telangana', 'Andhra Pradesh', 'Tripura', 'Nagaland', 'Manipur', 'Meghalaya', 'Sikkim', 'Himachal Pradesh'
    ]
    statuses = ['Pending'] * 15 + ['In Progress'] * 20 + ['Under Review'] * 10 + ['Resolved'] * 35 + ['Closed'] * 15 + ['Appealed'] * 5
    priorities = ['High'] * 20 + ['Medium'] * 50 + ['Low'] * 30
    petitioners = [
        'State Forest Dept', 'Wildlife Trust', 'Environmental NGO', 'Local Community', 'State Board', 'Citizen Group',
        'Tribal Council', 'River Authority', 'Green Tribunal', 'Forest Rangers', 'Academic Institution', 'Youth Group',
        'Women\'s Collective', 'Village Panchayat', 'Farmers Association'
    ]
    respondents = [
        'Private Company', 'Local Resident', 'Power Corp', 'Mining Corp', 'Industry Group', 'Municipal Body', 'Unknown',
        'Tourism Operator', 'Contractor', 'Agricultural Firm', 'Construction Company', 'Transport Authority', 'Real Estate Developer'
    ]
    eco_zone_types = [
        'Protected Forest', 'Wildlife Sanctuary', 'River Basin', 'National Park', 'Tiger Reserve', 'Wetland',
        'Biosphere Reserve', 'Mangrove', 'Hill Ecosystem', 'Grassland', 'Urban Green Space', 'Desert Ecosystem'
    ]
    impact_levels = ['Severe'] * 10 + ['Moderate'] * 20 + ['High'] * 25 + ['Low'] * 25 + ['Critical'] * 10 + ['Minimal'] * 10
    compliance_statuses = ['Non-Compliant'] * 10 + ['Partially Compliant'] * 20 + ['Under Review'] * 10 + ['Compliant'] * 50 + ['Not Applicable'] * 10
    clearance_statuses = ['Pending'] * 20 + ['Approved'] * 50 + ['Rejected'] * 5 + ['Under Review'] * 15 + ['Conditionally Approved'] * 10
    species_affected = [
        'Bengal Tiger', 'Asian Elephant', 'River Dolphins', 'Snow Leopard', 'One-horned Rhino', 'Leopard', 'Sloth Bear',
        'Gharial', 'Hornbill', 'Red Panda', 'Olive Ridley Turtle', 'Indian Bustard', 'Blackbuck', 'Sarus Crane', 'King Cobra'
    ]

    lats = np.random.uniform(8.0, 34.0, num_cases)
    lons = np.random.uniform(68.0, 92.0, num_cases)
    filing_dates = pd.date_range(start='2018-01-01', periods=num_cases, freq='D')
    next_hearings = filing_dates + pd.to_timedelta(np.random.randint(30, 365, num_cases), unit='D')
    affected_areas = np.random.randint(10, 50000, num_cases)  # Broader range for realism

    # Simulate more realistic status and priority distributions
    status_choices = np.random.choice(['Pending', 'In Progress', 'Under Review', 'Resolved', 'Closed', 'Appealed'], num_cases, p=[0.18, 0.22, 0.10, 0.30, 0.15, 0.05])
    priority_choices = np.random.choice(['High', 'Medium', 'Low'], num_cases, p=[0.22, 0.48, 0.30])
    impact_choices = np.random.choice(['Severe', 'Moderate', 'High', 'Low', 'Critical', 'Minimal'], num_cases, p=[0.12, 0.22, 0.28, 0.22, 0.10, 0.06])
    compliance_choices = np.random.choice(['Non-Compliant', 'Partially Compliant', 'Under Review', 'Compliant', 'Not Applicable'], num_cases, p=[0.10, 0.18, 0.12, 0.50, 0.10])
    clearance_choices = np.random.choice(['Pending', 'Approved', 'Rejected', 'Under Review', 'Conditionally Approved'], num_cases, p=[0.18, 0.55, 0.05, 0.12, 0.10])

    data = {
        'case_type': np.random.choice(case_types, num_cases),
        'location': np.random.choice(locations, num_cases),
        'status': status_choices,
        'lat': lats,
        'lon': lons,
        'filing_date': filing_dates,
        'priority': priority_choices,
        'next_hearing': next_hearings,
        'petitioner': np.random.choice(petitioners, num_cases),
        'respondent': np.random.choice(respondents, num_cases),
        'eco_zone_type': np.random.choice(eco_zone_types, num_cases),
        'impact_level': impact_choices,
        'compliance_status': compliance_choices,
        'clearance_status': clearance_choices,
        'affected_area': affected_areas,
        'species_affected': np.random.choice(species_affected, num_cases)
    }
    return pd.DataFrame(data)

@st.cache_data(show_spinner=False)
def load_eco_zones():
    # Placeholder function to load environmental sensitive zones
    return pd.DataFrame({
        'zone_name': ['Bandipur Tiger Reserve', 'Kaziranga National Park', 'Sundarbans', 'Jim Corbett', 'Gir Forest'],
        'zone_type': ['Tiger Reserve', 'National Park', 'Mangrove Forest', 'National Park', 'Wildlife Sanctuary'],
        'lat': [11.6700, 26.6700, 21.9497, 29.5300, 21.1200],
        'lon': [76.6300, 93.4200, 88.8000, 78.7747, 70.8000],
        'area': [87400, 42996, 140000, 52082, 258800],  # in hectares
        'biodiversity_index': [9.2, 8.9, 9.5, 8.8, 8.7],
        'threat_level': ['High', 'Critical', 'Severe', 'Moderate', 'High']
    })

@st.cache_data(show_spinner=False)
def load_satellite_imagery():
    # Placeholder function to load satellite imagery layers
    # In real implementation, this would integrate with Earth observation APIs
    return {
        'forest_cover': {
            'url': 'https://example.com/api/forest-cover-tiles/{z}/{x}/{y}',
            'attribution': '© Forest Cover Data by Environmental Monitoring Agency'
        },
        'water_bodies': {
            'url': 'https://example.com/api/water-bodies-tiles/{z}/{x}/{y}',
            'attribution': '© Water Bodies Data by Environmental Monitoring Agency'
        },
        'land_use': {
            'url': 'https://example.com/api/land-use-tiles/{z}/{x}/{y}',
            'attribution': '© Land Use Data by Environmental Monitoring Agency'
        }
    }

def main():
    st.set_page_config(layout="wide")
    st.title("🌿 Eco-Law Tracker")
    st.subheader("Environmental Case Management & Monitoring System")
    
    # Add sidebar filters
    st.sidebar.title("Filters")
    cases = load_eco_cases()
    
    case_type_filter = st.sidebar.multiselect(
        "Case Type",
        options=cases['case_type'].unique(),
        default=cases['case_type'].unique()
    )
    
    status_filter = st.sidebar.multiselect(
        "Status",
        options=cases['status'].unique(),
        default=cases['status'].unique()
    )
    
    priority_filter = st.sidebar.multiselect(
        "Priority",
        options=cases['priority'].unique(),
        default=cases['priority'].unique()
    )
    
    # Filter the dataframe
    filtered_cases = cases[
        cases['case_type'].isin(case_type_filter) &
        cases['status'].isin(status_filter) &
        cases['priority'].isin(priority_filter)
    ]

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Case Map", "Case Analytics", "Case Management", "Law Awareness"])

    with tab1:
        st.subheader("Environmental Cases Geospatial View")
        
        # Load environmental zones and satellite imagery
        eco_zones = load_eco_zones()
        satellite_layers = load_satellite_imagery()
        
        # Create map controls
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.subheader("Map Layers")
            show_forest_cover = st.checkbox("Show Forest Cover", value=True)
            show_water_bodies = st.checkbox("Show Water Bodies")
            show_eco_zones = st.checkbox("Show Protected Areas", value=True)
            show_cases = st.checkbox("Show Cases", value=True)
        
        with col1:
            # Create a map centered on India
            m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
            
            # Add satellite imagery layers
            if show_forest_cover:
                folium.TileLayer(
                    tiles=satellite_layers['forest_cover']['url'],
                    name='Forest Cover',
                    attr=satellite_layers['forest_cover']['attribution'],
                    overlay=True
                ).add_to(m)
            
            if show_water_bodies:
                folium.TileLayer(
                    tiles=satellite_layers['water_bodies']['url'],
                    name='Water Bodies',
                    attr=satellite_layers['water_bodies']['attribution'],
                    overlay=True
                ).add_to(m)
            
            # Add environmental zones
            if show_eco_zones:
                for _, zone in eco_zones.iterrows():
                    folium.Circle(
                        location=[zone['lat'], zone['lon']],
                        radius=zone['area'] * 10,  # Scale area to visible size
                        popup=f"<b>{zone['zone_name']}</b><br>Type: {zone['zone_type']}<br>Area: {zone['area']} ha<br>Biodiversity Index: {zone['biodiversity_index']}<br>Threat Level: {zone['threat_level']}",
                        color='green',
                        fill=True,
                        fillOpacity=0.2
                    ).add_to(m)
            
            # Add case markers
            if show_cases:
                marker_cluster = MarkerCluster().add_to(m)
                for idx, case in filtered_cases.iterrows():
                    color = 'red' if case['priority'] == 'High' else 'orange' if case['priority'] == 'Medium' else 'green'
                    popup_html = f"""
                    <div style='width: 300px'>
                        <h4>{case['case_type']}</h4>
                        <b>Status:</b> {case['status']}<br>
                        <b>Priority:</b> {case['priority']}<br>
                        <b>Next Hearing:</b> {case['next_hearing'].strftime('%Y-%m-%d')}<br>
                        <b>Petitioner:</b> {case['petitioner']}<br>
                        <b>Respondent:</b> {case['respondent']}<br>
                        <b>Eco Zone:</b> {case['eco_zone_type']}<br>
                        <b>Impact Level:</b> {case['impact_level']}<br>
                        <b>Affected Area:</b> {case['affected_area']} ha<br>
                        <b>Species Affected:</b> {case['species_affected']}<br>
                        <b>Compliance Status:</b> {case['compliance_status']}
                    </div>
                    """
                    folium.Marker(
                        [case['lat'], case['lon']],
                        popup=popup_html,
                        icon=folium.Icon(color=color)
                    ).add_to(marker_cluster)
            
            # Add layer control
            folium.LayerControl().add_to(m)
            folium_static(m)

    with tab2:
        st.subheader("Case Analytics Dashboard")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_cases = len(filtered_cases)
            st.metric("Total Cases", total_cases)
        with col2:
            pending_cases = len(filtered_cases[filtered_cases['status'] == 'Pending'])
            st.metric("Pending Cases", pending_cases)
        with col3:
            high_priority = len(filtered_cases[filtered_cases['priority'] == 'High'])
            st.metric("High Priority Cases", high_priority)
        with col4:
            total_area = filtered_cases['affected_area'].sum()
            st.metric("Total Affected Area (ha)", f"{total_area:,}")
        
        # Environmental Impact Metrics
        st.subheader("Environmental Impact Analysis")
        impact_col1, impact_col2, impact_col3 = st.columns(3)
        
        with impact_col1:
            # Impact Level Distribution
            fig_impact = px.pie(filtered_cases, 
                               names='impact_level', 
                               title='Environmental Impact Distribution',
                               color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_impact, use_container_width=True)
        
        with impact_col2:
            # Compliance Status
            compliance_counts = filtered_cases['compliance_status'].value_counts().reset_index(name='count')
            fig_compliance = px.bar(compliance_counts,
                                   x='compliance_status', 
                                   y='count',
                                   title='Compliance Status Distribution',
                                   color='compliance_status',
                                   color_discrete_sequence=px.colors.sequential.Viridis)
            st.plotly_chart(fig_compliance, use_container_width=True)
        
        with impact_col3:
            # Affected Area by Eco Zone
            fig_area = px.bar(filtered_cases.groupby('eco_zone_type')['affected_area'].sum().reset_index(),
                             x='eco_zone_type',
                             y='affected_area',
                             title='Affected Area by Eco Zone Type',
                             labels={'affected_area': 'Area (hectares)'},
                             color='affected_area',
                             color_continuous_scale='Viridis')
            st.plotly_chart(fig_area, use_container_width=True)
        
        # Case Trends and Distribution
        st.subheader("Case Analysis")
        trend_col1, trend_col2 = st.columns(2)
        
        with trend_col1:
            # Case type distribution with impact level
            fig_type = px.sunburst(filtered_cases, 
                                  path=['case_type', 'impact_level'],
                                  title='Case Types by Impact Level')
            st.plotly_chart(fig_type, use_container_width=True)
        
        with trend_col2:
            # Timeline of cases with priority
            timeline_data = filtered_cases.groupby(['filing_date', 'priority']).size().reset_index(name='count')
            fig_timeline = px.line(timeline_data,
                                  x='filing_date',
                                  y='count',
                                  color='priority',
                                  title='Cases Filed Over Time by Priority',
                                  labels={'count': 'Number of Cases'},
                                  color_discrete_map={'High': 'red',
                                                     'Medium': 'orange',
                                                     'Low': 'green'})
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        with col2:
            # Timeline of cases
            timeline_data = filtered_cases.groupby('filing_date').size().reset_index(name='count')
            fig_timeline = px.line(timeline_data,
                                  x='filing_date', y='count', title='Cases Filed Over Time')
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Priority distribution
            # Priority distribution
            priority_data = filtered_cases['priority'].value_counts().reset_index()
            priority_data.columns = ['priority', 'count']
            fig_priority = px.bar(priority_data,
                                 x='priority', y='count', title='Case Priority Distribution',
                                 color='priority',
                                 color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'})
            st.plotly_chart(fig_priority, use_container_width=True)

    with tab3:
        st.subheader("Case Management")
        
        # Create tabs for different case management aspects
        case_tabs = st.tabs(["Case Overview", "Compliance Tracking", "Document Management", "Alerts & Notifications"])
        
        with case_tabs[0]:
            # Case details view
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Case List")
                # Enhanced case view with environmental metrics
                case_view = filtered_cases[[
                    'case_type', 'status', 'priority', 'next_hearing',
                    'eco_zone_type', 'impact_level', 'affected_area',
                    'compliance_status', 'clearance_status'
                ]]
                st.dataframe(case_view, use_container_width=True)
            
            with col2:
                st.subheader("Upcoming Hearings")
                upcoming_hearings = filtered_cases[filtered_cases['next_hearing'] >= datetime.now()]
                upcoming_hearings = upcoming_hearings.sort_values('next_hearing')
                
                for _, case in upcoming_hearings.head().iterrows():
                    with st.expander(f"{case['case_type']} - {case['next_hearing'].strftime('%Y-%m-%d')}"):
                        st.write(f"**Status:** {case['status']}")
                        st.write(f"**Priority:** {case['priority']}")
                        st.write(f"**Impact Level:** {case['impact_level']}")
                        st.write(f"**Compliance Status:** {case['compliance_status']}")
        
        with case_tabs[1]:
            st.subheader("Environmental Compliance Tracking")
            
            # Compliance metrics
            comp_col1, comp_col2, comp_col3 = st.columns(3)
            with comp_col1:
                compliance_rate = len(filtered_cases[filtered_cases['compliance_status'] == 'Compliant']) / len(filtered_cases) * 100
                st.metric("Overall Compliance Rate", f"{compliance_rate:.1f}%")
            
            with comp_col2:
                pending_clearances = len(filtered_cases[filtered_cases['clearance_status'] == 'Pending'])
                st.metric("Pending Environmental Clearances", pending_clearances)
            
            with comp_col3:
                critical_cases = len(filtered_cases[filtered_cases['impact_level'].isin(['Severe', 'Critical'])])
                st.metric("Critical Impact Cases", critical_cases)
            
            # Compliance status by case type
            fig_compliance = px.bar(
                filtered_cases.groupby(['case_type', 'compliance_status']).size().reset_index(name='count'),
                x='case_type',
                y='count',
                color='compliance_status',
                title='Compliance Status by Case Type',
                barmode='group'
            )
            st.plotly_chart(fig_compliance, use_container_width=True)
        
        with case_tabs[2]:
            st.subheader("Document Management")
            
            # Document upload section
            doc_col1, doc_col2 = st.columns(2)
            
            with doc_col1:
                st.subheader("Upload Documents")
                selected_case = st.selectbox("Select Case", filtered_cases['case_type'].unique())
                doc_type = st.selectbox(
                    "Document Type",
                    ["Environmental Impact Assessment", "Forest Clearance", "Wildlife Clearance",
                     "Compliance Report", "Site Inspection Report", "Expert Opinion"]
                )
                uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'jpg'])
                if uploaded_file is not None:
                    st.success("File uploaded successfully!")
            
            with doc_col2:
                st.subheader("Recent Documents")
                st.info("This section will display recently uploaded documents with preview functionality")
        
        with case_tabs[3]:
            st.subheader("Alerts & Notifications")
            
            # Alert settings
            alert_types = [
                "Upcoming Hearings",
                "Compliance Deadlines",
                "New Environmental Violations",
                "Clearance Status Updates",
                "Critical Impact Alerts"
            ]
            
            st.multiselect("Select Alert Types", alert_types, default=alert_types)
            
            # Notification preferences
            st.subheader("Notification Preferences")
            col1, col2 = st.columns(2)
            
            with col1:
                st.checkbox("Email Notifications", value=True)
                st.checkbox("SMS Alerts", value=False)
            
            with col2:
                st.checkbox("Daily Digest", value=True)
                st.checkbox("Instant Alerts for Critical Cases", value=True)
            
            # Recent alerts preview
            st.subheader("Recent Alerts")
            with st.expander("🔴 Critical: New violation reported in Tiger Reserve"):
                st.write("Unauthorized construction activity detected in protected area")
            with st.expander("🟡 Upcoming: Environmental clearance deadline"):
                st.write("Forest clearance for Hydropower project expires in 7 days")
            with st.expander("🟢 Update: Compliance report submitted"):
                st.write("Quarterly compliance report submitted for Wildlife sanctuary case")
    
    with tab4:
        st.subheader("Environmental Law Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Key Environmental Laws")
            with st.expander("Forest Conservation Act, 1980"):
                st.write("""
                The Forest Conservation Act, 1980 was enacted to help conserve the country's forests. 
                It strictly restricts and regulates the de-reservation of forests or use of forest land 
                for non-forest purposes without the prior approval of the Central Government.
                
                **Key Provisions:**
                - Section 2: Restrictions on de-reservation of forests
                - Section 3: Advisory Committee
                - Section 4: Penalties and procedures
                """)
            
            with st.expander("Wildlife Protection Act, 1972"):
                st.write("""
                The Wildlife Protection Act, 1972 provides for the protection of wild animals, birds and plants. 
                It has six schedules which give varying degrees of protection to different species.
                
                **Key Features:**
                - Prohibition of hunting
                - Protection of specified plants
                - Declaration of sanctuaries and national parks
                - Regulation of trade in wildlife products
                """)
        
        with col2:
            st.markdown("### Latest Updates")
            # Real-time environmental news feed
            st.info("📰 Latest Environmental Law Updates")
            
            # Simulated news updates
            updates = [
                {"date": "2024-03-15", "title": "New Guidelines for Environmental Impact Assessment"},
                {"date": "2024-03-10", "title": "Supreme Court Ruling on Forest Rights"},
                {"date": "2024-03-05", "title": "Amendments to Wildlife Protection Act"}
            ]
            
            for update in updates:
                st.markdown(f"**{update['date']}:** {update['title']}")
                
            st.markdown("### Useful Resources")
            st.markdown("- [Ministry of Environment, Forest and Climate Change](https://moef.gov.in/)")
            st.markdown("- [National Green Tribunal](https://greentribunal.gov.in/)")
            st.markdown("- [Environmental Law Database](https://www.elaw.org/)")

if __name__ == "__main__":
    main()