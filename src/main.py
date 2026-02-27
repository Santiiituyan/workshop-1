import os
from dotenv import load_dotenv

# Import functions from our modular pipeline files
from extract import extract_data
from transform import transform_to_star_schema
from load import load_data

def main():
    print("=== STARTING ETL PIPELINE ===")
    
    # ==========================================
    # CONFIGURATION & CREDENTIALS
    # ==========================================
    # Load environment variables from the .env file for security
    load_dotenv()
    
    # Retrieve database credentials
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD", "") # Default to empty string if no password is set
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    # Construct the SQLAlchemy connection URL (MySQL)
    db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Relative path to the raw CSV data file
    file_path = 'C:/Users/USUARIO/Desktop/etl_2026_01/Workshop/data/raw/candidates.csv'
    
    # ==========================================
    # 1. EXTRACT
    # ==========================================
    df_raw = extract_data(file_path)
    
    if df_raw is not None:
        # ==========================================
        # 2. TRANSFORM
        # ==========================================
        print("\n--- Starting Transformation Phase ---")
        dim_loc, dim_tech, dim_date, dim_cand, fact_app = transform_to_star_schema(df_raw)
        
        # ==========================================
        # 3. LOAD
        # ==========================================
        print("\n--- Starting MySQL Load Phase ---")
        # Load the Star Schema components into the Data Warehouse
        load_data(dim_loc, dim_tech, dim_date, dim_cand, fact_app, db_url)
        
        print("\n=== ETL PIPELINE COMPLETED SUCCESSFULLY ===")
    else:
        print("\nProcess aborted: Data extraction failed.")

if __name__ == "__main__":
    main()