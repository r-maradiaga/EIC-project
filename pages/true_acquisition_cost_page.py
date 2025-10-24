import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.true_customer_acquisition_cost import get_final_df

st.header("True Customer Acquisition Cost")
st.write("Comprehensive analysis of customer acquisition costs including direct spend, indirect costs, and true CAC by channel")

try:
    acquisition_cost_dataframe = get_final_df()
    if acquisition_cost_dataframe is not None and not acquisition_cost_dataframe.empty:
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_cost = acquisition_cost_dataframe['true_total_cost'].sum()
            st.metric("Total Acquisition Cost", f"${total_cost:,.0f}")
        with col2:
            avg_cac = acquisition_cost_dataframe['true_cac'].mean()
            st.metric("Average CAC", f"${avg_cac:,.2f}")
        with col3:
            total_customers = acquisition_cost_dataframe['customers_acquired'].sum()
            st.metric("Total Customers", f"{total_customers:,}")
        with col4:
            number_of_converted_customers = acquisition_cost_dataframe['converted_customers'].sum()
            st.metric("Converted Customers", f"{number_of_converted_customers:,.0f}")
            

        tab1, tab2, tab3 = st.tabs(["Cost by Channel", "True Customer Acquisition Cost by Channel", "Customers Acquired by Channel"])

        with tab1:
            cost_breakdown_fig = go.Figure()
            
            cost_breakdown_fig.add_trace(go.Bar(
                name='Direct Spend',
                x=acquisition_cost_dataframe['channel'],
                y=acquisition_cost_dataframe['total_direct_spend']
            ))
            cost_breakdown_fig.add_trace(go.Bar(
                name='Staff Cost',
                x=acquisition_cost_dataframe['channel'],
                y=acquisition_cost_dataframe['staff_cost']
            ))
            cost_breakdown_fig.add_trace(go.Bar(
                name='Technology Cost',
                x=acquisition_cost_dataframe['channel'],
                y=acquisition_cost_dataframe['technology_cost']
            ))
            cost_breakdown_fig.add_trace(go.Bar(
                name='Returns Processing',
                x=acquisition_cost_dataframe['channel'],
                y=acquisition_cost_dataframe['returns_processing_cost']
            ))
            cost_breakdown_fig.add_trace(go.Bar(
                name='Indirect Cost',
                x=acquisition_cost_dataframe['channel'],
                y=acquisition_cost_dataframe['indirect_cost']
            ))
            
            cost_breakdown_fig.update_layout(
                barmode='stack',
                xaxis_title='Channel',
                yaxis_title='Cost ($)',
                height=500
            )
            st.plotly_chart(cost_breakdown_fig, use_container_width=True)
        
        with tab2:
            cac_fig = px.bar(
                acquisition_cost_dataframe,
                x='channel',
                y='true_cac',
                labels={'true_cac': 'True CAC ($)', 'channel': 'Channel'}
            )
            cac_fig.update_layout(height=400)
            st.plotly_chart(cac_fig, use_container_width=True)
            
        with tab3:
            customers_fig = px.bar(
                acquisition_cost_dataframe,
                x='channel',
                y='customers_acquired',
                labels={'customers_acquired': 'Customers', 'channel': 'Channel'}
            )
            customers_fig.update_layout(height=400)
            st.plotly_chart(customers_fig, use_container_width=True)
        
        with st.expander("Acquisition cost table"):
            display_df = acquisition_cost_dataframe.copy()
            money_columns = ['total_direct_spend', 'indirect_cost', 'staff_cost', 'technology_cost', 'returns_processing_cost', 'true_total_cost', 'true_cac']
            for col in money_columns:
                if col in display_df.columns:
                    display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(display_df, use_container_width=True)
            
except Exception as error:
    st.error(f"Error loading customer acquisition cost data: {error}")
    st.write("Please check your data source and try again.")