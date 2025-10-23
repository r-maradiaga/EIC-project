import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_handler import get_customers_df

def get_age_by_segment_and_channel():
    customers = get_customers_df()
    
    pivot_table = customers.pivot_table(
        index='customer_segment', 
        columns='acquisition_channel', 
        values='age', 
        aggfunc='mean'
    )
    
    age_data_melted = pivot_table.reset_index().melt(
        id_vars='customer_segment',
        var_name='acquisition_channel', 
        value_name='average_age'
    ).dropna()
    
    segment_order = ['Dormant', 'New', 'Occasional', 'Frequent', 'High-Value']
    
    grouped_bar_figure = px.bar(
        age_data_melted,
        x='customer_segment',
        y='average_age',
        color='acquisition_channel',
        labels={
            'average_age': 'Average Age (Years)',
            'customer_segment': 'Customer Segment',
            'acquisition_channel': 'Acquisition Channel'
        },
        barmode='group',
        category_orders={'customer_segment': segment_order}
    )
    
    grouped_bar_figure.update_layout(
        width=900,
        height=600,
        xaxis_title='Customer Segment',
        yaxis_title='Average Age (Years)',
        legend_title='Acquisition Channel',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=100, b=80, l=80, r=80),
        xaxis=dict(
            tickangle=0,
            categoryorder='array',
            categoryarray=segment_order
        )
    )
    
    # Add text annotations directly to bars instead of separate traces
    grouped_bar_figure.update_traces(
        texttemplate='%{y:.1f}',
        textposition='outside',
        textfont_size=10
    )
    
    return pivot_table, grouped_bar_figure

def get_lifetime_value_by_segment():
    customers = get_customers_df()
    
    # Summary of lifetime value by customer segment
    summary = customers.groupby('customer_segment')['lifetime_value'].agg([
        'sum', 'mean', 'count'
    ]).reset_index()
    summary.columns = ['customer_segment', 'total_ltv', 'avg_ltv', 'customer_count']
    
    segment_order = ['Dormant', 'New', 'Occasional', 'Frequent', 'High-Value']
    
    # Reorder the summary DataFrame to match the order
    summary['customer_segment'] = pd.Categorical(summary['customer_segment'], categories=segment_order, ordered=True)
    summary = summary.sort_values('customer_segment').reset_index(drop=True)
    
    fig = px.bar(
        summary,
        x='customer_segment',
        y='total_ltv',
        title='Total Lifetime Value by Customer Segment',
        labels={
            'total_ltv': 'Total Lifetime Value',
            'customer_segment': 'Customer Segment'
        },
        category_orders={'customer_segment': segment_order}
    )
    
    fig.update_layout(width=800, height=500, showlegend=False)
    
    for i, row in summary.iterrows():
        fig.add_annotation(
            x=row['customer_segment'],
            y=row['total_ltv'],
            text=f"${row['total_ltv']:,.0f}",
            showarrow=False,
            yshift=10
        )
    
    return summary, fig

def get_segment_counts():
    customers = get_customers_df()
    
    segment_counts = customers['customer_segment'].value_counts().reset_index()
    segment_counts.columns = ['customer_segment', 'customer_count']
    
    segment_order = ['Dormant', 'New', 'Occasional', 'Frequent', 'High-Value']
    
    # Reorder the counts DataFrame to match the custom order
    segment_counts['customer_segment'] = pd.Categorical(segment_counts['customer_segment'], categories=segment_order, ordered=True)
    segment_counts = segment_counts.sort_values('customer_segment').reset_index(drop=True)
    
    return segment_counts

def get_customer_segment_analysis():
    age_pivot, age_heatmap = get_age_by_segment_and_channel()
    ltv_summary, ltv_bar_chart = get_lifetime_value_by_segment()
    segment_counts = get_segment_counts()
    
    return {
        'age_pivot': age_pivot,
        'age_heatmap': age_heatmap,
        'ltv_summary': ltv_summary,
        'ltv_bar_chart': ltv_bar_chart,
        'segment_counts': segment_counts
    }

# For testing
if __name__ == "__main__":
    try:
        print("Testing customer segment analysis...")
        
        # Test age analysis
        age_pivot, age_fig = get_age_by_segment_and_channel()
        print("Age Analysis:")
        print(age_pivot)
        age_fig.show()
        
        # Test lifetime value analysis
        ltv_summary, ltv_fig = get_lifetime_value_by_segment()
        print("\nLifetime Value Analysis:")
        print(ltv_summary)
        ltv_fig.show()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()