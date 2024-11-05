import pandas as pd
from pandas_profiling import ProfileReport
import sweetviz as sv
import os
import matplotlib.pyplot as plt
import seaborn as sns

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
    
def display_data_info(data):
    """
    Display basic information about the dataset, including shape,
    data types, summary statistics, and missing value count.
    """
    print("1. Basic Dataset Information")
    print("-" * 30)
    print(f"Shape of data: {data.shape}")
    print("\nData Types of Columns:")
    print(data.dtypes)
    print("\nMissing Values in Each Column:")
    print(data.isnull().sum())
    print("\nStatistical Summary:")
    print(data.describe(include='all'))
    print("-" * 30)
    print("\nData Information Summary:")
    data.info()
    print("-" * 30)

def clean_data(data):
    """
    Perform comprehensive data cleaning on the dataset.
    This includes handling missing values, removing duplicates,
    handling and plotting outliers, and basic data type conversion.
    """
    # Display initial data info
    display_data_info(data)

    # 1. Handle Missing Values
    # - Fill numeric columns with the mean
    # - Fill categorical columns with the mode
    for column in data.columns:
        if data[column].isnull().sum() > 0:  # Only apply if there are missing values
            if data[column].dtype in ['float64', 'int64']:
                data[column].fillna(data[column].mean(), inplace=True)
            elif data[column].dtype == 'object':
                data[column].fillna(data[column].mode()[0], inplace=True)

    # 2. Remove Duplicates
    data = data.drop_duplicates()

    # 3. Outlier Detection, Plotting, and Treatment
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    data_cleaned = data.copy()  # Create a copy for cleaning
    
    for col in numeric_cols:
        # Calculate IQR
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Plotting the distribution before and after outlier removal
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f'Outlier Treatment for {col}', fontsize=16)

        # Before outlier treatment
        sns.boxplot(x=data[col], ax=axes[0], color="skyblue")
        axes[0].set_title("Before Outlier Treatment")
        axes[0].set_xlabel(col)
        
        # Clipping the outliers in the cleaned data
        data_cleaned[col] = np.clip(data[col], lower_bound, upper_bound)
        
        # After outlier treatment
        sns.boxplot(x=data_cleaned[col], ax=axes[1], color="salmon")
        axes[1].set_title("After Outlier Treatment")
        axes[1].set_xlabel(col)

        plt.show()

    # 4. Data Type Conversion
    # Convert object types to 'category' to save memory
    for col in data_cleaned.select_dtypes(include=['object']).columns:
        data_cleaned[col] = data_cleaned[col].astype('category')

    return data_cleaned