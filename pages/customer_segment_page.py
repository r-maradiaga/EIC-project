import streamlit as st
from utils.customer_segment import get_customer_segment_analysis

try:
    segment_analysis_results = get_customer_segment_analysis()
    
    total_customers_across_segments = segment_analysis_results['segment_counts']['customer_count'].sum()
    
except Exception as error:
    st.error(f"Error loading customer segment analysis: {error}")
    st.write("Please check your database connection and data availability.")

st.header(f"Customer Segment Analysis (N={total_customers_across_segments})")
st.write("Analysis of customer demographics and lifetime value across different customer segments and acquisition channels")

channel_insights = segment_analysis_results['channel_insights']

st.subheader("Lifetime Value by Customer Segment")
st.write("Analysis of total and average lifetime value across customer segments")

tab1, tab2 = st.tabs(["Bar Chart", "Table"])
with tab1:
    st.plotly_chart(segment_analysis_results['ltv_bar_chart'])

with tab2:
    st.dataframe(segment_analysis_results['ltv_summary'])

st.subheader("Customer Count by Segment and Channel")

st.plotly_chart(segment_analysis_results['count_chart'])

st.subheader("Top Performing Channels by Segment")

tab1, tab2 = st.tabs(["Highest Customer Count", "Overall Channel Ranking"])

with tab1:
    st.write("**Channels with Most Customers by Segment:**")
    display_df = channel_insights['top_channels_by_count'].copy()
    display_df['customer_count'] = display_df['customer_count'].apply(lambda x: f"{x:,}")
    st.dataframe(display_df, use_container_width=True)

with tab2:
    st.write("**Overall Channel Performance Ranking:**")
    display_df = channel_insights['channel_performance'].copy()
    display_df['avg_ltv'] = display_df['avg_ltv'].apply(lambda x: f"${x:,.2f}")
    display_df['total_customers'] = display_df['total_customers'].apply(lambda x: f"{x:,}")
    st.dataframe(display_df, use_container_width=True)
