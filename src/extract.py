import pandas as pd

def extract_data(file_path):
    """
    Extracts raw data from the source CSV file.
    """
    print(f"Starting data extraction from: {file_path}")
    try:
        # The source file uses ';' as a delimiter as previously identified
        df = pd.read_csv(file_path, sep=';')
        print(f"Extraction successful! {len(df)} records were loaded.")
        return df
    except Exception as e:
        print(f"Error during data extraction: {e}")
        return None