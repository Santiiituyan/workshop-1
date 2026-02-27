import pandas as pd
from sqlalchemy import create_engine

def load_data(dim_location, dim_technology, dim_date, dim_candidate, fact_applications, db_url):
    """
    Loads the transformed DataFrames into the SQL Data Warehouse.
    """
    print(f"Connecting to the database...")
    
    try:
        # Create the connection engine using SQLAlchemy
        engine = create_engine(db_url)
        
        # 1. Load Dimensions (if_exists='append' adds data to the pre-created tables)
        # index=False ensures Pandas' internal index is not inserted as a column
        print("Loading Dim_Location...")
        dim_location.to_sql('Dim_Location', con=engine, if_exists='append', index=False)
        
        print("Loading Dim_Technology...")
        dim_technology.to_sql('Dim_Technology', con=engine, if_exists='append', index=False)
        
        print("Loading Dim_Date...")
        dim_date.to_sql('Dim_Date', con=engine, if_exists='append', index=False)
        
        print("Loading Dim_Candidate...")
        dim_candidate.to_sql('Dim_Candidate', con=engine, if_exists='append', index=False)
        
        # 2. Load the Fact Table
        # This is loaded last to maintain referential integrity
        print("Loading Fact_Applications...")
        fact_applications.to_sql('Fact_Applications', con=engine, if_exists='append', index=False)
        
        print("Load successful! All data has been migrated to the Data Warehouse.")
        
    except Exception as e:
        print(f"Critical error during the load phase: {e}")