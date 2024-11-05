import pandas as pd
from pandas_profiling import ProfileReport
import sweetviz as sv
import os

def load_file(file):
    try:
        # Check the file type based on file extension
        if file.filename.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            data = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        
        # Basic validation
        if data.empty:
            raise ValueError("Uploaded file is empty.")
        
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None