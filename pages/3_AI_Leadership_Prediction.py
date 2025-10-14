import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
import plotly.graph_objects as go

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
    .stApp {
        background-color: white !important;
    }
    .search-result-count {
        font-size: 12px;
        color: #666;
        margin-bottom: 5px;
    }
    .gauge-container {
        background: linear-gradient(145deg, #f0fffb 0%, #e6fffa 100%);
        border: 2px solid #7df3d1;
        border-radius: 10px;
        padding: 12px;
        margin: 15px 0;
        box-shadow: 0 2px 6px rgba(0, 228, 124, 0.1);
    }
    .gauge-title {
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        color: #08312A;
        margin-bottom: 5px;
    }
    .gauge-legend {
        text-align: center;
        font-size: 11px;
        color: #6b7280;
        margin-top: 5px;
        padding: 5px;
    }
    .legend-item {
        display: inline-block;
        margin: 0 8px;
    }
    .legend-color {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 2px;
        margin-right: 4px;
        vertical-align: middle;
    }
    .prediction-text {
        margin-top: 10px;
        padding: 10px;
        background: white;
        border-radius: 6px;
        border-left: 4px solid #e5e7eb;
    }
    .prediction-label {
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .prediction-reasoning {
        font-size: 13px;
        color: #4b5563;
        line-height: 1.5;
    }
    .hrbp-actions-section {
        background: white;
        border: 3px dashed #00E47C;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .hrbp-actions-header {
        color: #1f2937;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 15px;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 8px;
    }
    .manager-actions-section {
        background: white;
        border: 3px dotted #00E47C;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .manager-actions-header {
        color: #1f2937;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 15px;
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

# ========================================
# BI Internal API Configuration
# ========================================

API_CONFIG = {
    'client_id': '074c933c-112f-4acf-a6a5-3199e4c78eea',
    'client_secret': 'ff7c6a75-1336-4594-b74e-f26065b87d4e',
    'model_name': 'gpt-4.1',
    'token_url': 'https://api-gw.boehringer-ingelheim.com:443/api/oauth/token',
    'api_url': 'https://api-gw.boehringer-ingelheim.com:443/apollo/llm-api/',
    'temperature': 0.2,
    'max_tokens': 1000,
    'completions_path': 'chat/completions'
}

def get_access_token():
    """Get OAuth2 access token for BI API"""
    try:
        response = requests.post(
            API_CONFIG['token_url'],
            data={
                'grant_type': 'client_credentials',
                'client_id': API_CONFIG['client_id'],
                'client_secret': API_CONFIG['client_secret']
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        st.error(f"Failed to get access token: {str(e)}")
        return None

def call_llm_api(prompt, max_retries=3):
    """Call BI Internal LLM API (GPT-4o)"""
    for attempt in range(max_retries):
        try:
            # Get access token
            access_token = get_access_token()
            if not access_token:
                return "Error: Failed to authenticate with BI API"
            
            # Prepare request
            url = f"{API_CONFIG['api_url']}{API_CONFIG['completions_path']}"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': API_CONFIG['model_name'],
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': API_CONFIG['temperature'],
                'max_tokens': API_CONFIG['max_tokens']
            }
            
            # Make API call
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            # Parse response
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            else:
                return "Error: Unexpected API response format"
                
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"Error: {str(e)}"
            continue
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Error: {str(e)}"
            continue
    
    return "Error: Failed to get response from API"

def get_ai_leadership_prediction(employee):
    """Get AI holistic leadership prediction based on company framework"""
    
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
        "months_since_promotion": safe_get_numeric('MonthsSincePromotion'),
        "monthly_income": safe_get_numeric('MonthlyIncome'),
        "people_managed": safe_get_numeric('People_Managed'),
        "years_working": safe_get_numeric('Years_Working'),
        "work_location": safe_get_string('WorkLocation'),
        "education": safe_get_string('Education'),
        "english_proficiency": safe_get_string('English_Proficiency'),
        "mobility": safe_get_string('Mobility'),
        "training_hours": safe_get_numeric('TrainingHours'),
        "project_count": safe_get_numeric('ProjectCount'),
        "mag_current": safe_get_string('MAG_Current_Year'),
        "mag_last": safe_get_string('MAG_Last_Year'),
        "motivational_score": safe_get_numeric('Leadership_Score'),
        "eq_score": safe_get_numeric('EQ'),
        "strategic_vision": safe_get_numeric('Strategic_Vision'),
        "stakeholder_mgmt": safe_get_numeric('Stakeholder_Management'),
        "decide_act_speed": safe_get_numeric('Decide_Act_Speed'),
        "deliver_win": safe_get_numeric('Deliver_Win'),
        "communicate_candor": safe_get_numeric('Communicate_Candor'),
        "collaborate_purpose": safe_get_numeric('Collaborate_Purpose'),
        "innovate_change": safe_get_numeric('Innovate_Change'),
        "adaptability": safe_get_numeric('Adaptability'),
        "coaching_skill": safe_get_numeric('Coaching_Skill'),
        "tech_fluency": safe_get_numeric('Tech_Fluency')
    }
    
    prompt = f"""You are an experienced HR leadership assessor at a pharmaceutical company. Evaluate this employee's leadership potential using HOLISTIC JUDGMENT based on our Path to 2035 framework.

LEADERSHIP FRAMEWORK (Path to 2035):

Core Behaviors:
1. Decide and act with speed - Agile decision-making, quick action
2. Communicate with candor - Honest communication, receptive to feedback
3. Collaborate with purpose - Cross-functional teamwork, stakeholder management
4. Innovate and drive change - Creative thinking, continuous improvement
5. Deliver to win - Results orientation, accountability

Key Competencies:
- Strategic vision & adaptability
- Emotional intelligence & empathy
- Change leadership & organizational agility
- Stakeholder management & communication
- Digital fluency & tech-enabled innovation
- People development & coaching
- Cross-cultural competence

HOLISTIC ASSESSMENT APPROACH:

Consider the WHOLE person, not just scores. Look for:
- **Trajectory & Growth**: Is this person improving? Do they seek challenges and learn from them?
- **Impact & Influence**: Have they made a difference beyond their job description? Do others seek their input?
- **Potential vs. Current State**: Could they excel with the right development? What's their ceiling?
- **Context Matters**: A high performer in a small team may have different potential than someone managing large groups
- **Behavioral Patterns**: Do their scores reflect consistent behavior or isolated incidents?
- **Hidden Strengths**: Look for underutilized talents - maybe high EQ but not managing people yet, or strong tech fluency in a non-technical role

Score Interpretation Guide (Use as context, NOT rigid rules):
- Strong indicators: Performance 4.0+, key competencies 4.0+, manages people, demonstrates behaviors
- Development indicators: Performance 3.5-4.5, mixed competencies 3.0-4.0, showing growth
- Foundation-building indicators: Performance <3.5, competencies <3.0, early career, learning mindset

CRITICAL: Scores are DATA POINTS, not decisions. A person with 3.8 performance but exceptional EQ and growth mindset may have higher potential than someone with 4.2 performance but limited adaptability.

Employee Profile:
{json.dumps(employee_info, indent=2)}

Analyze this employee like a seasoned HR professional would:
- What story do the data points tell about their journey?
- Where do you see untapped potential or hidden strengths?
- What combination of factors suggests their leadership ceiling?
- How do their behaviors and competencies work together (or against each other)?
- What's your GUT feeling about their leadership trajectory?

Be thoughtful but NOT cautious - make a clear assessment based on the full picture. Aim for realistic distribution: ~15% High, ~60% Medium, ~25% Low.

You MUST respond in EXACTLY this format:

Leadership Potential: [High/Medium/Low]

**Key Observations:**

1. Performance Track Record
[Tell the story: What do their performance, tenure, and leadership scope reveal? Look for patterns and trajectory, not just numbers.]

2. Behavioral Alignment (Path to 2035)
[Assess how they embody each of the 5 core behaviors. Look at scores but also consider context - are they growing? Do behaviors complement each other? Use ✓ for clear strengths, ○ for developing areas, ~ for mixed signals.]

3. Development Readiness & Potential
[This is KEY: Beyond current state, what's their ceiling? Consider growth mindset, learning agility, impact potential, and hidden strengths. What makes them stand out or hold back?]

4. Holistic Assessment & Recommendation
[Synthesize everything: What's your professional judgment? Why this rating? What's the development priority? Consider the full context.]


**Conclusion:**

[2-3 sentences summarizing your holistic view of their leadership potential, readiness timeline, and what would unlock their next level]

IMPORTANT: Ensure there is a blank line before the **Conclusion:** section for proper formatting.

Keep response under 350 words. Be insightful, nuanced, and human in your assessment.

Now analyze and respond:"""
    
    return call_llm_api(prompt)

def create_progress_bar_chart(prediction_category):
    """Create progress bar visualization for leadership score"""
    
    # Gray color for non-predicted zones
    gray_color = 'rgba(209, 213, 219, 0.5)'
    
    # Determine which zone to highlight
    if prediction_category == "High":
        low_color = gray_color
        medium_color = gray_color
        high_color = '#00E47C'
    elif prediction_category == "Medium":
        low_color = gray_color
        medium_color = '#f39c12'
        high_color = gray_color
    else:
        low_color = '#e74c3c'
        medium_color = gray_color
        high_color = gray_color
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[33.33],
        y=[''],
        orientation='h',
        marker=dict(color=low_color),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Bar(
        x=[33.33],
        y=[''],
        orientation='h',
        marker=dict(color=medium_color),
        showlegend=False,
        hoverinfo='skip',
        base=33.33
    ))
    
    fig.add_trace(go.Bar(
        x=[33.34],
        y=[''],
        orientation='h',
        marker=dict(color=high_color),
        showlegend=False,
        hoverinfo='skip',
        base=66.66
    ))
    
    fig.update_layout(
        height=80,
        margin=dict(l=10, r=10, t=30, b=5),
        xaxis=dict(
            range=[0, 100],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        barmode='stack',
        bargap=0
    )
    
    fig.add_annotation(
        x=16.5, y=1.4,
        text="Low",
        showarrow=False,
        font=dict(size=11, color="#6b7280", family="Arial"),
        yref='y'
    )
    fig.add_annotation(
        x=50, y=1.4,
        text="Medium",
        showarrow=False,
        font=dict(size=11, color="#6b7280", family="Arial"),
        yref='y'
    )
    fig.add_annotation(
        x=83.5, y=1.4,
        text="High",
        showarrow=False,
        font=dict(size=11, color="#6b7280", family="Arial"),
        yref='y'
    )
    
    return fig

def get_hrbp_leadership_insights(employee, prediction_category):
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
        "leadership_potential": prediction_category,
        "performance_rating": safe_get_numeric('AveragePerformanceRating'),
        "people_managed": safe_get_numeric('People_Managed'),
        "tenure": safe_get_numeric('Tenure')
    }
    
    hrbp_guide = """
HRBP Development Framework (70-20-10 Model + Path to 2035):

High Leadership Potential Actions:
- Nominate for high-visibility leadership programs (e.g., ALDP) and executive coaching
- Design stretch assignments: cross-functional project leadership, strategic initiatives, innovation challenges
- Facilitate executive mentoring AND reverse mentoring (digital skills from younger talent)
- Support succession planning and leadership pipeline discussions
- Arrange cross-functional/cross-regional rotations for broader exposure
- Enroll in digital leadership programs (AI, data analytics, tech-enabled innovation)
- Include in Leadership Labs/simulations for decision-making under pressure
- Sponsor attendance at external pharma leadership forums and industry conferences

Medium Leadership Potential Actions:
- Enroll in targeted competency development: change leadership, strategic thinking, digital fluency
- Arrange lateral moves or job rotations for skill-building
- Provide access to internal mentoring programs and peer learning circles
- Support manager in creating 70-20-10 development plans with stretch projects
- Focus on closing specific gaps: EQ development, stakeholder management, innovation mindset
- Leverage LinkedIn Learning/Coursera for targeted skills (data literacy, communication)
- Include in cross-departmental task forces and innovation challenges
- Implement 360-degree feedback for self-awareness and development planning

Low Leadership Potential Actions:
- Assess foundational competencies and create multi-year development roadmap
- Provide basic leadership training: first-time manager programs, communication workshops
- Support small-scale leadership opportunities: team lead roles, project coordination
- Focus on core behaviors: decide with speed, collaborate with purpose, deliver to win
- Facilitate coaching on EQ, adaptability, and self-awareness
- Assign mentors for guided development and skill-building
- Encourage participation in skills training: technical depth, digital basics, stakeholder engagement
- Set clear milestones and regular check-ins to track progress
"""
    
    prompt = f"""You are an HRBP providing strategic leadership development action items. Based on the employee profile and development framework, provide ONLY specific recommendations in the following format:

**Recommendations:**
- [Specific action item 1 - be concrete and actionable]
- [Specific action item 2 - reference specific programs or approaches]
- [Specific action item 3 - tied to their specific gaps/strengths]
- [Specific action item 4 - practical next steps]
- [Specific action item 5 - measurable development action]

Employee Profile:
{json.dumps(employee_info, indent=2)}

HRBP Development Framework:
{hrbp_guide}

Focus on leadership potential level ({prediction_category}). Reference the 70-20-10 model, stretch assignments, rotations, mentoring as appropriate. Be specific, data-driven, and actionable. NO summary introduction - start directly with **Recommendations:**.

Keep under 150 words total.
"""
    
    return call_llm_api(prompt)

def get_manager_leadership_insights(employee, prediction_category):
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
        "leadership_potential": prediction_category,
        "performance_rating": safe_get_numeric('AveragePerformanceRating'),
        "people_managed": safe_get_numeric('People_Managed'),
        "tenure": safe_get_numeric('Tenure')
    }
    
    manager_guide = """
Manager Development Framework (Practical Actions):

High Leadership Potential Actions:
- Delegate high-visibility strategic projects with increased scope and autonomy
- Create opportunities to lead cross-functional initiatives and innovation challenges
- Provide regular leadership coaching using GROW model and behavior-based feedback
- Enable presentations to senior leadership and key stakeholders
- Empower with decision-making authority on strategic priorities
- Facilitate exposure to digital tools (AI, analytics) in daily work
- Encourage leading change initiatives and organizational improvements
- Support attendance at industry events and external learning opportunities

Medium Leadership Potential Actions:
- Assign team lead roles on specific projects or work streams
- Provide mentoring opportunities with junior team members
- Conduct focused one-on-ones on leadership skill development (monthly)
- Encourage participation in cross-departmental committees or task forces
- Give targeted feedback and coaching on specific competency gaps
- Support skill-building: data literacy, stakeholder management, strategic thinking
- Create safe opportunities to practice decision-making and problem-solving
- Sponsor participation in relevant training programs and workshops

Low Leadership Potential Actions:
- Focus on building foundational leadership competencies and core behaviors
- Provide small-scale leadership opportunities: leading team meetings, project coordination
- Offer regular coaching on communication, collaboration, and delivering results
- Support basic management training and supervisory skills development
- Work on developing growth mindset and openness to feedback
- Assign clear, achievable goals with regular check-ins and support
- Encourage participation in lunch & learns and peer learning sessions
- Build confidence through incremental responsibility and positive reinforcement
"""
    
    prompt = f"""You are a Manager receiving guidance on developing your direct report's leadership potential. Based on the profile and development framework, provide ONLY specific recommendations:

**Recommendations:**
- [Specific action item 1 - practical and implementable]
- [Specific action item 2 - tied to daily work]
- [Specific action item 3 - coaching or mentoring approach]
- [Specific action item 4 - stretch opportunity or delegation]
- [Specific action item 5 - skill-building activity]

Employee Profile:
{json.dumps(employee_info, indent=2)}

Manager Development Framework:
{manager_guide}

Focus on leadership potential level ({prediction_category}). Be specific, practical, and action-oriented. NO summary introduction - start directly with **Recommendations:**.

Keep under 150 words total.
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
        st.image("BI-Logo.png", width=125)
        st.text(' ')
        st.text(' ')
        
        if st.button("🏠 Back to Home", key="home_btn", use_container_width=True):
            st.switch_page("Home.py")
        
        st.markdown("### Filters")
        
        departments = ["All"] + sorted([dept for dept in data['Department'].unique() if dept != 'Unknown'])
        selected_dept = st.selectbox("Department", departments)
        
        education_levels = ["All"] + sorted([edu for edu in data['Education'].unique() if edu != 'Unknown'])
        selected_education = st.selectbox("Education Level", education_levels)
    
    filtered_data = data.copy()
    if selected_dept != "All":
        filtered_data = filtered_data[filtered_data['Department'] == selected_dept]
    
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
        if 'leadership_score_100' in st.session_state:
            del st.session_state.leadership_score_100
    
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
            ("Project Count", f"{employee_data['ProjectCount']:.0f}" if pd.notna(employee_data['ProjectCount']) else "N/A"),
            ("MAG Current Year", str(employee_data['MAG_Current_Year'])),
            ("MAG Last Year", str(employee_data['MAG_Last_Year']))
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
            ("Motivational Score", safe_display_value(employee_data, 'Leadership_Score')),
            ("EQ (Emotional Intelligence)", safe_display_value(employee_data, 'EQ')),
            ("Strategic Vision", safe_display_value(employee_data, 'Strategic_Vision')),
            ("Stakeholder Management", safe_display_value(employee_data, 'Stakeholder_Management')),
            ("Coaching Skill", safe_display_value(employee_data, 'Coaching_Skill')),
            ("Adaptability", safe_display_value(employee_data, 'Adaptability')),
            ("Tech Fluency", safe_display_value(employee_data, 'Tech_Fluency'))
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
            with st.spinner("Generating AI leadership assessment..."):
                ai_prediction_raw = get_ai_leadership_prediction(employee_data)
            
            try:
                if ai_prediction_raw.startswith("Error:"):
                    st.error(ai_prediction_raw)
                    st.session_state.ai_prediction_done = False
                else:
                    lines = ai_prediction_raw.strip().split('\n')
                    ai_leadership_potential = None
                    ai_reasoning = []
                    
                    for line in lines:
                        line_stripped = line.strip()
                        if not line_stripped:
                            continue
                        if 'Leadership Potential:' in line_stripped:
                            ai_leadership_potential = line_stripped.split(':', 1)[1].strip()
                        else:
                            ai_reasoning.append(line_stripped)
                    
                    full_reasoning = '\n'.join(ai_reasoning) if ai_reasoning else "No detailed analysis provided"
                    
                    if ai_leadership_potential:
                        valid_levels = ['High', 'Medium', 'Low']
                        if ai_leadership_potential not in valid_levels:
                            st.error(f"Invalid prediction value received: {ai_leadership_potential}")
                            st.session_state.ai_prediction_done = False
                        else:
                            st.session_state.prediction_category = ai_leadership_potential
                            st.session_state.prediction_description = full_reasoning
                            st.session_state.ai_prediction_done = True
                            
                            with st.spinner("Generating development recommendations..."):
                                hrbp_actions = get_hrbp_leadership_insights(employee_data, ai_leadership_potential)
                                st.session_state.hrbp_actions = hrbp_actions
                                
                                manager_actions = get_manager_leadership_insights(employee_data, ai_leadership_potential)
                                st.session_state.manager_actions = manager_actions
                            
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
            progress_fig = create_progress_bar_chart(st.session_state.prediction_category)
            st.plotly_chart(progress_fig, use_container_width=True)
            
            if st.session_state.prediction_category == "High":
                box_color = "#00E47C"
            elif st.session_state.prediction_category == "Medium":
                box_color = "#f39c12"
            else:
                box_color = "#e74c3c"
            
            st.markdown(f'''
                <div style="
                    background-color: rgba({int(box_color[1:3], 16)}, {int(box_color[3:5], 16)}, {int(box_color[5:7], 16)}, 0.1);
                    border: 2px solid {box_color};
                    border-radius: 8px;
                    padding: 12px;
                    margin: 10px 0;
                    text-align: center;
                ">
                    <div style="font-weight: bold; font-size: 16px; color: {box_color};">
                        Leadership Potential: {st.session_state.prediction_category}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            with st.expander("📋 Detailed Analysis", expanded=False):
                formatted_description = st.session_state.prediction_description.replace(
                    '**Conclusion:**', 
                    '\n\n---\n\n**Conclusion:**'
                )
                st.markdown(formatted_description)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.prediction_category == "High":
                border_color = "#00E47C"
            elif st.session_state.prediction_category == "Medium":
                border_color = "#f39c12"
            else:
                border_color = "#e74c3c"
            
            st.markdown(f'''
            <div class="hrbp-actions-section" style="border-color: {border_color};">
                <div class="hrbp-actions-header">HRBP Action Items</div>
            </div>
            ''', unsafe_allow_html=True)
            
            hrbp_content = st.session_state.hrbp_actions
            if "**Recommendations:**" in hrbp_content:
                hrbp_recommendations = hrbp_content.split("**Recommendations:**")[1].strip()
            else:
                hrbp_recommendations = hrbp_content
            
            hrbp_lines = hrbp_recommendations.split('\n')
            hrbp_formatted = []
            for line in hrbp_lines:
                line = line.strip()
                if line and not line.startswith('-') and not line.startswith('•'):
                    if line[0].isdigit() and '.' in line[:3]:
                        line = line.split('.', 1)[1].strip()
                    hrbp_formatted.append(f"- {line}")
                elif line:
                    hrbp_formatted.append(line)
            
            st.markdown('\n'.join(hrbp_formatted))
            
            st.markdown(f'''
            <div class="manager-actions-section" style="border-color: {border_color};">
                <div class="manager-actions-header">Manager Action Items</div>
            </div>
            ''', unsafe_allow_html=True)
            
            manager_content = st.session_state.manager_actions
            if "**Recommendations:**" in manager_content:
                manager_recommendations = manager_content.split("**Recommendations:**")[1].strip()
            else:
                manager_recommendations = manager_content
            
            manager_lines = manager_recommendations.split('\n')
            manager_formatted = []
            for line in manager_lines:
                line = line.strip()
                if line and not line.startswith('-') and not line.startswith('•'):
                    if line[0].isdigit() and '.' in line[:3]:
                        line = line.split('.', 1)[1].strip()
                    manager_formatted.append(f"- {line}")
                elif line:
                    manager_formatted.append(line)
            
            st.markdown('\n'.join(manager_formatted))

if __name__ == "__main__":
    main()
