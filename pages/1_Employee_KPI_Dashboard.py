import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Employee KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: white;
    }
    .metric-card {
        border-radius: 10px;
        padding: 2px;
        margin-bottom: 15px;
    }
    .metric-card-high {
        background-color: rgba(231,76,60,0.9);
    }
    .metric-card-medium {
        background-color: rgba(243,156,18,0.9);
    }
    .metric-card-low {
        background-color: rgba(39,174,96,0.9);
    }
    .metric-card-total {
        background-color: rgba(52,152,219,0.9);
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
    }
    .metric-value-high {
        color: #e74c3c;
    }
    .metric-value-medium {
        color: #f39c12;
    }
    .metric-value-low {
        color: #27ae60;
    }
    .metric-value-total {
        color: #3498db;
    }
    .metric-percentage {
        font-size: 14px;
        opacity: 0.8;
    }
    .metric-title {
        font-size: 16px;
        margin-bottom: 5px;
    }
    .section-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .stApp {
        background-color: white !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 10px;
    }
    
    /* Hide sidebar collapse button */
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* Hide default navigation in sidebar */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Make sidebar fixed */
    section[data-testid="stSidebar"] {
        width: 250px !important;
        min-width: 250px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        width: 250px !important;
        min-width: 250px !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data = pd.read_excel("input/Employee_Dataset_SuccessFactors.xlsx")
    
    # Clean column names
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
    
    # Convert numeric columns
    numeric_columns = ['Age', 'Tenure', 'AveragePerformanceRating', 'MonthsSincePromotion', 
                      'MonthlyIncome', 'People_Managed']
    
    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Ensure categorical columns are strings
    categorical_columns = ['Retention_Risk', 'Business_Impact', 'Department', 'WorkLocation',
                          'English_Proficiency', 'Mobility', 'Availability', 'Education', 'Major',
                          'EmployeeID', 'Name', 'Designation', 'GeneralShift', 'Past_Experiences',
                          'MAG_Current_Year', 'MAG_Last_Year']
    
    for col in categorical_columns:
        if col in data.columns:
            data[col] = data[col].astype(str).replace('nan', 'Unknown')
    
    return data

# Create Risk vs Business Impact Matrix
def create_risk_impact_matrix(data):
    matrix_data = data.groupby(['Retention_Risk', 'Business_Impact']).size().reset_index(name='count')
    matrix_pivot = matrix_data.pivot(index='Retention_Risk', columns='Business_Impact', values='count').fillna(0)
    
    risk_order = ['Low', 'Medium', 'High']
    impact_order = ['Low', 'Medium', 'High']
    
    matrix_pivot = matrix_pivot.reindex(index=risk_order, columns=impact_order, fill_value=0)
    
    fig = px.imshow(
        matrix_pivot,
        labels=dict(x="Business Impact", y="Retention Risk", color="Employee Count"),
        x=impact_order,
        y=risk_order,
        color_continuous_scale='RdYlBu_r',
        title='Retention Risk vs Business Impact Matrix'
    )
    
    for i, risk in enumerate(risk_order):
        for j, impact in enumerate(impact_order):
            count = matrix_pivot.loc[risk, impact]
            fig.add_annotation(
                x=j, y=i,
                text=str(int(count)),
                showarrow=False,
                font=dict(color="white" if count > matrix_pivot.max().max()/2 else "black", size=14)
            )
    
    fig.update_layout(height=300)
    return fig

# Main application
def main():
    data = load_data()
    
    # Sidebar
    with st.sidebar:
        st.text(' ')
        #st.text(' ')
        st.image("BI-Logo.png", width=125)
        st.text(' ')
        st.text(' ')
        
        #st.markdown("---")
        
        # Home button
        if st.button("🏠 Back to Home", key="home_btn", use_container_width=True):
            st.switch_page("Home.py")
        
        #st.markdown("---")
        
        st.markdown("### Filters")
        
        # Department filter
        departments = ["All"] + sorted([dept for dept in data['Department'].unique() if dept != 'Unknown'])
        selected_dept = st.selectbox("Department", departments)
        
        # Risk level filter
        risk_levels = ["All"] + sorted([risk for risk in data['Retention_Risk'].unique() if risk != 'Unknown'])
        selected_risk = st.selectbox("Risk Level", risk_levels)
        
        # Business Impact filter
        impact_levels = ["All"] + sorted([impact for impact in data['Business_Impact'].unique() if impact != 'Unknown'])
        selected_impact = st.selectbox("Business Impact", impact_levels)
    
    # Apply filters
    filtered_data = data.copy()
    if selected_dept != "All":
        filtered_data = filtered_data[filtered_data['Department'] == selected_dept]
    if selected_risk != "All":
        filtered_data = filtered_data[filtered_data['Retention_Risk'] == selected_risk]
    if selected_impact != "All":
        filtered_data = filtered_data[filtered_data['Business_Impact'] == selected_impact]
    
    # Title
    st.markdown("<h6 style='text-align: center; color: black;'><font face='Verdana'>TalentLens AI</font></h6>",
    unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: grey;'><font face='Verdana'>(SAP SuccessFactors - Employee KPI Dashboard)</font></h6>",
    unsafe_allow_html=True)
    st.text(' ')
    
    # Top KPI metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card metric-card-total">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-title">Total Employees</div><div class="metric-value metric-value-total">{len(filtered_data)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        high_risk_count = len(filtered_data[filtered_data['Retention_Risk'] == 'High'])
        high_risk_percentage = (high_risk_count / len(filtered_data) * 100) if len(filtered_data) > 0 else 0
        
        st.markdown('<div class="metric-card metric-card-high">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-title">High Risk Employees</div><div class="metric-value metric-value-high">{high_risk_count} <span class="metric-percentage">({high_risk_percentage:.1f}%)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        medium_risk_count = len(filtered_data[filtered_data['Retention_Risk'] == 'Medium'])
        medium_risk_percentage = (medium_risk_count / len(filtered_data) * 100) if len(filtered_data) > 0 else 0
        
        st.markdown('<div class="metric-card metric-card-medium">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-title">Medium Risk Employees</div><div class="metric-value metric-value-medium">{medium_risk_count} <span class="metric-percentage">({medium_risk_percentage:.1f}%)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        low_risk_count = len(filtered_data[filtered_data['Retention_Risk'] == 'Low'])
        low_risk_percentage = (low_risk_count / len(filtered_data) * 100) if len(filtered_data) > 0 else 0
        
        st.markdown('<div class="metric-card metric-card-low">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-title">Low Risk Employees</div><div class="metric-value metric-value-low">{low_risk_count} <span class="metric-percentage">({low_risk_percentage:.1f}%)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, spacer, col2 = st.columns([1,0.2,1])
    
    with col1:
        # Retention Risk Distribution
        risk_counts = filtered_data['Retention_Risk'].value_counts().reset_index()
        risk_counts.columns = ['Risk Level', 'Count']
        
        risk_order = {'Low': 0, 'Medium': 1, 'High': 2}
        risk_counts['Order'] = risk_counts['Risk Level'].map(risk_order)
        risk_counts = risk_counts.sort_values('Order')
        
        colors = {'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e74c3c'}
        
        fig = go.Figure(data=[go.Pie(
            labels=risk_counts['Risk Level'],
            values=risk_counts['Count'],
            hole=.4,
            marker_colors=[colors[level] for level in risk_counts['Risk Level']]
        )])
        
        fig.update_layout(
            title='Employee Retention Risk Distribution',
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        if not filtered_data.empty:
            matrix_fig = create_risk_impact_matrix(filtered_data)
            st.plotly_chart(matrix_fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters")
    
    col1, spacer, col2 = st.columns([1,0.2,1])
    
    with col1:
        # Work Location vs Risk
        if not filtered_data.empty:
            location_risk = pd.crosstab(filtered_data['WorkLocation'], filtered_data['Retention_Risk'])
            
            for risk in ['Low', 'Medium', 'High']:
                if risk not in location_risk.columns:
                    location_risk[risk] = 0
            
            available_columns = [col for col in ['Low', 'Medium', 'High'] if col in location_risk.columns]
            location_risk = location_risk[available_columns]
            
            fig = px.bar(
                location_risk, 
                barmode='group',
                color_discrete_map={'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e74c3c'},
                title='Risk by Work Location'
            )
            fig.update_layout(
                height=300, 
                xaxis_title="Work Location", 
                yaxis_title="Employee Count",
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters")
        
    with col2:
        # Performance vs Income
        if not filtered_data.empty:
            fig = px.scatter(
                filtered_data,
                x='AveragePerformanceRating',
                y='MonthlyIncome',
                color='Retention_Risk',
                size='People_Managed',
                hover_name='Name',
                hover_data=['MAG_Current_Year', 'MAG_Last_Year'],
                color_discrete_map={'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e74c3c'},
                title='Performance vs Income by Risk Level',
                category_orders={"Retention_Risk": ["Low", "Medium", "High"]}
            )
            fig.update_layout(
                height=300, 
                showlegend=False,
                xaxis_title="Performance Rating",
                yaxis_title="Monthly Income"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters")
    
    # Employee table
    st.markdown('<p class="section-title">Employee Information</p>', unsafe_allow_html=True)
    
    # Additional filter for table
    table_filter_col1, table_filter_col2 = st.columns([1, 3])
    
    with table_filter_col1:
        locations = ["All"] + sorted([loc for loc in data['WorkLocation'].unique() if loc != 'Unknown'])
        selected_location = st.selectbox("Filter by Work Location", locations)
    
    # Apply additional filters for table
    table_data = filtered_data.copy()
    if selected_location != "All":
        table_data = table_data[table_data['WorkLocation'] == selected_location]
   
    # Format columns with colors
    def highlight_retention_risk(val):
        color_map = {'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e74c3c'}
        return f'background-color: {color_map.get(val, "")};color:white;font-weight:bold'
    
    def highlight_business_impact(val):
        color_map = {'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e74c3c'}
        return f'background-color: {color_map.get(val, "")};color:white;font-weight:bold'
    
    display_cols = ['EmployeeID', 'Name', 'Department', 'Designation', 'WorkLocation', 'Business_Impact', 'Retention_Risk', 'Tenure',
                   'AveragePerformanceRating', 'MonthlyIncome']
    
    if not table_data.empty:
        display_df = table_data[display_cols].copy()
        
        try:
            display_df.index = display_df.index + 1
            styled_df = display_df.style.applymap(
                highlight_retention_risk, 
                subset=['Retention_Risk']
            ).applymap(
                highlight_business_impact,
                subset=['Business_Impact']
            ).format({
                'MonthlyIncome': '${:,.0f}',
                'Tenure': '{:.1f}',
                'AveragePerformanceRating': '{:.1f}',
                'People_Managed': '{:.0f}'
            })
            
            st.dataframe(styled_df, height=380, use_container_width=True)
        except Exception:
            st.dataframe(display_df, height=380, use_container_width=True)
    else:
        st.info("No employees match the current filters.")

if __name__ == "__main__":
    main()
