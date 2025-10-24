import streamlit as st

pages = {
    "Business Analytics ": [
        st.Page("pages/customer_segment_page.py", title="Customer Segment Analysis"),
        st.Page("pages/onmichannel_analysis_page.py", title="Customer Channel Analysis"),
        st.Page("pages/true_acquisition_cost_page.py", title="True Acquisition Cost"),
    ],
}

pg = st.navigation(pages)
pg.run()
