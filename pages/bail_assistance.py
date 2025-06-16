import streamlit as st
import pandas as pd
from argument_generator import argument_generator
from legal_data import (
    get_offense_details, get_bail_information, bail_guidelines,
    ipc_sections, it_act_sections, mv_act_sections
)

st.set_page_config(
    page_title="Bail Assistance - Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("Bail Assistance Tool")
st.markdown("### Understand bail provisions and generate bail arguments")

# Sidebar for navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Back to Home"):
    st.switch_page("app.py")

if st.sidebar.button("Lawyer Assistant"):
    st.switch_page("pages/lawyer_assistant.py")

if st.sidebar.button("Legal Codes Reference"):
    st.switch_page("pages/legal_codes.py")

# Create tabs for different bail-related functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Bail Eligibility Check", "Bail Arguments Generator", "Bail Application Guide", "Himachal Pradesh Cases"])

# Add Himachal Pradesh specific categories in tab4
with tab4:
    st.markdown("## Himachal Pradesh Specific Cases")
    st.markdown("""
    Check bail eligibility and get specialized bail assistance based on Himachal Pradesh laws and procedures.
    """)
    
    # Main category selection
    hp_categories = {
        "Environmental & Forest Cases": [
            "Wildlife Protection Act Violations",
            "Forest Conservation Act Cases",
            "HP Forest Act Offenses",
            "Environmental Protection Cases"
        ],
        "Tribal Rights Cases": [
            "Forest Rights Act Violations",
            "Traditional Rights Disputes",
            "Community Resource Conflicts",
            "PESA Act Cases"
        ],
        "Local Criminal Cases": [
            "IPC Sections (HP Context)",
            "Local Ordinance Violations",
            "Special Acts Enforcement",
            "Prevention of Social Offences"
        ],
        "Special Categories": [
            "Tourism Related Offenses",
            "Hydropower Project Violations",
            "Land Use Violations",
            "Heritage Protection Cases"
        ]
    }
    
    selected_category = st.selectbox("Select Case Category", options=list(hp_categories.keys()), key="hp_main_category_select")
    
    # Subcategory selection based on main category
    if selected_category:
        selected_subcategory = st.selectbox(
            "Select Subcategory",
            options=hp_categories[selected_category],
            key="hp_sub_category_select"
        )
        
        # Display relevant information based on selection
        if selected_subcategory:
            st.markdown(f"### Information for {selected_subcategory}")
            
            # Environmental & Forest Cases
            if selected_category == "Environmental & Forest Cases":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Minor environmental violation",
                    "Moderate environmental damage",
                    "Serious ecological harm",
                    "Protected species related offense",
                    "Forest encroachment",
                    "Illegal mining/quarrying"
                ], key="hp_env_offense_type_select_2.2")
                
                previous_record = st.checkbox("Any previous environmental offenses?",key="env_offense_check_2.0")
                local_resident = st.checkbox("Is the accused a local resident?",key="local_res_env_2.0")
                community_support = st.checkbox("Does the accused have community support?",key="comm_supp_env_2.0")
                restoration_plan = st.checkbox("Is there a restoration/remediation plan?", key="restoration_plan_env_2.0")
                
                if st.button("Check Bail Eligibility"):
                    eligibility_score = 0
                    if offense_type == "Minor environmental violation":
                        eligibility_score += 3
                    elif offense_type == "Moderate environmental damage":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if not previous_record:
                        eligibility_score += 2
                    if local_resident:
                        eligibility_score += 2
                    if community_support:
                        eligibility_score += 1
                    if restoration_plan:
                        eligibility_score += 2
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 7:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Case appears to be bailable
                        - Strong community ties and support
                        - Positive factors outweigh concerns
                        """)
                    elif eligibility_score >= 5:
                        st.warning("Moderate chance of bail - subject to court's discretion")
                        st.markdown("""
                        **Key Considerations:**
                        - Court may impose conditions
                        - Regular reporting may be required
                        - Environmental restoration guarantees needed
                        """)
                    else:
                        st.error("Lower probability of bail - significant challenges")
                        st.markdown("""
                        **Critical Factors:**
                        - Serious nature of offense
                        - Previous record concerns
                        - Need for stronger remediation plan
                        """)
                
                st.markdown("""
                #### Relevant Acts and Guidelines
                - Wildlife Protection Act, 1972
                - Forest Conservation Act, 1980
                - HP Forest Act
                - Environmental Protection Act
                - NGT Guidelines for Environmental Cases
                """)
            
            # Local Criminal Cases
            elif selected_category == "Local Criminal Cases":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Minor local ordinance violation",
                    "Social offense case",
                    "Local law violation",
                    "Special act violation"
                ], key="hp_local_offense_type_select")
                
                local_resident = st.checkbox("Is the accused a local resident?",key="local_res_2")
                first_offense = st.checkbox("Is this a first offense?")
                community_standing = st.checkbox("Does the accused have good community standing?")
                cooperation = st.checkbox("Has the accused cooperated with authorities?")
                
                if st.button("Check Bail Eligibility"):
                    eligibility_score = 0
                    if offense_type == "Minor local ordinance violation":
                        eligibility_score += 3
                    elif offense_type == "Social offense case":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if local_resident:
                        eligibility_score += 2
                    if first_offense:
                        eligibility_score += 2
                    if community_standing:
                        eligibility_score += 2
                    if cooperation:
                        eligibility_score += 1
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 7:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Minor nature of offense
                        - Strong local ties
                        - Good community standing
                        """)
                    elif eligibility_score >= 5:
                        st.warning("Moderate chance of bail - subject to conditions")
                        st.markdown("""
                        **Key Considerations:**
                        - Regular reporting to local police
                        - Restrictions on movement
                        - Community service requirements
                        """)
                    else:
                        st.error("Lower probability of bail - requires additional support")
                        st.markdown("""
                        **Critical Factors:**
                        - Nature of local offense
                        - Need for community guarantors
                        - Additional conditions may apply
                        """)
                
                st.markdown("""
                #### Relevant Local Laws and Guidelines
                - HP Police Act
                - Local Municipal Ordinances
                - Social Justice Acts
                - Special Local Enactments
                """)
            
            # Special Categories
            elif selected_category == "Special Categories":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Tourism regulation violation",
                    "Heritage site offense",
                    "Hydropower project violation",
                    "Land use violation"
                ], key="special_offense_type_select")
                
                business_owner = st.checkbox("Is the accused a registered business owner?")
                first_violation = st.checkbox("Is this a first violation?")
                remediation_commitment = st.checkbox("Is there a commitment to remedy the violation?")
                local_employment = st.checkbox("Does the business provide local employment?")
                
                if st.button("Check Bail Eligibility"):
                    eligibility_score = 0
                    if offense_type == "Tourism regulation violation":
                        eligibility_score += 3
                    elif offense_type == "Land use violation":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if business_owner:
                        eligibility_score += 2
                    if first_violation:
                        eligibility_score += 2
                    if remediation_commitment:
                        eligibility_score += 2
                    if local_employment:
                        eligibility_score += 1
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 7:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Business establishment in region
                        - Economic contribution to area
                        - Commitment to compliance
                        """)
                    elif eligibility_score >= 5:
                        st.warning("Moderate chance of bail - subject to conditions")
                        st.markdown("""
                        **Key Considerations:**
                        - Business operation restrictions
                        - Regular compliance reporting
                        - Financial guarantees required
                        """)
                    else:
                        st.error("Lower probability of bail - significant compliance issues")
                        st.markdown("""
                        **Critical Factors:**
                        - Serious violation nature
                        - Impact on local heritage/resources
                        - Need for substantial guarantees
                        """)
                
                st.markdown("""
                #### Relevant Regulations and Guidelines
                - HP Tourism Development Act
                - Heritage Protection Laws
                - Land Use Regulations
                - Industrial Development Guidelines
                """)
            
            # Environmental & Forest Cases
            if selected_category == "Environmental & Forest Cases":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Minor environmental violation",
                    "Moderate environmental damage",
                    "Serious ecological harm",
                    "Protected species related offense",
                    "Forest encroachment",
                    "Illegal mining/quarrying"
                ], key="hp_env_offense_type_select_2.3")
                
                previous_record = st.checkbox("Any previous environmental offenses?",key="env_offense_check_2")
                local_resident = st.checkbox("Is the accused a local resident?",key="local_res_env_2")
                community_support = st.checkbox("Does the accused have community support?",key="comm_supp_env_2")
                restoration_plan = st.checkbox("Is there a restoration/remediation plan?", key="restoration_plan_env_2")
                
                if st.button("Check Bail Eligibility",key=1):
                    eligibility_score = 0
                    if offense_type == "Minor environmental violation":
                        eligibility_score += 3
                    elif offense_type == "Moderate environmental damage":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if not previous_record:
                        eligibility_score += 2
                    if local_resident:
                        eligibility_score += 2
                    if community_support:
                        eligibility_score += 1
                    if restoration_plan:
                        eligibility_score += 2
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 7:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Case appears to be bailable
                        - Strong community ties and support
                        - Positive factors outweigh concerns
                        """)
                    elif eligibility_score >= 5:
                        st.warning("Moderate chance of bail - subject to court's discretion")
                        st.markdown("""
                        **Key Considerations:**
                        - Court may impose conditions
                        - Regular reporting may be required
                        - Environmental restoration guarantees needed
                        """)
                    else:
                        st.error("Lower probability of bail - significant challenges")
                        st.markdown("""
                        **Critical Factors:**
                        - Serious nature of offense
                        - Previous record concerns
                        - Need for stronger remediation plan
                        """)
                
                st.markdown("""
                #### Relevant Acts and Guidelines
                - Wildlife Protection Act, 1972
                - Forest Conservation Act, 1980
                - HP Forest Act
                - Environmental Protection Act
                - NGT Guidelines for Environmental Cases
                """)
            
            # Tribal Rights Cases
            elif selected_category == "Tribal Rights Cases":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Traditional rights dispute",
                    "Community resource conflict",
                    "PESA Act violation",
                    "Forest rights violation"
                ], key="tribal_offense_type_select")
                
                tribal_resident = st.checkbox("Is the accused a tribal resident?")
                community_validation = st.checkbox("Is there community validation of traditional rights claim?")
                peaceful_resolution = st.checkbox("Is there willingness for peaceful resolution?")
                first_offense = st.checkbox("Is this a first offense?")
                
                if st.button("Check Bail Eligibility"):
                    eligibility_score = 0
                    if offense_type == "Traditional rights dispute":
                        eligibility_score += 3
                    elif offense_type == "Community resource conflict":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if tribal_resident:
                        eligibility_score += 3
                    if community_validation:
                        eligibility_score += 2
                    if peaceful_resolution:
                        eligibility_score += 2
                    if first_offense:
                        eligibility_score += 2
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 8:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Strong tribal community connection
                        - Traditional rights consideration
                        - Peaceful resolution approach
                        """)
                    elif eligibility_score >= 6:
                        st.warning("Moderate chance of bail - subject to conditions")
                        st.markdown("""
                        **Key Considerations:**
                        - Regular reporting to tribal council
                        - Maintain peace in community
                        - Respect traditional dispute resolution
                        """)
                    else:
                        st.error("Lower probability of bail - requires additional support")
                        st.markdown("""
                        **Critical Factors:**
                        - Need for stronger community backing
                        - Serious nature of tribal dispute
                        - Risk to community harmony
                        """)
                
                st.markdown("""
                #### Relevant Acts and Guidelines
                - PESA Act
                - Forest Rights Act
                - HP Tribal Areas Regulation
                - Traditional Rights Protection Guidelines
                """)
            
            # Environmental & Forest Cases
            if selected_category == "Environmental & Forest Cases":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Minor environmental violation",
                    "Moderate environmental damage",
                    "Serious ecological harm",
                    "Protected species related offense",
                    "Forest encroachment",
                    "Illegal mining/quarrying"
                ], key="hp_env_offense_type_select_2")
                
                previous_record = st.checkbox("Any previous environmental offenses?",key="env_offense_1")
                local_resident = st.checkbox("Is the accused a local resident?")
                community_support = st.checkbox("Does the accused have community support?")
                restoration_plan = st.checkbox("Is there a restoration/remediation plan?")
                
                if st.button("Check Bail Eligibility",key="check_bail_1"):
                    eligibility_score = 0
                    if offense_type == "Minor environmental violation":
                        eligibility_score += 3
                    elif offense_type == "Moderate environmental damage":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if not previous_record:
                        eligibility_score += 2
                    if local_resident:
                        eligibility_score += 2
                    if community_support:
                        eligibility_score += 1
                    if restoration_plan:
                        eligibility_score += 2
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 7:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Case appears to be bailable
                        - Strong community ties and support
                        - Positive factors outweigh concerns
                        """)
                    elif eligibility_score >= 5:
                        st.warning("Moderate chance of bail - subject to court's discretion")
                        st.markdown("""
                        **Key Considerations:**
                        - Court may impose conditions
                        - Regular reporting may be required
                        - Environmental restoration guarantees needed
                        """)
                    else:
                        st.error("Lower probability of bail - significant challenges")
                        st.markdown("""
                        **Critical Factors:**
                        - Serious nature of offense
                        - Previous record concerns
                        - Need for stronger remediation plan
                        """)
                
                st.markdown("""
                #### Relevant Acts and Guidelines
                - Wildlife Protection Act, 1972
                - Forest Conservation Act, 1980
                - HP Forest Act
                - Environmental Protection Act
                - NGT Guidelines for Environmental Cases
                """)
            
            # Local Criminal Cases
            elif selected_category == "Local Criminal Cases":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Minor local ordinance violation",
                    "Social offense case",
                    "Local law violation",
                    "Special act violation"
                ], key="local_offense_type_select_1")
                
                local_resident = st.checkbox("Is the accused a local resident?",key="local_res_5")
                first_offense = st.checkbox("Is this a first offense?")
                community_standing = st.checkbox("Does the accused have good community standing?")
                cooperation = st.checkbox("Has the accused cooperated with authorities?")
                
                if st.button("Check Bail Eligibility"):
                    eligibility_score = 0
                    if offense_type == "Minor local ordinance violation":
                        eligibility_score += 3
                    elif offense_type == "Social offense case":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if local_resident:
                        eligibility_score += 2
                    if first_offense:
                        eligibility_score += 2
                    if community_standing:
                        eligibility_score += 2
                    if cooperation:
                        eligibility_score += 1
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 7:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Minor nature of offense
                        - Strong local ties
                        - Good community standing
                        """)
                    elif eligibility_score >= 5:
                        st.warning("Moderate chance of bail - subject to conditions")
                        st.markdown("""
                        **Key Considerations:**
                        - Regular reporting to local police
                        - Restrictions on movement
                        - Community service requirements
                        """)
                    else:
                        st.error("Lower probability of bail - requires additional support")
                        st.markdown("""
                        **Critical Factors:**
                        - Nature of local offense
                        - Need for community guarantors
                        - Additional conditions may apply
                        """)
                
                st.markdown("""
                #### Relevant Local Laws and Guidelines
                - HP Police Act
                - Local Municipal Ordinances
                - Social Justice Acts
                - Special Local Enactments
                """)
            
            # Special Categories
            elif selected_category == "Special Categories":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Tourism regulation violation",
                    "Heritage site offense",
                    "Hydropower project violation",
                    "Land use violation"
                ], key="special_offense_type_select")
                
                business_owner = st.checkbox("Is the accused a registered business owner?")
                first_violation = st.checkbox("Is this a first violation?")
                remediation_commitment = st.checkbox("Is there a commitment to remedy the violation?")
                local_employment = st.checkbox("Does the business provide local employment?")
                
                if st.button("Check Bail Eligibility"):
                    eligibility_score = 0
                    if offense_type == "Tourism regulation violation":
                        eligibility_score += 3
                    elif offense_type == "Land use violation":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if business_owner:
                        eligibility_score += 2
                    if first_violation:
                        eligibility_score += 2
                    if remediation_commitment:
                        eligibility_score += 2
                    if local_employment:
                        eligibility_score += 1
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 7:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Business establishment in region
                        - Economic contribution to area
                        - Commitment to compliance
                        """)
                    elif eligibility_score >= 5:
                        st.warning("Moderate chance of bail - subject to conditions")
                        st.markdown("""
                        **Key Considerations:**
                        - Business operation restrictions
                        - Regular compliance reporting
                        - Financial guarantees required
                        """)
                    else:
                        st.error("Lower probability of bail - significant compliance issues")
                        st.markdown("""
                        **Critical Factors:**
                        - Serious violation nature
                        - Impact on local heritage/resources
                        - Need for substantial guarantees
                        """)
                
                st.markdown("""
                #### Relevant Regulations and Guidelines
                - HP Tourism Development Act
                - Heritage Protection Laws
                - Land Use Regulations
                - Industrial Development Guidelines
                """)
            
            # Environmental & Forest Cases
            if selected_category == "Environmental & Forest Cases":
                st.markdown("#### Bail Eligibility Check")
                offense_type = st.selectbox("Select Offense Type", [
                    "Minor environmental violation",
                    "Moderate environmental damage",
                    "Serious ecological harm",
                    "Protected species related offense",
                    "Forest encroachment",
                    "Illegal mining/quarrying"
                ], key="hp_env_offense_type_select_2.1")
                
                previous_record = st.checkbox("Any previous environmental offenses?",key="env_offense_4")
                local_resident = st.checkbox("Is the accused a local resident?",key="local_res_4")
                community_support = st.checkbox("Does the accused have community support?",key="comm_supp_3")
                restoration_plan = st.checkbox("Is there a restoration/remediation plan?",key="restoration_1")
                
                if st.button("Check Bail Eligibility",key="bail_elg_3"):
                    eligibility_score = 0
                    if offense_type == "Minor environmental violation":
                        eligibility_score += 3
                    elif offense_type == "Moderate environmental damage":
                        eligibility_score += 2
                    else:
                        eligibility_score += 1
                    
                    if not previous_record:
                        eligibility_score += 2
                    if local_resident:
                        eligibility_score += 2
                    if community_support:
                        eligibility_score += 1
                    if restoration_plan:
                        eligibility_score += 2
                    
                    st.markdown("#### Bail Eligibility Assessment")
                    if eligibility_score >= 7:
                        st.success("High likelihood of bail being granted")
                        st.markdown("""
                        **Favorable Factors:**
                        - Case appears to be bailable
                        - Strong community ties and support
                        - Positive factors outweigh concerns
                        """)
                    elif eligibility_score >= 5:
                        st.warning("Moderate chance of bail - subject to court's discretion")
                        st.markdown("""
                        **Key Considerations:**
                        - Court may impose conditions
                        - Regular reporting may be required
                        - Environmental restoration guarantees needed
                        """)
                    else:
                        st.error("Lower probability of bail - significant challenges")
                        st.markdown("""
                        **Critical Factors:**
                        - Serious nature of offense
                        - Previous record concerns
                        - Need for stronger remediation plan
                        """)
                
                st.markdown("""
                #### Relevant Acts and Guidelines
                - Wildlife Protection Act, 1972
                - Forest Conservation Act, 1980
                - HP Forest Act
                - Environmental Protection Act
                - NGT Guidelines for Environmental Cases
                """)
                
            elif "IPC Sections" in selected_subcategory:
                st.markdown("""
                #### Common IPC Sections in Himachal Pradesh
                - Section 379: Theft
                - Section 447: Criminal Trespass
                - Section 323: Voluntarily causing hurt
                
                #### Local Procedures
                - File bail application in concerned court
                - Provide local surety
                - Comply with reporting requirements
                """)
            
            # Civil Cases specific information
            elif selected_category == "Civil Cases":
                if "Land Disputes" in selected_subcategory:
                    st.markdown("""
                    #### Key Considerations
                    - Title documents and revenue records
                    - Local land laws and customs
                    - Possession status
                    - Previous litigation history
                    
                    #### Required Documents
                    - Property papers
                    - Revenue records (Jamabandi)
                    - Survey documents
                    - Previous court orders if any
                    """)
            
            # Revenue Cases specific information
            elif selected_category == "Revenue Cases":
                if "Mutation" in selected_subcategory:
                    st.markdown("""
                    #### Important Points
                    - Verification of revenue records
                    - Status of mutation proceedings
                    - Objections by interested parties
                    - Appeal procedures
                    
                    #### Required Documents
                    - Latest Jamabandi
                    - Inheritance documents
                    - Sale deed/gift deed if applicable
                    - Identity proof
                    """)
            
            # Special Local Categories information
            elif selected_category == "Special Local Categories":
                if "Environmental Litigation" in selected_subcategory:
                    st.markdown("""
                    #### Key Acts and Regulations
                    - Environment Protection Act
                    - Forest Conservation Act
                    - Himachal Pradesh Ground Water Act
                    - NGT Guidelines
                    
                    #### Important Considerations
                    - Environmental impact assessment
                    - Compliance with local regulations
                    - Public interest concerns
                    - Expert committee reports
                    """)
                elif "Tribal Rights" in selected_subcategory:
                    st.markdown("""
                    #### Relevant Laws
                    - Forest Rights Act
                    - PESA Act provisions
                    - Local tribal customs
                    - Constitutional safeguards
                    
                    #### Key Documents
                    - Tribal certificates
                    - Community rights documentation
                    - Traditional rights evidence
                    - Gram Sabha resolutions
                    """)


with tab1:
    st.markdown("## Check Bail Eligibility")
    st.markdown("""
    Determine whether an offense is bailable or non-bailable, and understand the 
    general eligibility criteria for bail based on the specific legal section.
    """)
    
    # Select legal act
    act_options = {"Indian Penal Code (IPC)": "IPC", 
                   "Information Technology Act": "IT Act", 
                   "Motor Vehicles Act": "MV Act"}
    selected_act = st.selectbox("Select Legal Act", options=list(act_options.keys()))
    act_code = act_options[selected_act]
            
    # Show relevant sections based on selected act
    if act_code == "IPC":
        section_options = {f"Section {k}: {v}": k for k, v in ipc_sections.items()}
    elif act_code == "IT Act":
        section_options = {f"Section {k}: {v}": k for k, v in it_act_sections.items()}
    else:  # MV Act
        section_options = {f"Section {k}: {v}": k for k, v in mv_act_sections.items()}
    
    selected_section_display = st.selectbox("Select Section", options=list(section_options.keys()))
    selected_section = section_options[selected_section_display]
    
    # Additional details
    col1, col2 = st.columns(2)
    
    with col1:
        first_time_offender = st.radio("First Time Offender?", options=["Yes", "No"])
        custody_duration = st.slider("Time in Custody (days)", min_value=0, max_value=365, value=30)
    
    with col2:
        accused_age = st.number_input("Age of Accused", min_value=10, max_value=100, value=30)
        health_issues = st.radio("Medical/Health Issues?", options=["None", "Minor", "Serious"])
    
    if st.button("Check Bail Eligibility", use_container_width=True):
        with st.spinner("Analyzing bail eligibility..."):
            # Get offense details
            offense_details = get_offense_details(selected_section, act_code)
            
            if not offense_details:
                st.error(f"Could not retrieve information for {act_code} Section {selected_section}.")
            else:
                # Get bail information
                bail_info = offense_details.get("bail_info", {})
                
                # Determine if bailable
                is_bailable = "bailable" in str(bail_info).lower()
                
                # Display eligibility information
                st.markdown(f"### Bail Eligibility for {act_code} Section {selected_section}")
                
                if is_bailable:
                    st.success("#### This is a BAILABLE Offense")
                    st.markdown("""
                    In bailable offenses, bail is a matter of right and not discretion. 
                    The accused has the right to be released on bail upon furnishing 
                    sureties or executing a personal bond.
                    """)
                    
                    # Display procedure
                    st.markdown("#### Bail Procedure")
                    for step in bail_info.get("procedure", []):
                        st.markdown(f"- {step}")
                    
                else:
                    st.error("#### This is a NON-BAILABLE Offense")
                    st.markdown("""
                    In non-bailable offenses, bail is a matter of court's discretion and not a right.
                    The court considers various factors before granting or denying bail.
                    """)
                    
                    # Display procedure
                    st.markdown("#### Bail Consideration Factors")
                    for step in bail_info.get("procedure", []):
                        st.markdown(f"- {step}")
                
                # Analyze additional factors
                st.markdown("### Additional Factors Affecting Bail Eligibility")
                
                factors = []
                if first_time_offender == "Yes":
                    factors.append(("First time offender status may work in favor of bail application", "positive"))
                else:
                    factors.append(("Previous criminal history may negatively impact bail chances", "negative"))
                
                if custody_duration > 60:
                    factors.append(("Extended custody period may strengthen bail application under Section 436A CrPC", "positive"))
                
                if accused_age < 18:
                    factors.append(("Juvenile status provides special protections under Juvenile Justice Act", "positive"))
                elif accused_age > 65:
                    factors.append(("Advanced age may be considered a humanitarian ground for bail", "positive"))
                
                if health_issues == "Serious":
                    factors.append(("Serious medical condition may constitute humanitarian ground for bail", "positive"))
                elif health_issues == "Minor":
                    factors.append(("Minor health issues should be documented but may not significantly impact bail decision", "neutral"))
                
                # Display factors
                for factor, impact in factors:
                    if impact == "positive":
                        st.markdown(f"✅ {factor}")
                    elif impact == "negative":
                        st.markdown(f"❌ {factor}")
                    else:
                        st.markdown(f"ℹ️ {factor}")
                
                # Display bail application routes
                st.markdown("### Bail Application Routes")
                
                if is_bailable:
                    st.markdown("""
                    1. **Police Station**: For bailable offenses, bail can be granted by the officer in charge
                    2. **Magistrate Court**: If police refuses bail or accused is produced before court
                    3. **Sessions Court**: Appeal if bail is denied by Magistrate
                    """)
                else:
                    st.markdown("""
                    1. **Magistrate Court**: Initial bail application for less serious non-bailable offenses
                    2. **Sessions Court**: For serious offenses or if denied by Magistrate
                    3. **High Court**: Under Section 439 CrPC if denied by lower courts
                    4. **Supreme Court**: In exceptional cases under Article 136
                    """)
                
                # Special provisions
                st.markdown("### Special Provisions")
                
                if not is_bailable:
                    st.markdown("""
                    - **Section 436A CrPC**: Eligible for bail if detained for half of the maximum punishment period
                    - **Special consideration** for women, senior citizens, and individuals with medical conditions
                    - **Anticipatory Bail** under Section 438 CrPC before arrest
                    """)

with tab2:
    st.markdown("## Bail Arguments Generator")
    st.markdown("""
    Generate persuasive legal arguments for bail applications based on the specific 
    section, case details, and relevant legal provisions.
    """)
    
    # Input form for argument generation
    col1, col2 = st.columns(2)
    
    with col1:
        # Select legal act
        arg_act_options = {"Indian Penal Code (IPC)": "IPC", 
                         "Information Technology Act": "IT Act", 
                         "Motor Vehicles Act": "MV Act"}
        arg_selected_act = st.selectbox("Select Legal Act", options=list(arg_act_options.keys()), key="arg_act")
        arg_act_code = arg_act_options[arg_selected_act]
        
        # Show relevant sections based on selected act
        if arg_act_code == "IPC":
            arg_section_options = {f"Section {k}: {v}": k for k, v in ipc_sections.items()}
        elif arg_act_code == "IT Act":
            arg_section_options = {f"Section {k}: {v}": k for k, v in it_act_sections.items()}
        else:  # MV Act
            arg_section_options = {f"Section {k}: {v}": k for k, v in mv_act_sections.items()}
        
        arg_selected_section_display = st.selectbox("Select Section", options=list(arg_section_options.keys()), key="arg_section")
        arg_selected_section = arg_section_options[arg_selected_section_display]
    
    with col2:
        # Case description
        arg_case_description = st.text_area("Case Description", 
                               placeholder="Describe the case facts and circumstances relevant to bail...",
                               height=100,
                               key="arg_desc")
        
        # Argument position
        arg_position_options = {
            "Arguments FOR Granting Bail": True,
            "Arguments AGAINST Granting Bail": False
        }
        arg_selected_position = st.radio("Generate Arguments", options=list(arg_position_options.keys()))
        favor_bail = arg_position_options[arg_selected_position]
        
        # Number of arguments
        arg_num = st.slider("Number of Arguments", min_value=3, max_value=10, value=5, key="arg_num")
    
    if st.button("Generate Bail Arguments", use_container_width=True):
        if not arg_case_description:
            st.warning("Please provide a case description to generate bail arguments.")
        else:
            with st.spinner("Generating bail arguments..."):
                # Generate bail arguments
                bail_arguments_result = argument_generator.generate_bail_arguments(
                    arg_selected_section, arg_act_code, arg_case_description, favor_bail, arg_num
                )
                
                if "error" in bail_arguments_result:
                    st.error(bail_arguments_result["error"])
                else:
                    # Display bail status
                    is_bailable = bail_arguments_result.get("is_bailable", False)
                    offense_details = bail_arguments_result.get("offense_details", {})
                    
                    if is_bailable:
                        st.success(f"Section {arg_selected_section} of {arg_act_code} is a BAILABLE offense")
                    else:
                        st.error(f"Section {arg_selected_section} of {arg_act_code} is a NON-BAILABLE offense")
                    
                    # Display arguments
                    st.markdown(f"### {arg_selected_position}")
                    arguments = bail_arguments_result.get("bail_arguments", [])
                    
                    for i, argument in enumerate(arguments, 1):
                        st.markdown(f"**Argument {i}:** {argument}")
                    
                    # Additional guidance
                    st.markdown("### Application Guidelines")
                    
                    if favor_bail:
                        st.markdown("""
                        When submitting these arguments in your bail application:
                        
                        1. **Structure your application** with these points in order of strength
                        2. **Support with precedents** cited in the arguments
                        3. **Include supporting documents** such as medical certificates, proof of residence, etc.
                        4. **Emphasize compliance** with any bail conditions the court may impose
                        5. **Address prosecution concerns** proactively in your application
                        """)
                    else:
                        st.markdown("""
                        When opposing bail as prosecution:
                        
                        1. **Structure your opposition** with these points in order of strength
                        2. **Support with precedents** cited in the arguments
                        3. **Include supporting evidence** of flight risk, threat to witnesses, etc.
                        4. **Emphasize gravity** of the offense and potential punishment
                        5. **Address defense arguments** proactively in your opposition
                        """)
                    
                    # Supporting precedents if available
                    precedents = bail_arguments_result.get("supporting_precedents", [])
                    if precedents:
                        st.markdown("### Supporting Legal Precedents")
                        for precedent in precedents:
                            with st.expander(f"{precedent['case_name']} ({precedent['citation']})"):
                                st.markdown(f"**Summary:** {precedent['summary']}")
                                st.markdown("**Key Points:**")
                                for point in precedent['key_points']:
                                    st.markdown(f"- {point}")

with tab3:
    st.markdown("## Bail Application Guide")
    st.markdown("""
    Step-by-step guide to preparing and filing bail applications in Indian courts,
    including required documents, procedures, and best practices.
    """)
    
    # Select application type
    application_type = st.selectbox(
        "Application Type",
        options=["Regular Bail (After Arrest)", "Anticipatory Bail (Before Arrest)", "Bail Pending Appeal"]
    )
    
    # Display appropriate guidance based on selection
    if application_type == "Regular Bail (After Arrest)":
        st.markdown("### Regular Bail Application Process")
        
        # Timeline
        st.markdown("#### Timeline")
        st.markdown("""
        1. **Arrest and Custody**: Accused is arrested and taken into custody
        2. **Production before Magistrate**: Within 24 hours of arrest
        3. **Bail Application Filing**: Can be filed immediately after production
        4. **Hearing**: Court schedules hearing (typically within 1-7 days)
        5. **Order**: Court passes order granting or rejecting bail
        6. **Compliance**: If granted, fulfill bail conditions and obtain release order
        """)
        
        # Required documents
        st.markdown("#### Required Documents")
        st.markdown("""
        1. **Bail Application**: In prescribed format as per court rules
        2. **Copy of FIR/Complaint**: Attach certified copy
        3. **Arrest Memo**: Copy of arrest memo if available
        4. **Medical Reports**: If there are health concerns
        5. **Vakalatnama**: Power of attorney for your lawyer
        6. **Supporting Affidavits**: Character certificates, employment proof, etc.
        7. **Previous Orders**: If bail was rejected earlier by lower court
        8. **Identity and Address Proof**: Of the accused and sureties
        """)
        
        # Key legal provisions
        st.markdown("#### Key Legal Provisions")
        st.markdown("""
        - **Section 437 CrPC**: Bail provisions for non-bailable offenses (Magistrate's power)
        - **Section 439 CrPC**: Special powers of High Court and Sessions Court regarding bail
        - **Section 436 CrPC**: Provisions for bailable offenses
        """)
        
        # Application format
        with st.expander("Sample Bail Application Format"):
            st.markdown("""
            ```
            IN THE COURT OF [COURT NAME], [LOCATION]
            
            Bail Application No. ____ of 20__
            
            IN THE MATTER OF:
            
            State vs. [Accused Name]
            FIR No. [FIR Number]
            Under Section [Sections] of [Act]
            Police Station [Police Station Name]
            
            APPLICATION FOR REGULAR BAIL UNDER SECTION 437/439 OF THE CODE OF CRIMINAL PROCEDURE, 1973
            
            RESPECTFULLY SHOWETH:
            
            1. That the applicant/accused was arrested on [date] in connection with FIR No. [number] under Section [sections] of [Act].
            
            2. That the allegations against the applicant are [briefly mention allegations].
            
            3. That the applicant is entitled to bail on the following grounds:
               [List all grounds for bail]
            
            4. [Additional grounds and arguments]
            
            PRAYER:
            
            It is, therefore, most respectfully prayed that this Hon'ble Court may graciously be pleased to:
            
            a) Release the applicant on bail in the above-mentioned case on such terms and conditions as this Hon'ble Court may deem fit and proper.
            
            b) Pass any other order which this Hon'ble Court may deem fit and proper in the facts and circumstances of the case.
            
            AND FOR THIS ACT OF KINDNESS, THE APPLICANT AS IN DUTY BOUND SHALL EVER PRAY.
            
            PLACE: [Place]
            DATE: [Date]                                                        ADVOCATE FOR THE APPLICANT
            ```
            """)
    
    elif application_type == "Anticipatory Bail (Before Arrest)":
        st.markdown("### Anticipatory Bail Application Process")
        
        # Timeline
        st.markdown("#### Timeline")
        st.markdown("""
        1. **Apprehension of Arrest**: When there's reason to believe arrest is imminent
        2. **Application Filing**: File anticipatory bail application under Section 438 CrPC
        3. **Interim Order**: Court may grant interim protection pending final hearing
        4. **Notice to Prosecution**: Court issues notice to prosecution/police
        5. **Final Hearing**: After hearing both sides, court passes final order
        6. **Execution**: If granted, the order is executed when arrest is attempted
        """)
        
        # Required documents
        st.markdown("#### Required Documents")
        st.markdown("""
        1. **Anticipatory Bail Application**: In prescribed format
        2. **Copy of FIR/Complaint**: If already registered
        3. **Threat Evidence**: Any evidence showing imminent arrest threat
        4. **Vakalatnama**: Power of attorney for your lawyer
        5. **Supporting Affidavits**: Character certificates, employment proof, etc.
        6. **Identity and Address Proof**: Of the applicant
        7. **Undertaking**: To cooperate with investigation if required
        """)
        
        # Key legal provisions
        st.markdown("#### Key Legal Provisions")
        st.markdown("""
        - **Section 438 CrPC**: Direction for grant of bail to person apprehending arrest
        - **Landmark Case**: Shri Gurbaksh Singh Sibbia vs. State of Punjab (1980)
        """)
        
        # Application format
        with st.expander("Sample Anticipatory Bail Application Format"):
            st.markdown("""
            ```
            IN THE COURT OF SESSIONS JUDGE / HIGH COURT OF [LOCATION]
            
            Anticipatory Bail Application No. ____ of 20__
            
            IN THE MATTER OF:
            
            [Applicant Name]                             ...APPLICANT
            
            VERSUS
            
            State of [State Name]                        ...RESPONDENT
            
            APPLICATION UNDER SECTION 438 CR.P.C. FOR GRANT OF ANTICIPATORY BAIL
            
            RESPECTFULLY SHOWETH:
            
            1. That the applicant is a law-abiding citizen of India [provide brief background].
            
            2. That the applicant has been falsely implicated in case FIR No. [number] under Section [sections] of [Act] registered at Police Station [name] OR the applicant apprehends arrest in connection with [details of potential case].
            
            3. That the actual facts of the case are as follows: [narrate true facts]
            
            4. That the applicant apprehends arrest in the above-mentioned case on the following grounds:
               [List grounds for apprehension]
            
            5. That the applicant is entitled to anticipatory bail on the following grounds:
               [List all grounds for anticipatory bail]
            
            6. [Additional grounds and arguments]
            
            7. That the applicant is ready and willing to abide by any condition that this Hon'ble Court may deem fit to impose.
            
            PRAYER:
            
            It is, therefore, most respectfully prayed that this Hon'ble Court may graciously be pleased to:
            
            a) Direct that in the event of arrest of the applicant in connection with [case details], the applicant be released on bail.
            
            b) Pass any other order which this Hon'ble Court may deem fit and proper in the facts and circumstances of the case.
            
            AND FOR THIS ACT OF KINDNESS, THE APPLICANT AS IN DUTY BOUND SHALL EVER PRAY.
            
            PLACE: [Place]
            DATE: [Date]                                                        ADVOCATE FOR THE APPLICANT
            ```
            """)
    
    else:  # Bail Pending Appeal
        st.markdown("### Bail Pending Appeal Process")
        
        # Timeline
        st.markdown("#### Timeline")
        st.markdown("""
        1. **Conviction and Sentence**: After court pronounces judgment
        2. **Appeal Filing**: File appeal against conviction and sentence
        3. **Bail Application**: File bail application pending appeal
        4. **Hearing**: Court schedules hearing on bail application
        5. **Order**: Court passes order on bail application
        6. **Compliance**: If granted, fulfill bail conditions and obtain release order
        """)
        
        # Required documents
        st.markdown("#### Required Documents")
        st.markdown("""
        1. **Bail Application**: In prescribed format
        2. **Copy of Judgment**: Certified copy of conviction and sentence
        3. **Appeal Memo**: Copy of appeal filed against conviction
        4. **Vakalatnama**: Power of attorney for your lawyer
        5. **Medical Reports**: If there are health concerns
        6. **Previous Orders**: Any previous bail orders in the case
        7. **Identity and Address Proof**: Of the appellant and sureties
        """)
        
        # Key legal provisions
        st.markdown("#### Key Legal Provisions")
        st.markdown("""
        - **Section 389 CrPC**: Suspension of sentence pending the appeal; release of appellant on bail
        - **Landmark Case**: Sanjay Chandra vs. CBI (2012)
        """)
        
        # Application format
        with st.expander("Sample Bail Pending Appeal Application Format"):
            st.markdown("""
            ```
            IN THE COURT OF SESSIONS JUDGE / HIGH COURT OF [LOCATION]
            
            Bail Application No. ____ of 20__
            
            IN THE MATTER OF:
            
            [Appellant Name]                             ...APPELLANT
            
            VERSUS
            
            State of [State Name]                        ...RESPONDENT
            
            APPLICATION UNDER SECTION 389 CR.P.C. FOR SUSPENSION OF SENTENCE AND GRANT OF BAIL PENDING APPEAL
            
            RESPECTFULLY SHOWETH:
            
            1. That the applicant/appellant has been convicted by [Court Name] vide judgment dated [date] in Case No. [number] under Section [sections] of [Act] and sentenced to [mention sentence].
            
            2. That against the said judgment, the appellant has preferred an appeal being Criminal Appeal No. [number], which is pending before this Hon'ble Court.
            
            3. That the applicant/appellant seeks suspension of sentence and release on bail during the pendency of the appeal on the following grounds:
               [List all grounds for bail]
            
            4. [Additional grounds and arguments]
            
            5. That the appeal is likely to take considerable time for final disposal and the appellant has already undergone [mention period] of the sentence.
            
            PRAYER:
            
            It is, therefore, most respectfully prayed that this Hon'ble Court may graciously be pleased to:
            
            a) Suspend the sentence imposed on the appellant and release the appellant on bail during the pendency of the appeal on such terms and conditions as this Hon'ble Court may deem fit.
            
            b) Pass any other order which this Hon'ble Court may deem fit and proper in the facts and circumstances of the case.
            
            AND FOR THIS ACT OF KINDNESS, THE APPLICANT AS IN DUTY BOUND SHALL EVER PRAY.
            
            PLACE: [Place]
            DATE: [Date]                                                        ADVOCATE FOR THE APPELLANT
            ```
            """)
    
    # Common bail conditions
    st.markdown("### Common Bail Conditions")
    st.markdown("""
    1. **Surety Bond**: Furnishing personal and/or surety bonds of specified amount
    2. **Travel Restrictions**: Not leaving jurisdiction without court permission
    3. **Passport Surrender**: Surrendering passport to prevent flight risk
    4. **Regular Attendance**: Marking attendance at police station periodically
    5. **Witness Non-interference**: Not contacting or influencing witnesses
    6. **Evidence Non-tampering**: Not tampering with evidence
    7. **Cooperation**: Cooperating with investigation/prosecution
    8. **Court Appearance**: Appearing for all court hearings
    """)
    
    # Common bail rejection grounds
    st.markdown("### Common Grounds for Bail Rejection")
    st.markdown("""
    1. **Flight Risk**: Likelihood of the accused fleeing from justice
    2. **Witness Tampering**: Possibility of influencing or threatening witnesses
    3. **Evidence Tampering**: Risk of destroying evidence
    4. **Repeat Offense**: History of committing similar offenses
    5. **Gravity of Offense**: Serious nature of the crime committed
    6. **Stage of Investigation**: Early stage where investigation may be hampered
    7. **Public Sentiment**: Potential for public disorder if released
    8. **Previous Conduct**: History of bail violations or absconding
    """)
    
    # Bail bond filing process
    st.markdown("### Bail Bond Filing Process")
    st.markdown("""
    1. **Obtain Bail Order**: Get certified copy of the bail order
    2. **Identify Sureties**: Arrange for sureties as per court order
    3. **Documentation**: Prepare surety affidavits with ID and address proofs
    4. **File Bond**: Submit bail bond with surety documents to court
    5. **Verification**: Court verifies surety documents and credentials
    6. **Release Order**: Court issues release order to the jail authority
    7. **Execution**: Present release order at jail for release of accused
    """)

# Add a disclaimer at the bottom
st.markdown("---")
st.caption("""
**Disclaimer**: This information is provided for educational purposes only and does not constitute legal advice. 
Always consult with a qualified legal professional for advice specific to your situation.
""")
