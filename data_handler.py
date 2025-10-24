import snowflake.connector
import pandas as pd
import decimal
from dotenv import load_dotenv

import os

load_dotenv()

snowflake_user = os.getenv("username")
snowflake_password = os.getenv("password")
snowflake_account = os.getenv("account")
snowflake_warehouse = os.getenv("warehouse")
snowflake_database = os.getenv("database")
snowflake_schema = os.getenv("schema")

conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema
)

def fetch_data(query):
    """Returns raw tuples"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()

def fetch_data_as_dataframe(query):
    """Fetch data and return as pandas DataFrame with proper column names"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]
        # Fetch all results
        results = cursor.fetchall()
        # Create DataFrame with proper column names
        df = pd.DataFrame(results, columns=columns)
        return df
    finally:
        cursor.close()

def convert_snowflake_types(df):
    """
    Convert Snowflake-specific data types in dataframe to pandas-compatible types.
    """

    df_converted = df.copy()
    
    for col in df_converted.columns:
        if df_converted[col].dtype == 'object':
            # Get a sample of non-null values to check type
            sample_values = df_converted[col].dropna()
            if len(sample_values) > 0:
                first_value = sample_values.iloc[0]
                
                # Convert decimal.Decimal to float
                if isinstance(first_value, decimal.Decimal):
                    df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
                
                elif isinstance(first_value, str):
                    # Only try to convert if it looks like a common date format
                    if (len(str(first_value)) >= 8 and 
                        any(char in str(first_value) for char in ['/', '-']) and 
                        any(char.isdigit() for char in str(first_value))):
                        try:
                            df_converted[col] = pd.to_datetime(df_converted[col], errors='coerce')
                        except:
                            pass  # Keep as string if conversion fails
    
    return df_converted

def standardize_column_names(df):
    """
    Standardize Snowflake column names to lowercase for easier analysis.
    Also converts decimal columns to float for pandas compatibility.
    
    Args:
        df (pd.DataFrame): DataFrame with Snowflake uppercase column names
        
    Returns:
        pd.DataFrame: DataFrame with lowercase column names and proper data types
    """
    df_standardized = df.copy()
    
    # Convert all column names to lowercase
    df_standardized.columns = df_standardized.columns.str.lower()
    
    # Convert Snowflake data types to types usable in pandas
    df_standardized = convert_snowflake_types(df_standardized)
    
    return df_standardized

def fetch_data_as_dataframe_standardized(query):
    """
    Fetch data and return as pandas DataFrame with standardized (lowercase) column names.
    This is the recommended function to use for analysis.
    """
    df = fetch_data_as_dataframe(query)
    return standardize_column_names(df)

def fetch_data_as_json(query):
    """Fetch data and return as JSON string"""
    df = fetch_data_as_dataframe(query)
    return df.to_json(orient='records')

def fetch_data_as_dict(query):
    """Fetch data and return as list of dictionaries"""
    df = fetch_data_as_dataframe(query)
    return df.to_dict('records')

def get_customers_df():
    """Get customers data as DataFrame with standardized column names - combines CUSTOMERS and CUSTOMERS_EXTRA"""
    customers = fetch_data_as_dataframe_standardized("SELECT * FROM CUSTOMERS")
    customers_extra = fetch_data_as_dataframe_standardized("SELECT * FROM CUSTOMERS_EXTRA")
    
    combined_customers = pd.concat([customers, customers_extra], ignore_index=True)
    
    combined_customers = combined_customers.drop_duplicates(subset=['customer_id'], keep='first')
    
    return combined_customers

def get_transactions_df():
    """Get transactions data as DataFrame with standardized column names - combines TRANSACTIONS and TRANSACTIONS_EXTRA"""
    transactions = fetch_data_as_dataframe_standardized("SELECT * FROM TRANSACTIONS")
    transactions_extra = fetch_data_as_dataframe_standardized("SELECT * FROM TRANSACTIONS_EXTRA")
    
    combined_transactions = pd.concat([transactions, transactions_extra], ignore_index=True)
    
    if 'transaction_id' in combined_transactions.columns:
        combined_transactions = combined_transactions.drop_duplicates(subset=['transaction_id'], keep='first')
    
    return combined_transactions

def close_connection():
    conn.close()


if __name__ == "__main__":
    # For testing
    print("Testing raw data fetch:")
    sample_query = "SELECT * FROM CUSTOMERS_EXTRA LIMIT 5"
    raw_data = fetch_data(sample_query)
    print(f"Raw data (first row): {raw_data[0] if raw_data else 'No data'}")
    
    print("\nTesting DataFrame fetch (original uppercase):")
    df_original = fetch_data_as_dataframe(sample_query)
    print(f"Original DataFrame columns: {df_original.columns.tolist()}")
    
    print("\nTesting DataFrame fetch (standardized lowercase):")
    df_standardized = fetch_data_as_dataframe_standardized(sample_query)
    print(f"Standardized DataFrame columns: {df_standardized.columns.tolist()}")
    
    print("\nTesting convenience functions:")
    try:
        customers_df = get_customers_df()
        print(f"Customers DataFrame shape: {customers_df.shape}")
        print(f"Customers columns (standardized): {customers_df.columns.tolist()}")
        
        transactions_df = get_transactions_df()
        print(f"Transactions DataFrame shape: {transactions_df.shape}")
        print(f"Transactions columns (standardized): {transactions_df.columns.tolist()}")
    except Exception as e:
        print(f"Error fetching data: {e}")

