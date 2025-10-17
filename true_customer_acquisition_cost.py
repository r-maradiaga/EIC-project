
import pandas as pd
import data_retriever

# Helper to convert fetch_data results to DataFrame
def fetch_df(query, columns):
    data = data_retriever.fetch_data(query)
    return pd.DataFrame(data, columns=columns)

# SQL queries for each dataset
customers_query = "SELECT customer_id, acquisition_channel FROM CUSTOMERS"
spend_query = "SELECT spend_id, channel, spend_amount FROM MARKETING_SPEND"
touchpoints_query = "SELECT touchpoint_id, customer_id, channel, converted_flag FROM CUSTOMER_TOUCHPOINTS"
#Sdata_retriever.close_connection()

# Fetch data from Snowflake
customers = fetch_df(customers_query, ["customer_id", "acquisition_channel"])
spend = fetch_df(spend_query, ["spend_id", "channel", "spend_amount"])
touchpoints = fetch_df(touchpoints_query, ["touchpoint_id", "customer_id", "channel", "converted_flag"])

spend = spend.drop_duplicates(subset='spend_id')
touchpoints = touchpoints.drop_duplicates(subset='touchpoint_id')
 
# customer acquisition counts
acquisition_summary = (
    customers['acquisition_channel']
    .value_counts()
    .reset_index()
)
acquisition_summary.columns = ['channel', 'customers_acquired']
 
# direct spend aggregation
spend_summary = (
    spend.groupby('channel', as_index=False)
    .agg(total_direct_spend=('spend_amount', 'sum'))
)
spend_summary.columns = ['channel', 'total_direct_spend']
 
# conversion session counts
session_summary = (
    touchpoints.query("converted_flag == True")['channel']
    .value_counts()
    .reset_index()
)
session_summary.columns = ['channel', 'count']
session_summary['count'] = session_summary['count'].astype(int)
 
# converted customers
converted_customer_summary = (
    touchpoints.query("converted_flag == True").groupby('channel', as_index=False)
    .agg(converted_customers=('customer_id', 'nunique'))
)
converted_customer_summary.columns = ['channel', 'converted_customers']
 
# allocate indirect cost proportionally
total_indirect = 10000
session_summary['indirect_cost'] = (
    session_summary['count'] / session_summary['count'].sum()
) * total_indirect
 
def get_final_df():
    # merge all summaries
    merged_df = (
        acquisition_summary
        .merge(spend_summary, on='channel', how='outer')
        .merge(session_summary[['channel', 'indirect_cost']], on='channel', how='left')
        .merge(converted_customer_summary, on='channel', how='left')
        .fillna({'total_direct_spend': 0, 'indirect_cost': 0, 'converted_customers': 0})
    )
    
    # detailed indirect costs
    indirect_details = pd.DataFrame({
        'channel': ['Email', 'Facebook', 'Google', 'Instagram', 'TikTok', 'Walk-in', 'Direct'],
        'staff_cost': [400, 1200, 1800, 1500, 1000, 2500, 800],
        'technology_cost': [600, 1000, 1500, 1400, 1200, 400, 700],
        'returns_processing_cost': [300, 800, 1000, 900, 1100, 300, 500]
    })

    # convert all cost columns to float before assigning final costs
    cost_columns = [
        'total_direct_spend', 'indirect_cost', 'staff_cost',
        'technology_cost', 'returns_processing_cost'
    ]
    for col in cost_columns:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].astype(float)

    # merge and calculate final costs
    final_df = (
        merged_df
        .merge(indirect_details, on='channel', how='left')
        .fillna({'staff_cost': 0, 'technology_cost': 0, 'returns_processing_cost': 0})
        .assign(
            true_total_cost=lambda df: df['total_direct_spend'] + df['indirect_cost'] +
                                    df['staff_cost'] + df['technology_cost'] + df['returns_processing_cost'],
            true_cac=lambda df: df.apply(
                lambda row: row['true_total_cost'] if row['converted_customers'] == 0
                else row['true_total_cost'] / row['converted_customers'], axis=1
            )
        )
    )
    return final_df

# if __name__ == "__main__":
#     df = get_final_df()
#     print(df)