"""
Batch AI Retention Predictions Generator
==========================================

This script generates AI predictions for employee retention risk and business impact.
It processes all employees from the SuccessFactors dataset and saves predictions to Excel.

OUTPUT FILE: Employee_AI_Predictions.xlsx

ESTIMATED TIME: ~250 employees × 3 seconds per call = ~12-15 minutes

HOW TO RUN:
-----------
1. Ensure you're in the project directory
2. Run: python generate_retention_predictions.py
3. Wait for completion (progress will be shown)
4. Check output file: Employee_AI_Predictions.xlsx

API CONFIGURATION:
------------------
Currently using: AWS Bedrock (Claude 3.5 Sonnet)

To switch to BI API:
1. Comment out the "AWS Bedrock Configuration" section (lines 45-60)
2. Uncomment the "BI API Configuration" section (lines 65-80)
3. Update credentials if needed
"""

import pandas as pd
import json
import boto3
import time
from datetime import datetime
import sys

print("=" * 70)
print("AI RETENTION PREDICTIONS GENERATOR")
print("=" * 70)
print()

# ========================================
# API CONFIGURATION
# ========================================

# ============================================================
# AWS BEDROCK CONFIGURATION (CURRENTLY ACTIVE)
# ============================================================
print("✓ Using AWS Bedrock (Claude 3.5 Sonnet)")
print("  Region: us-east-1")
print("  Credentials: From ~/.aws/credentials")
print()

BEDROCK_CONFIG = {
    'model_id': 'anthropic.claude-3-5-sonnet-20240620-v1:0',
    'region': 'us-east-1',
    'max_tokens': 800,  # Increased for detailed reasoning
    'temperature': 0.2
}

try:
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=BEDROCK_CONFIG['region']
    )
    print("✓ AWS Bedrock client initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize AWS Bedrock: {str(e)}")
    print("  Please check your ~/.aws/credentials file")
    sys.exit(1)

def call_ai_api(prompt, max_retries=3):
    """Call AWS Bedrock API"""
    for attempt in range(max_retries):
        try:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": BEDROCK_CONFIG['max_tokens'],
                "temperature": BEDROCK_CONFIG['temperature'],
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = bedrock_runtime.invoke_model(
                modelId=BEDROCK_CONFIG['model_id'],
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                return "Error: Unexpected API response format"
                
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Error: {str(e)}"
            time.sleep(2)  # Wait before retry
            continue
    
    return "Error: Failed after retries"


# ============================================================
# BOEHRINGER INGELHEIM API CONFIGURATION (COMMENTED OUT)
# ============================================================
# To use BI API instead of Bedrock:
# 1. Comment out the AWS Bedrock section above (lines 45-91)
# 2. Uncomment this entire section
# 3. Update client_id and client_secret if needed
# ============================================================

# import requests
# 
# print("✓ Using Boehringer Ingelheim API (GPT-4o)")
# print("  Endpoint: api-gw.boehringer-ingelheim.com")
# print()
# 
# API_CONFIG = {
#     'client_id': '074c933c-112f-4acf-a6a5-3199e4c78eea',
#     'client_secret': 'ff7c6a75-1336-4594-b74e-f26065b87d4e',
#     'model_name': 'gpt-4o',
#     'token_url': 'https://api-gw.boehringer-ingelheim.com:443/api/oauth/token',
#     'api_url': 'https://api-gw.boehringer-ingelheim.com:443/llm-api/',
#     'temperature': 0.2,
#     'max_tokens': 800,
#     'completions_path': 'chat/completions'
# }
# 
# def get_api_token():
#     try:
#         token_response = requests.post(
#             API_CONFIG['token_url'],
#             data={
#                 'grant_type': 'client_credentials',
#                 'client_id': API_CONFIG['client_id'],
#                 'client_secret': API_CONFIG['client_secret']
#             },
#             headers={'Content-Type': 'application/x-www-form-urlencoded'}
#         )
#         token_response.raise_for_status()
#         return token_response.json()['access_token']
#     except Exception as e:
#         print(f"✗ Failed to get API token: {str(e)}")
#         return None
# 
# def call_ai_api(prompt, max_retries=3):
#     """Call BI API"""
#     token = get_api_token()
#     if not token:
#         return "Error: Unable to authenticate"
#     
#     url = f"{API_CONFIG['api_url']}{API_CONFIG['completions_path']}"
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }
#     
#     payload = {
#         'model': API_CONFIG['model_name'],
#         'messages': [{'role': 'user', 'content': prompt}],
#         'temperature': API_CONFIG['temperature'],
#         'max_tokens': API_CONFIG['max_tokens']
#     }
#     
#     for attempt in range(max_retries):
#         try:
#             response = requests.post(url, json=payload, headers=headers, timeout=30)
#             response.raise_for_status()
#             
#             response_data = response.json()
#             if 'choices' in response_data and len(response_data['choices']) > 0:
#                 return response_data['choices'][0]['message']['content']
#             else:
#                 return "Error: Unexpected API response format"
#         except Exception as e:
#             if attempt == max_retries - 1:
#                 return f"Error: {str(e)}"
#             time.sleep(2)
#             continue
#     
#     return "Error: Failed after retries"


# ========================================
# LOAD DATA
# ========================================

print()
print("=" * 70)
print("LOADING DATA")
print("=" * 70)

try:
    data = pd.read_excel("Employee_Dataset_SuccessFactors.xlsx")
    print(f"✓ Loaded {len(data)} employees from Employee_Dataset_SuccessFactors.xlsx")
except Exception as e:
    print(f"✗ Error loading data: {str(e)}")
    sys.exit(1)

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

# Convert categorical columns
categorical_columns = ['Retention_Risk', 'Business_Impact', 'Department', 'WorkLocation',
                      'English_Proficiency', 'Mobility', 'Availability', 'Education', 'Major',
                      'EmployeeID', 'Name', 'Designation', 'GeneralShift', 'Past_Experiences',
                      'MAG_Current_Year', 'MAG_Last_Year']

for col in categorical_columns:
    if col in data.columns:
        data[col] = data[col].astype(str).replace('nan', 'Unknown')

print("✓ Data cleaned and ready for processing")


# ========================================
# AI PREDICTION FUNCTION
# ========================================

def get_retention_prediction(employee):
    """Get AI prediction for retention risk and business impact"""
    
    # Extract employee info
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
        "availability": employee['Availability'],
        "mag_current": employee['MAG_Current_Year'],
        "mag_last": employee['MAG_Last_Year'],
        "past_experiences": employee['Past_Experiences']
    }
    
    prompt = f"""You are an experienced HR analyst predicting employee retention risk and business impact. Analyze this employee profile holistically.

Employee Profile:
{json.dumps(employee_info, indent=2)}

Evaluation Criteria:

RETENTION RISK (likelihood they will leave):
- High: Strong flight risk - low performance, stagnant career, compensation issues, disengagement signals
- Medium: Mixed signals - some concerns but also stability factors
- Low: Stable and engaged - growing in role, satisfied, strong performance

BUSINESS IMPACT (cost of losing them):
- High: Critical role, manages people, specialized skills, hard to replace, significant disruption
- Medium: Important contributor, some specialized knowledge, moderate replacement difficulty
- Low: Easier to replace, junior role, standard skills, minimal disruption

Consider holistically:
- Performance trajectory and career progression
- Role criticality and people management
- Compensation alignment with market/role
- Development indicators (MAG scores, training)
- Engagement signals (tenure, promotion timing)

IMPORTANT: 
- Refer to the employee by their first name in the reasoning (e.g., "John demonstrates..." not "This employee demonstrates...")
- Make reasoning personal and specific to their data
- Reference actual numbers from their profile

You MUST respond in EXACTLY this format:

Retention Risk: [High/Medium/Low]
Business Impact: [High/Medium/Low]
Reasoning: [First name] demonstrates [specific analysis referencing their actual data - performance rating, tenure, income, role, etc. Explain WHY you chose these specific risk and impact levels. Be specific and data-driven. 100-150 words.]

Now analyze and respond:"""
    
    return call_ai_api(prompt)


# ========================================
# PROCESS ALL EMPLOYEES
# ========================================

print()
print("=" * 70)
print("GENERATING PREDICTIONS")
print("=" * 70)
print(f"Processing {len(data)} employees...")
print(f"Estimated time: ~{len(data) * 3 / 60:.0f} minutes")
print()

results = []
errors = []
prediction_date = datetime.now().strftime("%Y-%m-%d")

for idx, row in data.iterrows():
    employee_id = row['EmployeeID']
    employee_name = row['Name']
    
    print(f"[{idx+1}/{len(data)}] Processing: {employee_name} ({employee_id})...", end=" ")
    
    try:
        # Get AI prediction
        ai_response = get_retention_prediction(row)
        
        if ai_response.startswith("Error:"):
            print(f"✗ FAILED - {ai_response}")
            errors.append({
                'EmployeeID': employee_id,
                'Name': employee_name,
                'Error': ai_response
            })
            # Add placeholder data
            results.append({
                'EmployeeID': employee_id,
                'Name': employee_name,
                'AI_Retention_Risk': 'Error',
                'AI_Business_Impact': 'Error',
                'AI_Retention_Reasoning': ai_response,
                'Prediction_Date': prediction_date
            })
            continue
        
        # Parse response
        lines = ai_response.strip().split('\n')
        retention_risk = None
        business_impact = None
        reasoning = ""
        
        for line in lines:
            line_stripped = line.strip()
            if 'Retention Risk:' in line_stripped:
                retention_risk = line_stripped.split(':', 1)[1].strip()
            elif 'Business Impact:' in line_stripped:
                business_impact = line_stripped.split(':', 1)[1].strip()
            elif 'Reasoning:' in line_stripped:
                reasoning = line_stripped.split(':', 1)[1].strip()
        
        # Validate
        if not retention_risk or not business_impact or not reasoning:
            print("✗ FAILED - Could not parse AI response")
            errors.append({
                'EmployeeID': employee_id,
                'Name': employee_name,
                'Error': 'Parse error',
                'RawResponse': ai_response
            })
            results.append({
                'EmployeeID': employee_id,
                'Name': employee_name,
                'AI_Retention_Risk': 'Parse Error',
                'AI_Business_Impact': 'Parse Error',
                'AI_Retention_Reasoning': ai_response,
                'Prediction_Date': prediction_date
            })
            continue
        
        # Add to results
        results.append({
            'EmployeeID': employee_id,
            'Name': employee_name,
            'AI_Retention_Risk': retention_risk,
            'AI_Business_Impact': business_impact,
            'AI_Retention_Reasoning': reasoning,
            'Prediction_Date': prediction_date
        })
        
        print("✓ SUCCESS")
        
        # Rate limiting - wait between calls
        time.sleep(1.5)  # 1.5 seconds between calls
        
    except Exception as e:
        print(f"✗ EXCEPTION - {str(e)}")
        errors.append({
            'EmployeeID': employee_id,
            'Name': employee_name,
            'Error': str(e)
        })
        results.append({
            'EmployeeID': employee_id,
            'Name': employee_name,
            'AI_Retention_Risk': 'Error',
            'AI_Business_Impact': 'Error',
            'AI_Retention_Reasoning': f"Exception: {str(e)}",
            'Prediction_Date': prediction_date
        })


# ========================================
# SAVE RESULTS
# ========================================

print()
print("=" * 70)
print("SAVING RESULTS")
print("=" * 70)

# Create DataFrame
predictions_df = pd.DataFrame(results)

# Save to Excel
output_file = "Employee_AI_Predictions.xlsx"
try:
    predictions_df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"✓ Predictions saved to: {output_file}")
except Exception as e:
    print(f"✗ Error saving file: {str(e)}")
    # Try CSV as backup
    csv_file = "Employee_AI_Predictions.csv"
    predictions_df.to_csv(csv_file, index=False)
    print(f"✓ Saved as CSV instead: {csv_file}")

# Save error log if there were errors
if errors:
    error_df = pd.DataFrame(errors)
    error_file = "prediction_errors.xlsx"
    error_df.to_excel(error_file, index=False, engine='openpyxl')
    print(f"⚠ {len(errors)} errors occurred - see: {error_file}")


# ========================================
# SUMMARY
# ========================================

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total Employees Processed: {len(results)}")
print(f"Successful Predictions: {len(results) - len(errors)}")
print(f"Failed Predictions: {len(errors)}")
print()

# Show distribution
if len(results) > len(errors):
    risk_counts = predictions_df['AI_Retention_Risk'].value_counts()
    impact_counts = predictions_df['AI_Business_Impact'].value_counts()
    
    print("Retention Risk Distribution:")
    for level in ['High', 'Medium', 'Low']:
        count = risk_counts.get(level, 0)
        pct = (count / len(results) * 100) if len(results) > 0 else 0
        print(f"  {level}: {count} ({pct:.1f}%)")
    
    print()
    print("Business Impact Distribution:")
    for level in ['High', 'Medium', 'Low']:
        count = impact_counts.get(level, 0)
        pct = (count / len(results) * 100) if len(results) > 0 else 0
        print(f"  {level}: {count} ({pct:.1f}%)")

print()
print("=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print()
print(f"Next steps:")
print(f"1. Review the output file: {output_file}")
print(f"2. Update your Streamlit app to read from this file")
print(f"3. Run: streamlit run Home.py")
print()
