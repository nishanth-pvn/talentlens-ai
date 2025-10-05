import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="AI Leadership Potential",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: white;
    }
    .profile-section {
        margin-bottom: 20px;
    }
    .profile-header {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 10px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }
    .profile-field {
        display: flex;
        margin-bottom: 5px;
    }
    .profile-label {
        font-weight: 500;
        width: 50%;
    }
    .profile-value {
        width: 50%;
    }
    .low-potential {
        color: #e74c3c;
        font-weight: bold;
    }
    .medium-potential {
        color: #f39c12;
        font-weight: bold;
    }
    .high-potential {
        color: #27ae60;
        font-weight: bold;
    }
    .stApp {
        background-color: white !important;
    }
    .search-result-count {
        font-size: 12px;
        color: #666;
        margin-bottom: 5px;
    }
    .ai-potential-low {
        color: #e74c3c;
        font-weight: bold;
        background: rgba(231, 76, 60, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid rgba(231, 76, 60, 0.3);
    }
    .ai-potential-medium {
        color: #f39c12;
        font-weight: bold;
        background: rgba(243, 156, 18, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid rgba(243, 156, 18, 0.3);
    }
    .ai-potential-high {
        color: #00E47C;
        font-weight: bold;
        background: rgba(0, 228, 124, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid rgba(0, 228, 124, 0.3);
    }
    .ai-matrix-position-box {
        background: linear-gradient(145deg, #f0fffb 0%, #e6fffa 100%);
        border: 2px solid #7df3d1;
        border-radius: 10px;
        padding: 16px;
        margin: 15px 0;
        box-shadow: 0 3px 6px rgba(0, 228, 124, 0.1);
    }
    .ai-matrix-position-title {
        font-weight: bold;
        color: #08312A;
        margin-bottom: 8px;
        font-size: 15px;
    }
    .ai-matrix-position-desc {
        color: #0a4a3a;
        font-style: italic;
        line-height: 1.5;
        font-size: 14px;
    }
    .hrbp-actions-section {
        background: white;
        border: 3px dashed #00E47C;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        position: relative;
        box-shadow: 
            0 4px 6px rgba(0, 228, 124, 0.15),
            0 1px 3px rgba(0, 228, 124, 0.1);
        background: linear-gradient(145deg, #f8fffe 0%, #f0fffb 100%);
    }
    .hrbp-actions-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #00E47C, #08312A, #00E47C);
        border-radius: 10px 10px 0 0;
        animation: ai-pulse 3s ease-in-out infinite;
    }
    @keyframes ai-pulse {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }
    .hrbp-actions-header {
        color: #08312A;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 8px;
    }
    .hrbp-actions-content {
        background: rgba(0, 228, 124, 0.02);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #00E47C;
    }
    .manager-actions-section {
        background: white;
        border: 3px dotted #00E47C;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        position: relative;
        box-shadow: 
            0 4px 6px rgba(0, 228, 124, 0.15),
            0 1px 3px rgba(0, 228, 124, 0.1);
        background: linear-gradient(145deg, #f8fffe 0%, #f0fffb 100%);
    }
    .manager-actions-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #00E47C, #08312A, #00E47C);
        border-radius: 10px 10px 0 0;
        animation: ai-pulse 3s ease-in-out infinite;
    }
    .manager-actions-header {
        color: #08312A;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 8px;
    }
    .manager-actions-content {
        background: rgba(0, 228, 124, 0.02);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #00E47C;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00E47C 0%, #08312A 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 228, 124, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 228, 124, 0.4) !important;
        background: linear-gradient(135deg, #00d470 0%, #06281f 100%) !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    section[data-testid="stSidebar"] {
        width: 250px !important;
        min-width: 250px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        width: 250px !important;
        min-width: 250px !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: white !important;
        border: 2px solid #00E47C !important;
        color: #00E47C !important;
        box-shadow: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(0, 228, 124, 0.05) !important;
        border: 2px solid #00E47C !important;
        color: #00E47C !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 2px 8px rgba(0, 228, 124, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data = pd.read_excel("input/Employee_Dataset_LeadershipPrediction_Input.xlsx")
    
    column_mapping = {}
    
    for col in data.columns:
        if 'English Proficency' in str(col):
            column_mapping[col] = 'English_Proficiency'
        elif '# of People Managed' in str(col):
            column_mapping[col] = 'People_Managed'
        elif 'How many years of working' in str(col):
            column_mapping[col] = 'Years_Working'
        elif 'Past experiences' in str(col):
            column_mapping[col] = 'Past_Experiences'
        elif 'MAG current year' in str(col):
            column_mapping[col] = 'MAG_Current_Year'
        elif 'MAG last year' in str(col):
            column_mapping[col] = 'MAG_Last_Year'
        elif 'Motivational' in str(col) and 'leadership' in str(col):
            column_mapping[col] = 'Leadership_Score'
        elif 'Decide & Act with speed' in str(col):
            column_mapping[col] = 'Decide_Act_Speed'
        elif 'Deliver to win' in str(col):
            column_mapping[col] = 'Deliver_Win'
        elif 'Communicate' in str(col) and 'candor' in str(col):
            column_mapping[col] = 'Communicate_Candor'
        elif 'Collaborate' in str(col) and 'purose' in str(col):
            column_mapping[col] = 'Collaborate_Purpose'
        elif 'Innovate & Drive change' in str(col):
            column_mapping[col] = 'Innovate_Change'
        elif 'Stakeholder Management' in str(col):
            column_mapping[col] = 'Stakeholder_Management'
        elif 'Strategic vision' in str(col):
            column_mapping[col] = 'Strategic_Vision'
        elif 'Tech Fluency' in str(col):
            column_mapping[col] = 'Tech_Fluency'
        elif 'Coaching Skill' in str(col):
            column_mapping[col] = 'Coaching_Skill'
    
    data = data.rename(columns=column_mapping)
    
    numeric_columns = ['Age', 'Tenure', 'AveragePerformanceRating', 'MonthsSincePromotion', 
                      'MonthlyIncome', 'People_Managed', 'ProjectCount', 'CommuteTime',
                      'TrainingHours', 'Years_Working', 'Leadership_Score', 'Decide_Act_Speed',
                      'Deliver_Win', 'Communicate_Candor', 'Collaborate_Purpose', 'Innovate_Change',
                      'EQ', 'Stakeholder_Management', 'Strategic_Vision', 'Adaptability',
                      'Tech_Fluency', 'Coaching_Skill']
    
    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    categorical_columns = ['Department', 'WorkLocation', 'English_Proficiency', 'Mobility', 
                          'Availability', 'Education', 'Major', 'EmployeeID', 'Name', 
                          'Designation', 'GeneralShift', 'Past_Experiences',
                          'MAG_Current_Year', 'MAG_Last_Year']
    
    for col in categorical_columns:
        if col in data.columns:
            data[col] = data[col].astype(str).replace('nan', 'Unknown')
    
    return data

# API Configuration
try:
    API_CONFIG = {
        'client_id': st.secrets["client_id"],
        'client_secret': st.secrets["client_secret"],
        'model_name': st.secrets["model_name"],
        'token_url': st.secrets["token_url"],
        'api_url': st.secrets["api_url"],
        'temperature': float(st.secrets["temperature"]),
        'max_tokens': int(st.secrets["max_tokens"]),
        'completions_path': st.secrets["completions_path"]
    }
except KeyError as e:
    st.error(f"Missing secret configuration: {e}")
    st.stop()

@st.cache_resource
def get_api_token():
    try:
        token_response = requests.post(
            API_CONFIG['token_url'],
            data={
                'grant_type': 'client_credentials',
                'client_id': API_CONFIG['client_id'],
                'client_secret': API_CONFIG['client_secret']
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        token_response.raise_for_status()
        return token_response.json()['access_token']
    except Exception as e:
        st.error(f"Failed to get API token: {str(e)}")
        return None

def call_llm_api(prompt, max_retries=3):
    token = get_api_token()
    if not token:
        return "Error: Unable to authenticate with API"
    
    url = f"{API_CONFIG['api_url']}{API_CONFIG['completions_path']}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': API_CONFIG['model_name'],
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': API_CONFIG['temperature'],
        'max_tokens': API_CONFIG['max_tokens']
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            else:
                return "Error: Unexpected API response format"
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Error: {str(e)}"
            continue
    
    return "Error: Failed to get response from API"

def calculate_leadership_potential(employee):
    leadership_scores = []
    
    core_metrics = ['Leadership_Score', 'EQ', 'Strategic_Vision', 'Stakeholder_Management']
    for metric in core_metrics:
        if metric in employee.index and pd.notna(employee[metric]):
            leadership_scores.append(float(employee[metric]) * 1.2)
    
    feedback_metrics = ['Decide_Act_Speed', 'Deliver_Win', 'Communicate_Candor', 
                       'Collaborate_Purpose', 'Innovate_Change']
    for metric in feedback_metrics:
        if metric in employee.index and pd.notna(employee[metric]):
            leadership_scores.append(float(employee[metric]))
    
    additional_metrics = ['Adaptability', 'Coaching_Skill']
    for metric in additional_metrics:
        if metric in employee.index and pd.notna(employee[metric]):
            leadership_scores.append(float(employee[metric]) * 0.8)
    
    if leadership_scores:
        avg_score = sum(leadership_scores) / len(leadership_scores)
        return min(avg_score, 5.0)
    
    return 0.0

def get_ai_leadership_prediction(employee):
    leadership_score = calculate_leadership_potential(employee)
    
    def safe_get_numeric(key, default=0):
        if key in employee.index and pd.notna(employee[key]):
            return float(employee[key])
        return default
    
    def safe_get_string(key, default="Unknown"):
        if key in employee.index and pd.notna(employee[key]):
            return str(employee[key])
        return default
    
    employee_info = {
        "name": safe_get_string('Name'),
        "id": safe_get_string('EmployeeID'),
        "age": safe_get_numeric('Age'),
        "tenure": safe_get_numeric('Tenure'),
        "department": safe_get_string('Department'),
        "designation": safe_get_string('Designation'),
        "performance_rating": safe_get_numeric('AveragePerformanceRating'),
        "people_managed": safe_get_numeric('People_Managed'),
        "years_working": safe_get_numeric('Years_Working'),
        "education": safe_get_string('Education'),
        "leadership_score": safe_get_numeric('Leadership_Score'),
        "eq_score": safe_get_numeric('EQ'),
        "strategic_vision": safe_get_numeric('Strategic_Vision'),
        "stakeholder_mgmt": safe_get_numeric('Stakeholder_Management'),
        "decide_act_speed": safe_get_numeric('Decide_Act_Speed'),
        "deliver_win": safe_get_numeric('Deliver_Win'),
        "communicate_candor": safe_get_numeric('Communicate_Candor'),
        "collaborate_purpose": safe_get_numeric('Collaborate_Purpose'),
        "innovate_change": safe_get_numeric('Innovate_Change'),
        "adaptability": safe_get_numeric('Adaptability'),
        "coaching_skill": safe_get_numeric('Coaching_Skill')
    }
    
    prompt = f"""Analyze this employee's leadership potential. You must make a clear determination - High, Medium, or Low.

Employee Profile:
{json.dumps(employee_info, indent=2)}

Context: On a 1-5 scale, typical organizational distributions are:
- Scores 4.0-5.0 = Top 20-30% (exceptional)
- Scores 3.0-3.9 = Middle 40-50% (solid performers)  
- Scores 1.0-2.9 = Bottom 20-30% (needs development)

Your task: Assess this specific individual's readiness for expanded leadership roles.

HIGH Leadership Potential means:
- Multiple leadership scores at 4.0+ showing exceptional capability
- Strong people management track record (manages 3+ people) with high performance
- Clear evidence of strategic thinking and stakeholder influence
- Ready NOW for senior leadership roles

LOW Leadership Potential means:
- Most leadership scores below 3.0 showing significant gaps
- No people management experience AND weak performance (<3.5)
- Limited evidence of leadership behaviors or readiness
- Needs 2+ years of foundational development before leadership roles

MEDIUM Leadership Potential means:
- Mixed profile with some strengths and some gaps
- OR solid scores (3.0-3.9) but limited proven track record
- Shows promise but needs 6-18 months targeted development
- Not ready for immediate promotion but has potential

Be decisive. Look at the actual numbers. Don't default to Medium unless the profile truly is mixed.

You MUST respond in EXACTLY this format with no other text:
Leadership Potential: High
Reasoning: Strong leadership scores (Leadership 4.2, EQ 4.0, Strategic Vision 4.3) combined with management of 5 people and performance rating of 4.5 indicates exceptional leadership capability and readiness for senior roles.

Now analyze and respond:"""
    
    return call_llm_api(prompt)

def get_hrbp_leadership_insights(employee, ai_potential):
    def safe_get_numeric(key, default=0):
        if key in employee.index and pd.notna(employee[key]):
            return float(employee[key])
        return default
    
    def safe_get_string(key, default="Unknown"):
        if key in employee.index and pd.notna(employee[key]):
            return str(employee[key])
        return default
    
    employee_info = {
        "name": safe_get_string('Name'),
        "department": safe_get_string('Department'),
        "designation": safe_get_string('Designation'),
        "leadership_potential": ai_potential,
        "performance_rating": safe_get_numeric('AveragePerformanceRating'),
        "people_managed": safe_get_numeric('People_Managed')
    }
    
    hrbp_guide = """
High Leadership Potential HRBP Actions:
- Nominate for high-visibility leadership development programs and executive coaching
- Create stretch assignments and cross-functional project leadership opportunities
- Facilitate mentoring relationships with senior executives
- Support succession planning discussions and leadership pipeline development

Medium Leadership Potential HRBP Actions:
- Enroll in targeted leadership development courses and skill-building workshops
- Arrange job rotation opportunities and lateral moves for exposure
- Provide access to internal mentoring programs and leadership circles
- Support manager in creating individual development plans

Low Leadership Potential HRBP Actions:
- Assess foundational leadership competencies and create development roadmap
- Provide access to basic leadership training and communication skills workshops
- Support first-time people management opportunities
- Facilitate coaching on emotional intelligence and self-awareness
"""
    
    prompt = f"""You are an HRBP providing strategic leadership development action items. Based on the employee profile and HRBP guide below, provide your response in the following format:

(2-3 sentences summarizing the employee's leadership potential and development priority)

**Recommendations:**
 [Specific action item 1]
 [Specific action item 2]
 [Specific action item 3]
 [Specific action item 4]
 [Specific action item 5]

Employee Profile:
{json.dumps(employee_info, indent=2)}

HRBP Guide:
{hrbp_guide}

Focus on leadership potential level ({ai_potential}). Be specific and data-driven. Keep total response under 200 words.
"""
    
    return call_llm_api(prompt)

def get_manager_leadership_insights(employee, ai_potential):
    def safe_get_numeric(key, default=0):
        if key in employee.index and pd.notna(employee[key]):
            return float(employee[key])
        return default
    
    def safe_get_string(key, default="Unknown"):
        if key in employee.index and pd.notna(employee[key]):
            return str(employee[key])
        return default
    
    employee_info = {
        "name": safe_get_string('Name'),
        "department": safe_get_string('Department'),
        "designation": safe_get_string('Designation'),
        "leadership_potential": ai_potential,
        "performance_rating": safe_get_numeric('AveragePerformanceRating'),
        "people_managed": safe_get_numeric('People_Managed')
    }
    
    manager_guide = """
High Leadership Potential Manager Actions:
- Provide challenging stretch assignments with increased scope
- Delegate high-visibility projects and cross-functional leadership opportunities
- Schedule regular leadership development conversations using GROW model
- Create opportunities to present to senior leadership

Medium Leadership Potential Manager Actions:
- Assign team lead responsibilities for specific projects
- Provide opportunities to mentor junior team members
- Schedule monthly one-on-ones focused on leadership skill development
- Encourage participation in cross-departmental committees

Low Leadership Potential Manager Actions:
- Focus on building foundational leadership competencies
- Provide small-scale leadership opportunities like leading team meetings
- Offer regular coaching on communication and decision-making
- Support basic management and supervisory skills training
"""
    
    prompt = f"""You are a Manager receiving strategic leadership development action items for your direct report. Based on the employee profile and manager guide below, provide your response in the following format:

(2-3 sentences summarizing the employee's leadership potential and development priority)

**Recommendations:**
 [Specific action item 1]
 [Specific action item 2]
 [Specific action item 3]
 [Specific action item 4]
 [Specific action item 5]

Employee Profile:
{json.dumps(employee_info, indent=2)}

Manager Guide:
{manager_guide}

Focus on leadership potential level ({ai_potential}). Be specific and practical. Keep total response under 200 words.
"""
    
    return call_llm_api(prompt)

def search_employee_with_filter(filtered_data, data):
    search_option = st.radio("Search by:", ["Employee Name", "Employee ID"], horizontal=True)
    
    if 'last_search_option' not in st.session_state:
        st.session_state.last_search_option = search_option
    elif st.session_state.last_search_option != search_option:
        st.session_state.ai_prediction_done = False
        st.session_state.last_search_option = search_option
    
    if search_option == "Employee Name":
        filtered_names = filtered_data['Name'].dropna()
        filtered_names = filtered_names[filtered_names != 'Unknown'].sort_values().tolist()
        
        if filtered_names:
            filter_col, select_col = st.columns([1, 2])
            
            with filter_col:
                name_filter = st.text_input(
                    "Filter names:", 
                    key="name_filter",
                    placeholder="Type to filter...",
                    help="Type part of the employee name to filter the list"
                )
            
            if name_filter:
                filtered_names = [name for name in filtered_names if name_filter.lower() in name.lower()]
            
            with select_col:
                if filtered_names:
                    if name_filter:
                        st.markdown(f'<div class="search-result-count">Showing {len(filtered_names)} employees matching "{name_filter}"</div>', unsafe_allow_html=True)
                    
                    search_value = st.selectbox(
                        "Select Employee", 
                        filtered_names,
                        key="employee_name_select"
                    )
                    return data[data['Name'] == search_value].iloc[0]
                else:
                    st.warning(f"No employees match '{name_filter}'")
                    return None
        else:
            st.warning("No employees match the current filters.")
            return None
            
    else:
        filtered_ids = filtered_data['EmployeeID'].dropna()
        filtered_ids = filtered_ids[filtered_ids != 'Unknown'].sort_values().tolist()
        
        if filtered_ids:
            filter_col, select_col = st.columns([1, 2])
            
            with filter_col:
                id_filter = st.text_input(
                    "Filter IDs:", 
                    key="id_filter",
                    placeholder="Type to filter..."
                )
            
            if id_filter:
                filtered_ids = [emp_id for emp_id in filtered_ids if id_filter.lower() in str(emp_id).lower()]
            
            with select_col:
                if filtered_ids:
                    if id_filter:
                        st.markdown(f'<div class="search-result-count">Showing {len(filtered_ids)} employees matching "{id_filter}"</div>', unsafe_allow_html=True)
                    
                    search_value = st.selectbox(
                        "Select Employee ID", 
                        filtered_ids,
                        key="employee_id_select"
                    )
                    return data[data['EmployeeID'] == search_value].iloc[0]
                else:
                    st.warning(f"No employee IDs match '{id_filter}'")
                    return None
        else:
            st.warning("No employees match the current filters.")
            return None

def main():
    data = load_data()
    
    with st.sidebar:
        st.text(' ')
        #st.text(' ')
        st.image("BI-Logo.png", width=125)
        st.text(' ')
        st.text(' ')
        
        #st.markdown("---")
        
        if st.button("🏠 Back to Home", key="home_btn", use_container_width=True):
            st.switch_page("Home.py")
        
        #st.markdown("---")
        
        st.markdown("### Filters")
        
        departments = ["All"] + sorted([dept for dept in data['Department'].unique() if dept != 'Unknown'])
        selected_dept = st.selectbox("Department", departments)
        
        experience_levels = ["All", "Junior (0-5 years)", "Mid-level (6-15 years)", "Senior (16+ years)"]
        selected_experience = st.selectbox("Experience Level", experience_levels)
        
        education_levels = ["All"] + sorted([edu for edu in data['Education'].unique() if edu != 'Unknown'])
        selected_education = st.selectbox("Education Level", education_levels)
    
    filtered_data = data.copy()
    if selected_dept != "All":
        filtered_data = filtered_data[filtered_data['Department'] == selected_dept]
    
    if selected_experience != "All":
        if selected_experience == "Junior (0-5 years)":
            filtered_data = filtered_data[filtered_data['Years_Working'] <= 5]
        elif selected_experience == "Mid-level (6-15 years)":
            filtered_data = filtered_data[(filtered_data['Years_Working'] > 5) & (filtered_data['Years_Working'] <= 15)]
        elif selected_experience == "Senior (16+ years)":
            filtered_data = filtered_data[filtered_data['Years_Working'] > 15]
    
    if selected_education != "All":
        filtered_data = filtered_data[filtered_data['Education'] == selected_education]
    
    st.markdown("<h6 style='text-align: center; color: black;'><font face='Verdana'>TalentLens AI</font></h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: grey;'><font face='Verdana'>(Leadership Potential Dashboard)</font></h6>", unsafe_allow_html=True)
    st.text(' ')
    
    employee_data = search_employee_with_filter(filtered_data, data)
    
    if employee_data is None:
        return
    
    current_employee_id = str(employee_data['EmployeeID'])
    if 'last_employee_id' not in st.session_state:
        st.session_state.last_employee_id = current_employee_id
        st.session_state.ai_prediction_done = False
    elif st.session_state.last_employee_id != current_employee_id:
        st.session_state.last_employee_id = current_employee_id
        st.session_state.ai_prediction_done = False
        if 'ai_leadership_potential' in st.session_state:
            del st.session_state.ai_leadership_potential
        if 'ai_reasoning' in st.session_state:
            del st.session_state.ai_reasoning
    
    col1, col2 = st.columns([4, 6])
    
    with col1:
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown('<div class="profile-header">Basic Information</div>', unsafe_allow_html=True)
        
        fields = [
            ("Employee ID", str(employee_data['EmployeeID'])),
            ("Employee Name", str(employee_data['Name'])),
            ("Age", f"{employee_data['Age']:.0f} years" if pd.notna(employee_data['Age']) else "N/A"),
            ("Department", str(employee_data['Department'])),
            ("Designation", str(employee_data['Designation'])),
            ("Work Location", str(employee_data['WorkLocation'])),
            ("General Shift", str(employee_data['GeneralShift'])),
            ("Education", str(employee_data['Education'])),
            ("Major", str(employee_data['Major'])),
            ("English Proficiency", str(employee_data['English_Proficiency'])),
            ("Mobility", str(employee_data['Mobility'])),
            ("Availability", str(employee_data['Availability']))
        ]
        
        for label, value in fields:
            st.markdown(f'<div class="profile-field"><div class="profile-label">{label}</div><div class="profile-value"><b>{value}</b></div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown('<div class="profile-header">Performance & Leadership Metrics</div>', unsafe_allow_html=True)
        
        performance_fields = [
            ("Performance Rating", f"{employee_data['AveragePerformanceRating']:.1f}/5" if pd.notna(employee_data['AveragePerformanceRating']) else "N/A"),
            ("Last Promotion", f"{employee_data['MonthsSincePromotion']:.0f} month(s)" if pd.notna(employee_data['MonthsSincePromotion']) else "N/A"),
            ("Tenure", f"{employee_data['Tenure']:.1f} years" if pd.notna(employee_data['Tenure']) else "N/A"),
            ("Monthly Income", f"${employee_data['MonthlyIncome']:,.0f}" if pd.notna(employee_data['MonthlyIncome']) else "N/A"),
            ("People Managed", f"{employee_data['People_Managed']:.0f}" if pd.notna(employee_data['People_Managed']) else "0"),
            ("Years Working", f"{employee_data['Years_Working']:.0f}" if pd.notna(employee_data['Years_Working']) else "N/A"),
            ("Training Hours", f"{employee_data['TrainingHours']:.0f}" if pd.notna(employee_data['TrainingHours']) else "N/A"),
            ("Project Count", f"{employee_data['ProjectCount']:.0f}" if pd.notna(employee_data['ProjectCount']) else "N/A")
        ]
        
        for label, value in performance_fields:
            st.markdown(f'<div class="profile-field"><div class="profile-label">{label}</div><div class="profile-value"><b>{value}</b></div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown('<div class="profile-header">Leadership Assessment Scores</div>', unsafe_allow_html=True)
        
        def safe_display_value(employee, column, scale="/5"):
            if column in employee.index and pd.notna(employee[column]):
                return f"{employee[column]:.1f}{scale}"
            return "N/A"
        
        leadership_fields = [
            ("Leadership Score", safe_display_value(employee_data, 'Leadership_Score')),
            ("EQ (Emotional Intelligence)", safe_display_value(employee_data, 'EQ')),
            ("Strategic Vision", safe_display_value(employee_data, 'Strategic_Vision')),
            ("Stakeholder Management", safe_display_value(employee_data, 'Stakeholder_Management')),
            ("Coaching Skill", safe_display_value(employee_data, 'Coaching_Skill')),
            ("Adaptability", safe_display_value(employee_data, 'Adaptability'))
        ]
        
        for label, value in leadership_fields:
            st.markdown(f'<div class="profile-field"><div class="profile-label">{label}</div><div class="profile-value"><b>{value}</b></div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown('<div class="profile-header">360 Feedback Leadership Scores</div>', unsafe_allow_html=True)
        
        feedback_fields = [
            ("Decide & Act with Speed", safe_display_value(employee_data, 'Decide_Act_Speed')),
            ("Deliver to Win", safe_display_value(employee_data, 'Deliver_Win')),
            ("Communicate with Candor", safe_display_value(employee_data, 'Communicate_Candor')),
            ("Collaborate with Purpose", safe_display_value(employee_data, 'Collaborate_Purpose')),
            ("Innovate & Drive Change", safe_display_value(employee_data, 'Innovate_Change'))
        ]
        
        for label, value in feedback_fields:
            st.markdown(f'<div class="profile-field"><div class="profile-label">{label}</div><div class="profile-value"><b>{value}</b></div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown('<div class="profile-header">AI Leadership Potential Prediction</div>', unsafe_allow_html=True)
        
        if 'ai_prediction_done' not in st.session_state:
            st.session_state.ai_prediction_done = False
        
        if st.button("Generate AI Prediction", key="ai_predict_btn"):
            with st.spinner("Generating AI leadership potential prediction..."):
                ai_prediction_raw = get_ai_leadership_prediction(employee_data)
            
            try:
                if ai_prediction_raw.startswith("Error:"):
                    st.error(ai_prediction_raw)
                    st.session_state.ai_prediction_done = False
                else:
                    lines = ai_prediction_raw.strip().split('\n')
                    ai_leadership_potential = None
                    ai_reasoning = ""
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        if 'Leadership Potential:' in line:
                            ai_leadership_potential = line.split(':', 1)[1].strip()
                        elif 'Reasoning:' in line:
                            ai_reasoning = line.split(':', 1)[1].strip()
                    
                    if ai_leadership_potential:
                        valid_levels = ['High', 'Medium', 'Low']
                        if ai_leadership_potential not in valid_levels:
                            st.error(f"Invalid prediction value received: {ai_leadership_potential}")
                            st.session_state.ai_prediction_done = False
                        else:
                            st.session_state.ai_leadership_potential = ai_leadership_potential
                            st.session_state.ai_reasoning = ai_reasoning if ai_reasoning else "No reasoning provided"
                            st.session_state.ai_prediction_done = True
                            st.rerun()
                    else:
                        st.error("Could not parse AI prediction. Please try again.")
                        st.write("Raw response:", ai_prediction_raw)
                        st.session_state.ai_prediction_done = False
            except Exception as e:
                st.error(f"Error parsing AI response: {str(e)}")
                st.write("Raw response:", ai_prediction_raw)
                st.session_state.ai_prediction_done = False
        
        if st.session_state.ai_prediction_done:
            ai_leadership_potential = st.session_state.ai_leadership_potential
            
            potential_color_class = {'Low': 'ai-potential-low', 'Medium': 'ai-potential-medium', 'High': 'ai-potential-high'}[ai_leadership_potential]
            
            st.markdown(f'<div class="profile-field"><div class="profile-label">AI Leadership Potential:</div><div class="profile-value"><span class="{potential_color_class}">{ai_leadership_potential}</span></div></div>', unsafe_allow_html=True)
            
            if ai_leadership_potential == "High":
                matrix_desc = "Strong leadership candidate - ready for advanced development and succession planning"
            elif ai_leadership_potential == "Medium":
                matrix_desc = "Developing leader - focus on targeted skill building and leadership experiences"
            else:
                matrix_desc = "Early career leadership potential - needs foundational development and assessment"
            
            st.markdown(f'''
            <div class="ai-matrix-position-box">
                <div class="ai-matrix-position-title">AI Assessment: {ai_leadership_potential} Leadership Potential</div>
                <div class="ai-matrix-position-desc">{matrix_desc}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('''
            <div class="hrbp-actions-section">
                <div class="hrbp-actions-header">HRBP Action Items</div>
            ''', unsafe_allow_html=True)
            
            with st.spinner("Generating HRBP recommendations..."):
                hrbp_actions = get_hrbp_leadership_insights(employee_data, ai_leadership_potential)
            
            st.markdown(hrbp_actions)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('''
            <div class="manager-actions-section">
                <div class="manager-actions-header">Manager Action Items</div>
            ''', unsafe_allow_html=True)
            
            with st.spinner("Generating Manager recommendations..."):
                manager_actions = get_manager_leadership_insights(employee_data, ai_leadership_potential)
            
            st.markdown(manager_actions)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()