import snowflake.connector

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
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()

def close_connection():
    conn.close()


if __name__ == "__main__":
    sample_query = "SELECT * FROM CUSTOMERS LIMIT 10"
    data = fetch_data(sample_query)
    for row in data:
        print(row)

