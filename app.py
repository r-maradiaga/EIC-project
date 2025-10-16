import streamlit as st
import plotly.express as px
import pandas as pd 

st.write("Plotly test to make sure package works with Streamlit")

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 11, 12, 13, 14],
    'color_group': ['A', 'B', 'A', 'C', 'B']
})
fig = px.scatter(df, x='x', y='y', color='color_group')
st.plotly_chart(fig)