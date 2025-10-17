import streamlit as st
import plotly.express as px
import pandas as pd 
from true_customer_acquisition_cost import get_final_df

st.write("True customer acquisition cost")
st.write("Based on indirect costs of $10,000 allocated proportionally by converting sessions")
df = get_final_df()
st.dataframe(df)