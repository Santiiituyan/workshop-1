import pandas as pd

def clean_data(df):
    """
    Applies data cleaning and Data Quality Assumptions.
    Strategy: Relaxing Thresholds to avoid bias and preserve sample size.
    """
    # 1. Remove exact duplicates or by Email (keep the most recent application)
    df = df.drop_duplicates(subset=['Email'], keep='last').copy()
    
    # 2. Apply Quality Rule: Eliminate only extreme outliers
    # We broadened the margins for career changers and unusual profiles
    # Data is only removed if statistically improbable.
    filtro_intern = ~((df['Seniority'] == 'Intern') & (df['YOE'] > 10))
    filtro_trainee = ~((df['Seniority'] == 'Trainee') & (df['YOE'] > 12))
    filtro_junior = ~((df['Seniority'] == 'Junior') & (df['YOE'] > 15))
    
    # General sanity check: No negative years or experience exceeding 50 years
    filtro_cordura = (df['YOE'] >= 0) & (df['YOE'] <= 50)
    
    df = df[filtro_intern & filtro_trainee & filtro_junior & filtro_cordura]
    
    # 3. MANDATORY BUSINESS RULE (HIRED STATUS)
    # Logic: Code Challenge >= 7 AND Technical Interview >= 7
    df['Is_Hired'] = ((df['Code Challenge Score'] >= 7) & 
                      (df['Technical Interview Score'] >= 7)).astype(int)
    
    print(f"Cleaning complete. Records saved: {len(df)}")
    return df

def transform_to_star_schema(df):
    """
    Transforms the cleaned dataset into the 5 Data Warehouse tables.
    """
    df_clean = clean_data(df)
    
    # ==========================================
    # DIMENSION CREATION (Generating Surrogate Keys)
    # ==========================================
    
    # 1. Dim_Location
    dim_location = df_clean[['Country']].drop_duplicates().reset_index(drop=True)
    dim_location['Location_SK'] = dim_location.index + 1
    
    # 2. Dim_Technology
    dim_technology = df_clean[['Technology']].drop_duplicates().reset_index(drop=True)
    dim_technology.rename(columns={'Technology': 'Technology_Name'}, inplace=True)
    dim_technology['Technology_SK'] = dim_technology.index + 1
    
    # 3. Dim_Date (Convert application date and extract attributes)
    df_clean['Application Date'] = pd.to_datetime(df_clean['Application Date'])
    dim_date = df_clean[['Application Date']].drop_duplicates().reset_index(drop=True)
    dim_date['Date_SK'] = dim_date['Application Date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['Year'] = dim_date['Application Date'].dt.year
    dim_date['Month'] = dim_date['Application Date'].dt.month
    dim_date['Day'] = dim_date['Application Date'].dt.day
    dim_date.rename(columns={'Application Date': 'Full_Date'}, inplace=True)
    
    # 4. Dim_Candidate
    dim_candidate = df_clean[['First Name', 'Last Name', 'Email', 'Seniority', 'YOE']].drop_duplicates(subset=['Email']).reset_index(drop=True)
    dim_candidate.rename(columns={'First Name': 'First_Name', 'Last Name': 'Last_Name'}, inplace=True)
    dim_candidate['Candidate_SK'] = dim_candidate.index + 1
    
    # ==========================================
    # FACT TABLE CREATION
    # ==========================================
    
    # Merges to map natural data to Surrogate Keys (SK)
    fact_df = df_clean.merge(dim_location, on='Country', how='left')
    fact_df = fact_df.merge(dim_technology, left_on='Technology', right_on='Technology_Name', how='left')
    fact_df['Date_SK'] = fact_df['Application Date'].dt.strftime('%Y%m%d').astype(int)
    fact_df = fact_df.merge(dim_candidate[['Email', 'Candidate_SK']], on='Email', how='left')
    
    # Select columns for the Fact Table according to the defined Grain
    fact_applications = fact_df[[
        'Candidate_SK', 'Technology_SK', 'Location_SK', 'Date_SK', 
        'Code Challenge Score', 'Technical Interview Score', 'Is_Hired'
    ]].copy()
    
    # Standardize column names to match the SQL Warehouse schema
    fact_applications.rename(columns={
        'Code Challenge Score': 'Code_Challenge_Score',
        'Technical Interview Score': 'Technical_Interview_Score'
    }, inplace=True)
    
    fact_applications['Application_SK'] = fact_applications.index + 1
    
    print("Star Schema transformation completed successfully.")
    return dim_location, dim_technology, dim_date, dim_candidate, fact_applications