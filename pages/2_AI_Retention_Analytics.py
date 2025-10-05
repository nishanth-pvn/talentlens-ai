import streamlit as st
import pandas as pd
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="AI Retention Analytics",
    page_icon="🎯",
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
    .low-risk {
        color: #27ae60;
        font-weight: bold;
    }
    .medium-risk {
        color: #f39c12;
        font-weight: bold;
    }
    .high-risk {
        color: #e74c3c;
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
    .ai-risk-low {
        color: #00E47C;
        font-weight: bold;
        background: rgba(0, 228, 124, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid rgba(0, 228, 124, 0.3);
    }
    .ai-risk-medium {
        color: #f39c12;
        font-weight: bold;
        background: rgba(243, 156, 18, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid rgba(243, 156, 18, 0.3);
    }
    .ai-risk-high {
        color: #e74c3c;
        font-weight: bold;
        background: rgba(231, 76, 60, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid rgba(231, 76, 60, 0.3);
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

@st.cache_data
def load_data():
    data = pd.read_excel("input/Employee_Dataset_SuccessFactors.xlsx")
    
    column_mapping = {
        'Retention Risk (High, Medium, Low)': 'Retention_Risk',
        'Business Impact': 'Business_Impact',
        'English Proficency': 'English_Proficiency',
        '# of People Managed': 'People_Managed',
        'Past experiences': 'Past_Experiences',
        'MAG current year': 'MAG_Current_Year',
        'MAG last year': 'MAG_Last_Year'
    }
    
    data = data.rename(columns=column_mapping)
    
    numeric_columns = ['Age', 'Tenure', 'AveragePerformanceRating', 'MonthsSincePromotion', 
                      'MonthlyIncome', 'People_Managed']
    
    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    categorical_columns = ['Retention_Risk', 'Business_Impact', 'Department', 'WorkLocation',
                          'English_Proficiency', 'Mobility', 'Availability', 'Education', 'Major',
                          'EmployeeID', 'Name', 'Designation', 'GeneralShift', 'Past_Experiences',
                          'MAG_Current_Year', 'MAG_Last_Year']
    
    for col in categorical_columns:
        if col in data.columns:
            data[col] = data[col].astype(str).replace('nan', 'Unknown')
    
    return data

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

def get_ai_risk_prediction(employee):
    employee_info = {
        "name": employee['Name'],
        "id": employee['EmployeeID'],
        "age": float(employee['Age']) if pd.notna(employee['Age']) else 0,
        "tenure": float(employee['Tenure']) if pd.notna(employee['Tenure']) else 0,
        "department": employee['Department'],
        "designation": employee['Designation'],
        "performance_rating": float(employee['AveragePerformanceRating']) if pd.notna(employee['AveragePerformanceRating']) else 0,
        "months_since_promotion": float(employee['MonthsSincePromotion']) if pd.notna(employee['MonthsSincePromotion']) else 0,
        "monthly_income": float(employee['MonthlyIncome']) if pd.notna(employee['MonthlyIncome']) else 0,
        "people_managed": float(employee['People_Managed']) if pd.notna(employee['People_Managed']) else 0,
        "work_location": employee['WorkLocation'],
        "education": employee['Education'],
        "english_proficiency": employee['English_Proficiency'],
        "mobility": employee['Mobility'],
        "mag_current": employee['MAG_Current_Year'],
        "mag_last": employee['MAG_Last_Year']
    }
    
    prompt = f"""You are an AI system that predicts employee retention risk and business impact. Analyze this employee profile and predict their retention risk and business impact.

Employee Profile:
{json.dumps(employee_info, indent=2)}

Consider these factors:
- Performance rating and career progression (promotions, tenure)
- Role responsibilities and people management
- Compensation relative to role and experience
- Education, skills, and career development (MAG performance)
- Work flexibility (location, mobility, availability)

Classify Retention Risk:
- High: Strong flight risk signals (low performance, long time since promotion, limited growth, low engagement indicators)
- Medium: Mixed signals or moderate concerns
- Low: Stable, engaged, growing in role

Classify Business Impact:
- High: Critical role, manages people, specialized skills, hard to replace
- Medium: Important contributor, some specialized knowledge
- Low: Easier to replace, junior role, standard skills

You MUST respond in EXACTLY this format with no other text:
Retention Risk: High
Business Impact: Medium
Reasoning: This employee shows signs of disengagement with below-average performance and limited career progression, but holds a critical role managing a team.

Now analyze and respond:"""
    
    return call_llm_api(prompt)

def get_hrbp_insights(employee, ai_risk, ai_impact):
    employee_info = {
        "name": employee['Name'],
        "department": employee['Department'],
        "designation": employee['Designation'],
        "retention_risk": ai_risk,
        "business_impact": ai_impact,
        "performance_rating": float(employee['AveragePerformanceRating']) if pd.notna(employee['AveragePerformanceRating']) else 0,
        "people_managed": float(employee['People_Managed']) if pd.notna(employee['People_Managed']) else 0
    }
    
    hrbp_guide = """
High Retention Risk HRBP Actions:
- Coach managers on high-touch 1:1 conversations using the I-GROW model
- Support use of Career Navigator and motivation surveys to uncover drivers
- Apply the 70/20/10 development framework
- Coordinate non-financial retention measures (e.g., leadership exposure, flexible work)
- Track retention risk in SuccessFactors Talent Cards
- Conduct retention check-ins and share best practices

Medium Retention Risk HRBP Actions:
- Provide managers with stay interview templates and structured questions
- Encourage job rotation, enrichment, and project involvement
- Use Skill Coach to align development goals
- Activate local health and well-being programs
- Coach managers on feedback models (e.g., SBI)

Low Retention Risk HRBP Actions:
- Encourage regular appreciation and communication
- Promote inclusive team activities and recognition programs
- Use Skill Coach and Career Navigator to identify and grow strengths
- Offer mentoring and peer coaching opportunities
"""
    
    prompt = f"""
You are an HRBP providing strategic action items for employee retention. Based on the employee profile and HRBP guide below, provide your response in the following format:

(2-3 sentences summarizing the employee's situation and priority level)

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

Focus on the retention risk level ({ai_risk}) and business impact ({ai_impact}). Be specific and data-driven. Keep total response under 200 words.
"""
    
    return call_llm_api(prompt)

def get_manager_insights(employee, ai_risk, ai_impact):
    employee_info = {
        "name": employee['Name'],
        "department": employee['Department'],
        "designation": employee['Designation'],
        "retention_risk": ai_risk,
        "business_impact": ai_impact,
        "performance_rating": float(employee['AveragePerformanceRating']) if pd.notna(employee['AveragePerformanceRating']) else 0,
        "people_managed": float(employee['People_Managed']) if pd.notna(employee['People_Managed']) else 0
    }
    
    manager_guide = """
High Retention Risk Manager Actions:
- Conduct 1:1 engagement dialogues to uncover emotional state, motivations, and needs
- Apply the 70/20/10 development framework
- Offer career growth opportunities and exposure to senior leadership
- Provide recognition and autonomy, including flexible work arrangements
- Assign mentors or coaches and use the I-GROW model for career planning

Medium Retention Risk Manager Actions:
- Hold monthly informal check-ins to monitor engagement
- Conduct stay interviews with questions like 'Why do you stay?'
- Provide development opportunities such as job enrichment and rotation
- Use coaching and mentoring to support growth
- Apply the SBI Feedback Model to recognize contributions

Low Retention Risk Manager Actions:
- Celebrate small wins and maintain open communication
- Assign tasks aligned with employees' natural strengths
- Ensure expectations are clear and provide necessary resources
- Promote an inclusive culture and encourage team collaboration
"""
    
    prompt = f"""
You are a Manager receiving guidance on retention actions for your direct report. Based on the employee profile and manager guide below, provide your response in the following format:

(2-3 sentences summarizing the employee's situation)

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

Focus on the retention risk level ({ai_risk}) and business impact ({ai_impact}). Be specific and practical. Keep total response under 200 words.
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
        
        risk_levels = ["All"] + sorted([risk for risk in data['Retention_Risk'].unique() if risk != 'Unknown'])
        selected_risk = st.selectbox("Risk Level", risk_levels)
        
        impact_levels = ["All"] + sorted([impact for impact in data['Business_Impact'].unique() if impact != 'Unknown'])
        selected_impact = st.selectbox("Business Impact", impact_levels)
    
    filtered_data = data.copy()
    if selected_dept != "All":
        filtered_data = filtered_data[filtered_data['Department'] == selected_dept]
    if selected_risk != "All":
        filtered_data = filtered_data[filtered_data['Retention_Risk'] == selected_risk]
    if selected_impact != "All":
        filtered_data = filtered_data[filtered_data['Business_Impact'] == selected_impact]
    
    st.markdown("<h6 style='text-align: center; color: black;'><font face='Verdana'>TalentLens AI</font></h6>",
    unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: grey;'><font face='Verdana'>(Retention Analytics Dashboard)</font></h6>",
    unsafe_allow_html=True)
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
        if 'ai_risk_level' in st.session_state:
            del st.session_state.ai_risk_level
        if 'ai_business_impact' in st.session_state:
            del st.session_state.ai_business_impact
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
        st.markdown('<div class="profile-header">Performance & Career Metrics</div>', unsafe_allow_html=True)
        
        performance_fields = [
            ("Performance Rating", f"{employee_data['AveragePerformanceRating']:.1f}/5" if pd.notna(employee_data['AveragePerformanceRating']) else "N/A"),
            ("Last Promotion", f"{employee_data['MonthsSincePromotion']:.0f} month(s)" if pd.notna(employee_data['MonthsSincePromotion']) else "N/A"),
            ("Tenure", f"{employee_data['Tenure']:.1f} years" if pd.notna(employee_data['Tenure']) else "N/A"),
            ("Monthly Income", f"${employee_data['MonthlyIncome']:,.0f}" if pd.notna(employee_data['MonthlyIncome']) else "N/A"),
            ("People Managed", f"{employee_data['People_Managed']:.0f}" if pd.notna(employee_data['People_Managed']) else "0"),
            ("Past Experience", str(employee_data['Past_Experiences'])),
            ("MAG Current Year", str(employee_data['MAG_Current_Year'])),
            ("MAG Last Year", str(employee_data['MAG_Last_Year']))
        ]
        
        for label, value in performance_fields:
            st.markdown(f'<div class="profile-field"><div class="profile-label">{label}</div><div class="profile-value"><b>{value}</b></div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown('<div class="profile-header">Retention Analysis</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="profile-header">Manager\'s Feedback (from SAP SuccessFactors)</div>', unsafe_allow_html=True)
        manager_risk = employee_data['Retention_Risk']
        manager_impact = employee_data['Business_Impact']
        manager_risk_color = {'Low': 'low-risk', 'Medium': 'medium-risk', 'High': 'high-risk'}[manager_risk]
        manager_impact_color = {'Low': 'low-risk', 'Medium': 'medium-risk', 'High': 'high-risk'}[manager_impact]
        
        st.markdown(f'<div class="profile-field"><div class="profile-label">Retention Risk:</div><div class="profile-value"><span class="{manager_risk_color}">{manager_risk}</span></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="profile-field"><div class="profile-label">Business Impact:</div><div class="profile-value"><span class="{manager_impact_color}">{manager_impact}</span></div></div>', unsafe_allow_html=True)
        
        st.markdown(' ', unsafe_allow_html=True)
        
        st.markdown('<div class="profile-header">AI Prediction</div>', unsafe_allow_html=True)
        
        if 'ai_prediction_done' not in st.session_state:
            st.session_state.ai_prediction_done = False
        
        if st.button("Generate AI Prediction", key="ai_predict_btn"):
            with st.spinner("Generating AI risk prediction..."):
                ai_prediction_raw = get_ai_risk_prediction(employee_data)
            
            try:
                if ai_prediction_raw.startswith("Error:"):
                    st.error(ai_prediction_raw)
                    st.session_state.ai_prediction_done = False
                else:
                    lines = ai_prediction_raw.strip().split('\n')
                    ai_risk_level = None
                    ai_business_impact = None
                    ai_reasoning = ""
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        if 'Retention Risk:' in line:
                            ai_risk_level = line.split(':', 1)[1].strip()
                        elif 'Business Impact:' in line:
                            ai_business_impact = line.split(':', 1)[1].strip()
                        elif 'Reasoning:' in line:
                            ai_reasoning = line.split(':', 1)[1].strip()
                    
                    if ai_risk_level and ai_business_impact:
                        valid_levels = ['High', 'Medium', 'Low']
                        if ai_risk_level not in valid_levels or ai_business_impact not in valid_levels:
                            st.error(f"Invalid prediction values received. Risk: {ai_risk_level}, Impact: {ai_business_impact}")
                            st.session_state.ai_prediction_done = False
                        else:
                            st.session_state.ai_risk_level = ai_risk_level
                            st.session_state.ai_business_impact = ai_business_impact
                            st.session_state.ai_reasoning = ai_reasoning if ai_reasoning else "No reasoning provided"
                            st.session_state.ai_prediction_done = True
                            st.rerun()
                    else:
                        st.error(f"Could not parse AI prediction. Please try again.")
                        st.write("Raw response:", ai_prediction_raw)
                        st.session_state.ai_prediction_done = False
            except Exception as e:
                st.error(f"Error parsing AI response: {str(e)}")
                st.write("Raw response:", ai_prediction_raw)
                st.session_state.ai_prediction_done = False
        
        if st.session_state.ai_prediction_done:
            ai_risk_level = st.session_state.ai_risk_level
            ai_business_impact = st.session_state.ai_business_impact
            
            risk_color_class = {'Low': 'ai-risk-low', 'Medium': 'ai-risk-medium', 'High': 'ai-risk-high'}[ai_risk_level]
            impact_color_class = {'Low': 'ai-risk-low', 'Medium': 'ai-risk-medium', 'High': 'ai-risk-high'}[ai_business_impact]
            
            st.markdown(f'<div class="profile-field"><div class="profile-label">Retention Risk:</div><div class="profile-value"><span class="{risk_color_class}">{ai_risk_level}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="profile-field"><div class="profile-label">Business Impact:</div><div class="profile-value"><span class="{impact_color_class}">{ai_business_impact}</span></div></div>', unsafe_allow_html=True)
            
            matrix_position = f"{ai_risk_level} Risk + {ai_business_impact} Impact"
            if ai_risk_level == "High" and ai_business_impact == "High":
                matrix_desc = "Critical employee at high risk - immediate action required"
            elif ai_risk_level == "Medium" and ai_business_impact == "Medium":
                matrix_desc = "Moderate risk and impact - proactive engagement needed"
            elif ai_risk_level == "Low" and ai_business_impact == "Low":
                matrix_desc = "Stable employee - minimal disruption if departed"
            else:
                matrix_desc = f"Mixed profile - {ai_risk_level.lower()} retention risk with {ai_business_impact.lower()} business impact"
            
            st.markdown(f'''
            <div class="ai-matrix-position-box">
                <div class="ai-matrix-position-title">AI Assessment: {matrix_position}</div>
                <div class="ai-matrix-position-desc">{matrix_desc}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('''
            <div class="hrbp-actions-section">
                <div class="hrbp-actions-header">HRBP Action Items</div>
            ''', unsafe_allow_html=True)
            
            with st.spinner("Generating HRBP recommendations..."):
                hrbp_actions = get_hrbp_insights(employee_data, ai_risk_level, ai_business_impact)
            
            st.markdown(hrbp_actions)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('''
            <div class="manager-actions-section">
                <div class="manager-actions-header">Manager Action Items</div>
            ''', unsafe_allow_html=True)
            
            with st.spinner("Generating Manager recommendations..."):
                manager_actions = get_manager_insights(employee_data, ai_risk_level, ai_business_impact)
            
            st.markdown(manager_actions)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()                    