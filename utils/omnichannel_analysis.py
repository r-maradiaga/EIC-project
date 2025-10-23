import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_handler import get_customers_df, get_transactions_df

def get_omnichannel_analysis():
    """
    Analyze customer lifetime value by omnichannel vs single-channel usage.
    
    Returns:
        tuple: (summary_df, detailed_df, bar_chart_fig, box_plot_fig)
    """
    customers = get_customers_df()
    tx = get_transactions_df()
     
    # sort channels using lowercase column names
    tx['channel'] = tx['channel'].str.strip().str.lower()
    customers = customers.drop_duplicates(subset=['customer_id'])
    customers = customers[customers['lifetime_value'].notna()]
     
    channel_counts = tx.groupby('customer_id')['channel'].nunique().reset_index()
    channel_counts.columns = ['customer_id', 'channels_used']
     
    df = customers.merge(channel_counts, on='customer_id', how='left')
    df['channels_used'] = df['channels_used'].fillna(0).astype(int)
    df = df[df['channels_used'] >= 1]
     
    # omnichannel vs single channel
    df['cohort'] = df['channels_used'].apply(lambda x: 'Omnichannel' if x >= 2 else 'Single-channel')
     
    summary = df.groupby('cohort')['lifetime_value'].agg(['count', 'mean', 'median', lambda x: x.quantile(0.9)])
    summary.columns = ['n_customers', 'mean_clv', 'median_clv', 'p90_clv']
     
    fig_bar = go.Figure(data=[
        go.Bar(name='Mean CLV', x=summary.index, y=summary['mean_clv']),
        go.Bar(name='Median CLV', x=summary.index, y=summary['median_clv'])
    ])
    fig_bar.update_layout(
        title='Mean vs Median CLV by Cohort',
        xaxis_title='Cohort',
        yaxis_title='CLV',
        barmode='group',
        width=800,
        height=500
    )

    fig_box = px.box(df, x='cohort', y='lifetime_value', title='CLV Distribution by Cohort')
    fig_box.update_layout(xaxis_title='Cohort', yaxis_title='CLV', width=800, height=500)
    
    return summary, df, fig_bar, fig_box

if __name__ == "__main__":
    summary, df, fig_bar, fig_box = get_omnichannel_analysis()
    print("Summary Statistics:")
    print(summary)