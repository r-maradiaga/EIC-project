
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_handler import fetch_data_as_dataframe_standardized

def get_final_df():
    try:
        customers = fetch_data_as_dataframe_standardized("SELECT customer_id, acquisition_channel FROM CUSTOMERS")
        customers_extra = fetch_data_as_dataframe_standardized("SELECT customer_id, acquisition_channel FROM CUSTOMERS_EXTRA")
        combined_customers = pd.concat([customers, customers_extra], ignore_index=True)
        combined_customers = combined_customers.drop_duplicates(subset=['customer_id'], keep='first')
        
        touchpoints = fetch_data_as_dataframe_standardized("SELECT touchpoint_id, customer_id, channel, converted_flag FROM CUSTOMER_TOUCHPOINTS")
        touchpoints_extra = fetch_data_as_dataframe_standardized("SELECT touchpoint_id, customer_id, channel, converted_flag FROM CUSTOMER_TOUCHPOINTS_EXTRA")
        combined_touchpoints = pd.concat([touchpoints, touchpoints_extra], ignore_index=True)
        combined_touchpoints = combined_touchpoints.drop_duplicates(subset=['touchpoint_id'], keep='first')
        
        spend = fetch_data_as_dataframe_standardized("SELECT spend_id, channel, spend_amount FROM MARKETING_SPEND")
        spend = spend.drop_duplicates(subset='spend_id')
         
        acquisition_summary = combined_customers['acquisition_channel'].value_counts().reset_index()
        acquisition_summary.columns = ['channel', 'customers_acquired']
         
        spend_summary = spend.groupby('channel', as_index=False).agg(total_direct_spend=('spend_amount', 'sum'))
        spend_summary.columns = ['channel', 'total_direct_spend']

        session_summary = combined_touchpoints.query("converted_flag == True")['channel'].value_counts().reset_index()
        session_summary.columns = ['channel', 'count']
        session_summary['count'] = session_summary['count'].astype(int)
         
        # Map acquisition channels to their corresponding transaction channels
        acquisition_to_touchpoint_mapping = {
            'Direct': ['Direct'],
            'Email': ['Email'], 
            'Facebook': ['Facebook'],
            'Google': ['Google'],
            'Instagram': ['Instagram'],
            'TikTok': ['TikTok'],
            'Referral': ['Walk-in', 'Direct'],  # Referral customers often convert in-store or direct
            'Social Media': ['Instagram', 'Facebook', 'TikTok', 'Walk-in']  # Social media maps to social platforms + store
        }
        
        # Calculate conversions by tracking acquired customers through any of their mapped channels
        converted_customer_summary = []
        
        for acq_channel, touchpoint_channels in acquisition_to_touchpoint_mapping.items():
            acquired_customer_ids = combined_customers[
                combined_customers['acquisition_channel'] == acq_channel
            ]['customer_id'].tolist()
            
            if acquired_customer_ids:
                converted_count = combined_touchpoints[
                    (combined_touchpoints['customer_id'].isin(acquired_customer_ids)) &
                    (combined_touchpoints['channel'].isin(touchpoint_channels)) &
                    (combined_touchpoints['converted_flag'] == True)
                ]['customer_id'].nunique()
            else:
                converted_count = 0
                
            converted_customer_summary.append({
                'channel': acq_channel,
                'converted_customers': converted_count
            })
        
        converted_customer_summary = pd.DataFrame(converted_customer_summary)

        # allocate indirect cost proportionally
        total_indirect = 10000
        session_summary['indirect_cost'] = (session_summary['count'] / session_summary['count'].sum()) * total_indirect
        
        merged_df = (
            acquisition_summary
            .merge(spend_summary, on='channel', how='outer')
            .merge(session_summary[['channel', 'indirect_cost']], on='channel', how='left')
            .merge(converted_customer_summary, on='channel', how='left')
            .fillna({'total_direct_spend': 0, 'indirect_cost': 0, 'converted_customers': 0})
        )
        
        # detailed indirect costs
        indirect_details = pd.DataFrame({
            'channel': ['Direct', 'Email', 'Facebook', 'Google', 'Instagram', 'Referral', 'Social Media', 'TikTok'],
            'staff_cost': [800, 400, 1200, 1800, 1500, 1000, 1100, 1000],
            'technology_cost': [700, 600, 1000, 1500, 1400, 800, 900, 1200],
            'returns_processing_cost': [500, 300, 800, 1000, 900, 600, 700, 1100]
        })

        # convert all cost columns to float before assigning final costs
        cost_columns = ['total_direct_spend', 'indirect_cost', 'staff_cost', 'technology_cost', 'returns_processing_cost']
        for col in cost_columns:
            if col in merged_df.columns:
                merged_df[col] = merged_df[col].astype(float)

        # merge and calculate final costs
        final_df = (
            merged_df
            .merge(indirect_details, on='channel', how='left')
            .fillna({'staff_cost': 0, 'technology_cost': 0, 'returns_processing_cost': 0})
            .assign(
                true_total_cost=lambda df: df['total_direct_spend'] + df['indirect_cost'] + df['staff_cost'] + df['technology_cost'] + df['returns_processing_cost'],
                true_cac=lambda df: df.apply(lambda row: row['true_total_cost'] if row['converted_customers'] == 0 else row['true_total_cost'] / row['converted_customers'], axis=1)
            )
        )
        return final_df
    
    except Exception as e:
        print(f"Error in get_final_df: {e}")
        return None

# For testing
if __name__ == "__main__":
    try:
        df = get_final_df()
        if df is not None:
            print("Customer Acquisition Cost Analysis:")
            print(df)
            print(f"\nShape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
        else:
            print("Failed to generate analysis")
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
