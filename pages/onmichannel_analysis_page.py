import streamlit as st
from omnichannel_analysis import get_omnichannel_analysis

st.header("Omnichannel vs Single-Channel Analysis")
st.write("Analysis of customer lifetime value comparing omnichannel customers (using 2+ channels) vs single-channel customers")

try:
    omnichannel_summary, detailed_customer_dataframe, bar_chart_figure, box_plot_figure = get_omnichannel_analysis()
    
    st.subheader("Summary Statistics")
    st.dataframe(omnichannel_summary)
    
    # insights
    if len(omnichannel_summary) >= 2:
        omnichannel_mean_clv = omnichannel_summary.loc['Omnichannel', 'mean_clv'] if 'Omnichannel' in omnichannel_summary.index else 0
        single_channel_mean_clv = omnichannel_summary.loc['Single-channel', 'mean_clv'] if 'Single-channel' in omnichannel_summary.index else 0
        
        if omnichannel_mean_clv > single_channel_mean_clv:
            clv_improvement_percentage = ((omnichannel_mean_clv - single_channel_mean_clv) / single_channel_mean_clv) * 100
            st.success(f"Omnichannel customers have {clv_improvement_percentage:.1f}% higher average lifetime value")
        
    st.subheader("Customer Lifetime Value Comparison")
    st.plotly_chart(bar_chart_figure, use_container_width=True)
    
    st.subheader("Customer Lifetime Value Distribution")
    st.plotly_chart(box_plot_figure, use_container_width=True)
    
    with st.expander("View Detailed Customer Data"):
        st.dataframe(detailed_customer_dataframe)
        
except Exception as error:
    st.error(f"Error loading omnichannel analysis: {error}")
    st.write("Please check your database connection and data availability.")