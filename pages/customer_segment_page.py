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

st.subheader("Lifetime Value by Customer Segment")
st.write("Analysis of total and average lifetime value across customer segments")

tab1, tab2 = st.tabs(["Bar Chart", "Table"])
with tab1:
    st.plotly_chart(segment_analysis_results['ltv_bar_chart'])

with tab2:
    st.dataframe(segment_analysis_results['ltv_summary'])

# Age Analysis
st.subheader("Average Age by Segment and Channel")

st.plotly_chart(segment_analysis_results['age_heatmap'])

with st.expander("Table of Age Data Summary"):
    st.dataframe(segment_analysis_results['age_pivot'])
