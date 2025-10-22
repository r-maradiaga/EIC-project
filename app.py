import streamlit as st

pages = {
    "Business Analytics ": [
        st.Page("pages/customer_segment_page.py", title="Customer Segment"), # potential security issue
        st.Page("pages/onmichannel_analysis_page.py", title="Omnichannel Analysis"),
        st.Page("pages/true_acquisition_cost_page.py", title="True Acquisition Cost"),
    ],
    # "Resources": [
    #     st.Page("learn.py", title="Learn about us"),
    #     st.Page("trial.py", title="Try it out"),
    # ],
}

pg = st.navigation(pages)
pg.run()
