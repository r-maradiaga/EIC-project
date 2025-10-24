import streamlit as st
from utils.omnichannel_analysis import get_omnichannel_analysis

st.header("Omnichannel vs Single-Channel Analysis")
st.write("Analysis of customer lifetime value comparing omnichannel customers (using 2+ channels) vs single-channel customers")

try:
    # Get the analysis results (summary, detailed_df, bar_chart, box_plot)
    omnichannel_summary, detailed_customer_dataframe, bar_chart_figure, box_plot_figure = get_omnichannel_analysis()
    
    st.subheader("Summary Statistics")
    st.dataframe(omnichannel_summary)
    
    # Calculate and display insights
    if len(omnichannel_summary) >= 2:
        if 'Omnichannel' in omnichannel_summary.index and 'Single-channel' in omnichannel_summary.index:
            omnichannel_mean_clv = omnichannel_summary.loc['Omnichannel', 'mean_clv']
            single_channel_mean_clv = omnichannel_summary.loc['Single-channel', 'mean_clv']
            
            if omnichannel_mean_clv > single_channel_mean_clv:
                clv_improvement_percentage = ((omnichannel_mean_clv - single_channel_mean_clv) / single_channel_mean_clv) * 100
                st.badge(f"Omnichannel customers have {clv_improvement_percentage:.1f}% higher average lifetime value")
    
    tab1, tab2 = st.tabs(["CLV Comparison (Bar chart)", "CLV Distribution (Box plot)"])

    with tab1:
        st.subheader("Customer Lifetime Value Comparison")
        st.plotly_chart(bar_chart_figure, use_container_width=True)
    
    with tab2:
        st.subheader("Customer Lifetime Value Distribution")
        st.plotly_chart(box_plot_figure, use_container_width=True)
    
    # Detailed data in expandable section
    with st.expander("View Detailed Customer Data"):
        st.dataframe(detailed_customer_dataframe, use_container_width=True)
        
except Exception as error:
    st.error(f"Error loading omnichannel analysis: {error}")
    st.write("Please check your database connection and data availability.")
    
    # Show debug information
    with st.expander("Debug Information"):
        import traceback
        st.code(traceback.format_exc())