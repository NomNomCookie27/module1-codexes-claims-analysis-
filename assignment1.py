import pandas as pd

# Load the dataset with the correct delimiter '|' and low_memory=False to handle mixed data types
file_path = 'inpatient.csv'
df = pd.read_csv(file_path, delimiter= '|', low_memory=False)

# Display the first few rows of the dataset
print(df.head())

# Identify possible codex columns using relevant keywords
possible_codex_keywords = ['code', 'icd', 'drg', 'hcpcs', 'procedure', 'diagnosis']
codex_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in possible_codex_keywords)]

# Print the identified codex columns
print("Identified Codex Columns:", codex_columns)

# Function to perform frequency analysis on a given list of columns
def analyze_codex_frequency(df, columns, description):
    print(f"\nAnalyzing {description}:")
    for col in columns:
        print(f"\nFrequency of unique values in {col}:")
        print(df[col].value_counts().head(10))  # Show top 10 for brevity

# ICD Diagnosis Codes
icd_diagnosis_columns = [col for col in codex_columns if 'dgns_cd' in col.lower() and 'e_cd' not in col.lower()]
analyze_codex_frequency(df, icd_diagnosis_columns, 'ICD Diagnosis Codes')

# ICD External Cause Diagnosis Codes
icd_external_cause_columns = [col for col in codex_columns if 'dgns_e_cd' in col.lower()]
analyze_codex_frequency(df, icd_external_cause_columns, 'ICD External Cause Diagnosis Codes')

# ICD Procedure Codes
icd_procedure_columns = [col for col in codex_columns if 'prcdr_cd' in col.lower()]
analyze_codex_frequency(df, icd_procedure_columns, 'ICD Procedure Codes')

# DRG Codes
drg_columns = ['CLM_DRG_CD', 'CLM_DRG_OUTLIER_STAY_CD', 'NCH_DRG_OUTLIER_APRVD_PMT_AMT']
analyze_codex_frequency(df, drg_columns, 'DRG Codes')

# HCPCS Codes
hcpcs_columns = ['HCPCS_CD']
analyze_codex_frequency(df, hcpcs_columns, 'HCPCS Codes')

# Claim Query Codes
claim_query_columns = ['CLAIM_QUERY_CODE']
analyze_codex_frequency(df, claim_query_columns, 'Claim Query Codes')

# DRG Weights
drg_weight_columns = ['CLM_PPS_CPTL_DRG_WT_NUM']
analyze_codex_frequency(df, drg_weight_columns, 'DRG Weights')

# Checking for missing or null values in codex columns and filling with 'Unknown' if missing
for column in codex_columns:
    missing_count = df[column].isnull().sum()
    print(f"Missing values in {column}: {missing_count}")  # Output the count of missing values
    
    if missing_count > 0:
        df[column] = df[column].fillna('Unknown')
        print(f"Filled missing values in {column} with 'Unknown'.")

# Checking if 'region' column or similar exists for geographical analysis
region_columns = [col for col in df.columns if 'region' in col.lower() or 'state' in col.lower()]

# Summarizing most common codes for each codex type
common_codes_summary = {column: df[column].value_counts().head(10) for column in codex_columns}

# Analyzing regional patterns using a sample of the data to avoid memory issues
regional_patterns = {}
if region_columns:
    region_col = region_columns[0]  # Use the first identified region column
    sample_data = df[[region_col] + codex_columns].sample(frac=0.4, random_state=1)  # Using 40% of the data as a sample
    
    for column in codex_columns:
        regional_patterns[column] = sample_data.groupby(region_col)[column].value_counts().unstack(fill_value=0).head(10)
        
# Displaying the summarized results
# Printing Most Common Codes Summary
print("Most Common Codes Summary:")
for column, summary in common_codes_summary.items():
    print(f"\nColumn: {column}")
    print(summary)

# Displaying regional patterns analysis if available
if regional_patterns:
    print("\nRegional Patterns Analysis:")
    for column, pattern in regional_patterns.items():
        print(f"\nRegional Analysis for {column}:")
        print(pattern.head(10))  # Display the first few rows for brevity
else:
    print("No regional columns were found for analysis.")

