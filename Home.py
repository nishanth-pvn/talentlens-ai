import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="TalentLens AI - Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: white;
    }
    .stApp {
        background-color: white !important;
    }
    
    /* Hide sidebar collapse button */
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* Hide default navigation in sidebar */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Make sidebar always visible and fixed */
    section[data-testid="stSidebar"] {
        width: 250px !important;
        min-width: 250px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        width: 250px !important;
        min-width: 250px !important;
    }
    
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 2px solid #e5e7eb;
        height: 100%;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .ai-card {
        border: 2px solid #00E47C;
        background: linear-gradient(145deg, #ffffff 0%, #f8fffe 100%);
    }
    
    .ai-card:hover {
        border-color: #00d470;
        box-shadow: 0 8px 15px rgba(0, 228, 124, 0.2);
    }
    
    .standard-card {
        border: 2px solid #3498db;
        background: linear-gradient(145deg, #ffffff 0%, #f8fbff 100%);
    }
    
    .standard-card:hover {
        border-color: #2980b9;
        box-shadow: 0 8px 15px rgba(52, 152, 219, 0.2);
    }
    
    .card-icon {
        font-size: 48px;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .card-title {
        font-size: 24px;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 8px;
        text-align: center;
    }
    
    .card-subtitle {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 15px;
        text-align: center;
        font-style: italic;
    }
    
    .card-description {
        font-size: 15px;
        color: #4b5563;
        line-height: 1.6;
        margin-bottom: 20px;
        text-align: center;
        min-height: 60px;
    }
    
    .ai-badge {
        display: inline-block;
        background: linear-gradient(135deg, #00E47C 0%, #08312A 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    
    .standard-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00E47C 0%, #08312A 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 228, 124, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 228, 124, 0.4) !important;
        background: linear-gradient(135deg, #00d470 0%, #06281f 100%) !important;
    }
    
    .header-section {
        text-align: center;
        margin-bottom: 40px;
        padding: 20px;
    }
    
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 10px;
    }
    
    .main-subtitle {
        font-size: 18px;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Sidebar with Logo
    with st.sidebar:
        st.text(" ")
        st.text(" ")
        st.image("BI-Logo.png", width=125)
    
    # Main Title (centered)
    #st.markdown('<h1 style="text-align: center; font-size: 33px; font-weight: bold; color: #1f2937; ">TalentLens AI</h1>', unsafe_allow_html=True)
    st.markdown('''
<h1 style="
    text-align: center; 
    font-size: 33px; 
    font-weight: 600; 
    color: #1f2937; 
    font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-bottom: 10px;
">TalentLens AI</h1>
''', unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="text-align: center;"><span class="standard-badge">ANALYTICS</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-icon">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Employee KPI Dashboard</div>', unsafe_allow_html=True)
        st.text(' ')
        st.markdown('<div class="card-description">Analyze key metrics, retention risk distribution and employee profile data from SAP SuccessFactors across departments</div>', unsafe_allow_html=True)
        
        # Center the button
        btn_col1, btn_col2, btn_col3 = st.columns([0.2, 2, 0.2])
        with btn_col2:
            if st.button("View KPI Metrics", key="kpi_btn", use_container_width=True):
                st.switch_page("pages/1_Employee_KPI_Dashboard.py")
    
    with col2:
        st.markdown('<div style="text-align: center;"><span class="ai-badge">AI</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-icon">🎯</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Retention Analytics</div>', unsafe_allow_html=True)
        st.text(' ')
        st.markdown('<div class="card-description">AI-enabled retention risk assessment with personalized HRBP and Manager action items for targeted interventions</div>', unsafe_allow_html=True)
        
        # Center the button
        btn_col1, btn_col2, btn_col3 = st.columns([0.2, 2, 0.2])
        with btn_col2:
            if st.button("Analyze Retention Risk", key="retention_btn", use_container_width=True):
                st.switch_page("pages/2_AI_Retention_Analytics.py")
    
    with col3:
        st.markdown('<div style="text-align: center;"><span class="ai-badge">AI</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-icon">👥</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Leadership Prediction</div>', unsafe_allow_html=True)
        st.text(' ')
        st.markdown('<div class="card-description">AI-driven leadership assessment with personalized HRBP and Manager action items for talent development</div>', unsafe_allow_html=True)
        
        # Center the button
        btn_col1, btn_col2, btn_col3 = st.columns([0.1, 2, 0.1])
        with btn_col2:
            if st.button("Assess Leadership Potential", key="leadership_btn", use_container_width=True):
                st.switch_page("pages/3_AI_Leadership_Prediction.py")

if __name__ == "__main__":
    main()
