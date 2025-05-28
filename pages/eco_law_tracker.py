import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import MarkerCluster

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

@st.cache_data(show_spinner=False)
def load_eco_cases():
    # Enhanced sample data generation with optimized performance
    import numpy as np
    np.random.seed(42)
    num_cases = 1000  # Reduced sample size for faster loading
    
    # Pre-allocate arrays for better memory efficiency
    lats = np.random.uniform(8.0, 34.0, num_cases)
    lons = np.random.uniform(68.0, 92.0, num_cases)
    filing_dates = pd.date_range(start='2018-01-01', periods=num_cases, freq='D')
    next_hearings = filing_dates + pd.to_timedelta(np.random.randint(30, 365, num_cases), unit='D')
    affected_areas = np.random.randint(10, 50000, num_cases)

    # Use vectorized operations for better performance
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
            # Create a map with optimized settings
            m = folium.Map(location=[20.5937, 78.9629], 
                          zoom_start=5,
                          prefer_canvas=True,
                          disable_3d=True)
            
            # Add satellite imagery layers with lazy loading
            if show_forest_cover:
                with st.spinner('Loading forest cover layer...'):
                    folium.TileLayer(
                        tiles=satellite_layers['forest_cover']['url'],
                        name='Forest Cover',
                        attr=satellite_layers['forest_cover']['attribution'],
                        overlay=True,
                        control=True
                    ).add_to(m)
            
            if show_water_bodies:
                with st.spinner('Loading water bodies layer...'):
                    folium.TileLayer(
                        tiles=satellite_layers['water_bodies']['url'],
                        name='Water Bodies',
                        attr=satellite_layers['water_bodies']['attribution'],
                        overlay=True,
                        control=True,
                        maxNativeZoom=18,
                        maxZoom=18
                    ).add_to(m)
            
            # Add environmental zones with optimized rendering
            if show_eco_zones:
                with st.spinner('Loading protected areas...'):
                    for _, zone in eco_zones.iterrows():
                        folium.Circle(
                            location=[zone['lat'], zone['lon']],
                            radius=zone['area'] * 10,  # Scale area to visible size
                            popup=f"<b>{zone['zone_name']}</b><br>Type: {zone['zone_type']}<br>Area: {zone['area']} ha<br>Biodiversity Index: {zone['biodiversity_index']}<br>Threat Level: {zone['threat_level']}",
                            color='green',
                            fill=True,
                            fillOpacity=0.2,
                            weight=2,
                            opacity=0.8
                        ).add_to(m)
            
            # Add case markers with optimized clustering
            if show_cases:
                marker_cluster = MarkerCluster(maxClusterRadius=60, chunkedLoading=True).add_to(m)
                # Limit the number of markers displayed initially for performance
                max_initial_markers = 200
                show_all = st.checkbox("Show all cases on map (may be slow)", value=False)
                if show_all:
                    cases_to_show = filtered_cases
                else:
                    cases_to_show = filtered_cases.iloc[:max_initial_markers]
                    if len(filtered_cases) > max_initial_markers:
                        st.info(f"Showing first {max_initial_markers} cases. Enable 'Show all cases' to view all {len(filtered_cases)} cases.")
                for idx, case in cases_to_show.iterrows():
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
            st_folium(m, width=800)

    with tab2:
        st.subheader("Case Analytics Dashboard")
        
        # Summary metrics with optimized calculations
        with st.spinner('Loading summary metrics...'):
            # Use vectorized operations for better performance
            metrics = pd.DataFrame({
                'status': filtered_cases['status'],
                'priority': filtered_cases['priority'],
                'area': filtered_cases['affected_area']
            })
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_cases = len(metrics)
                st.metric("Total Cases", total_cases)
            with col2:
                pending_cases = (metrics['status'] == 'Pending').sum()
                st.metric("Pending Cases", pending_cases)
            with col3:
                high_priority = (metrics['priority'] == 'High').sum()
                st.metric("High Priority Cases", high_priority)
            with col4:
                total_area = metrics['area'].sum()
                st.metric("Total Affected Area (ha)", f"{total_area:,}")

        
        # Environmental Impact Metrics
        st.subheader("Environmental Impact Analysis")
        impact_col1, impact_col2, impact_col3 = st.columns(3)
        
        with impact_col1:
            # Impact Level Distribution
            fig_impact = px.pie(filtered_cases, 
                               names='impact_level', 
                               title='Impact Level Distribution',
                               color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_impact)
        
        with impact_col2:
            # Case Type Distribution
            fig_case_type = px.pie(filtered_cases, 
                                  names='case_type', 
                                  title='Case Type Distribution',
                                  color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_case_type)
        
        with impact_col3:
            # Compliance Status Distribution
            fig_compliance = px.pie(filtered_cases, 
                                   names='compliance_status', 
                                   title='Compliance Status Distribution',
                                   color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_compliance)
        
        # Temporal Analysis
        st.subheader("Temporal Analysis")
        temp_col1, temp_col2 = st.columns(2)
        
        with temp_col1:
            # Cases Over Time with optimized data processing
            with st.spinner('Loading timeline chart...'):
                # Pre-calculate the monthly aggregation
                cases_over_time = filtered_cases.groupby(
                    pd.Grouper(key='filing_date', freq='M')
                ).size().reset_index()
                cases_over_time.columns = ['Month', 'Count']
                
                fig_timeline = px.line(
                    cases_over_time,
                    x='Month',
                    y='Count',
                    title='Cases Filed Over Time',
                    render_mode='svg'  # Use SVG for better performance
                )
                fig_timeline.update_layout(uirevision=True)  # Preserve UI state
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        with temp_col2:
            # Status Transition
            status_time = filtered_cases.groupby(['filing_date', 'status']).size().reset_index()
            status_time.columns = ['Date', 'Status', 'Count']
            
            fig_status = px.area(status_time, 
                                x='Date', 
                                y='Count', 
                                color='Status',
                                title='Case Status Over Time')
            st.plotly_chart(fig_status)

    with tab3:
        st.subheader("Case Management")
        
        # Case Details Table with optimized search
        st.write("### Case Details")
        
        # Add search functionality with loading indicator
        search_term = st.text_input("Search Cases", "")
        
        with st.spinner('Searching cases...'):
            if search_term:
                # Use vectorized operations for faster search
                mask = (
                    filtered_cases['case_type'].str.contains(search_term, case=False, na=False) |
                    filtered_cases['location'].str.contains(search_term, case=False, na=False) |
                    filtered_cases['petitioner'].str.contains(search_term, case=False, na=False) |
                    filtered_cases['respondent'].str.contains(search_term, case=False, na=False)
                )
                search_results = filtered_cases[mask]
            else:
                search_results = filtered_cases
        
        # Display paginated results with optimized rendering
        with st.spinner('Loading results...'):
            page_size = 20  # Increased page size for better performance
            total_pages = max(1, len(search_results) // page_size + (1 if len(search_results) % page_size > 0 else 0))
            current_page = st.number_input("Page", min_value=1, max_value=total_pages, value=1) - 1
            
            start_idx = current_page * page_size
            end_idx = start_idx + page_size
            
            # Display selected columns with optimized data types
            display_cols = ['case_type', 'location', 'status', 'priority', 'filing_date', 'next_hearing', 'impact_level']
            df_display = search_results[display_cols].iloc[start_idx:end_idx].copy()
            
            # Convert date columns to string for faster rendering
            df_display['filing_date'] = df_display['filing_date'].dt.strftime('%Y-%m-%d')
            df_display['next_hearing'] = df_display['next_hearing'].dt.strftime('%Y-%m-%d')
            
            st.dataframe(df_display, use_container_width=True)
        
        # Case Statistics
        st.write("### Case Statistics")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            # Average Processing Time
            avg_processing_time = (filtered_cases['next_hearing'] - filtered_cases['filing_date']).mean().days
            st.metric("Avg. Processing Time (days)", f"{avg_processing_time:.1f}")
        
        with stats_col2:
            # Resolution Rate
            resolution_rate = len(filtered_cases[filtered_cases['status'] == 'Resolved']) / len(filtered_cases) * 100
            st.metric("Resolution Rate (%)", f"{resolution_rate:.1f}%")
        
        with stats_col3:
            # Compliance Rate
            compliance_rate = len(filtered_cases[filtered_cases['compliance_status'] == 'Compliant']) / len(filtered_cases) * 100
            st.metric("Compliance Rate (%)", f"{compliance_rate:.1f}%")

    with tab4:
        st.subheader("Environmental Law Awareness")
        
        # Educational Resources
        st.write("### Key Environmental Laws and Regulations")
        
        # Create expandable sections for different laws
        with st.expander("Wildlife Protection Act, 1972"):
            st.write("""
            The Wildlife Protection Act, 1972 provides for the protection of wild animals, birds and plants. Key provisions include:
            - Prohibition of hunting of wild animals
            - Protection of specified plants
            - Declaration and management of protected areas
            - Regulation of trade in wildlife and its products
            - Penalties for violation of the Act
            """)
        
        with st.expander("Forest Conservation Act, 1980"):
            st.write("""
            The Forest Conservation Act, 1980 was enacted to help conserve the country's forests. Main features include:
            - Restriction on de-reservation of forests
            - Regulation of use of forest land for non-forest purposes
            - Requirement of prior approval for forest clearance
            - Compensatory afforestation requirements
            """)
        
        with st.expander("Environmental Protection Act, 1986"):
            st.write("""
            The Environmental Protection Act, 1986 is an umbrella legislation that provides for:
            - Protection and improvement of environmental quality
            - Control of environmental pollution
            - Setting standards for emissions and discharges
            - Environmental impact assessment requirements
            - Powers to take measures to protect and improve environment
            """)
        
        # Add interactive quiz section
        st.write("### Test Your Knowledge")
        
        # Sample quiz question
        quiz_question = st.radio(
            "Which act provides for the protection of wild animals, birds and plants?",
            ["Forest Conservation Act, 1980", "Wildlife Protection Act, 1972", "Environmental Protection Act, 1986", "Biological Diversity Act, 2002"]
        )
        
        if quiz_question:
            if quiz_question == "Wildlife Protection Act, 1972":
                st.success("Correct! The Wildlife Protection Act, 1972 is the primary legislation for protection of wildlife in India.")
            else:
                st.error("Incorrect. The Wildlife Protection Act, 1972 is the correct answer.")
        
        # Add resources section
        st.write("### Additional Resources")
        st.write("""
        - National Green Tribunal (NGT) Website
        - Ministry of Environment, Forest and Climate Change
        - State Pollution Control Board Guidelines
        - Environmental Law Research Tools
        - Case Law Databases
        """)

if __name__ == "__main__":
    main()