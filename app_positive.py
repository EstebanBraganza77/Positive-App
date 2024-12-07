import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
import streamlit as st

warnings.filterwarnings('ignore')
data = pd.read_csv('https://olympus.mygreatlearning.com/courses/96080/files/11055029/download?verifier=ECNvbt1T3Pqlektc0L4EeablXmlQ9wquu2OsZFGp&wrap=1')
data['Sales'] = data['Bottles.Sold'] * data['State.Bottle.Retail']

# --- Dashboard with Streamlit ---

st.set_page_config(
    page_title="Iowa top Alcohol products",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

    
st.header('Iowa top Alcohol products 🍾', divider= 'rainbow')
col = st.columns(4, gap='medium')


# Left Column: Overview Metrics

def format_large_numbers(number):
    if number >= 1_000_000_000:
        return f"{number/1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return str(number)
    
st.markdown("""
<style>
    .css-1v3fvcr {
        font-size: 30px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
# Now use it in your metrics
total_sales = data['Sales'].sum()
total_bottles = data['Bottles.Sold'].sum()
avg_sales_per_bottle = total_sales / total_bottles
top_category = data.groupby('Category.Name')['Bottles.Sold'].sum().idxmax().capitalize()

col[0].metric("Total Sales", format_large_numbers(total_sales))
col[1].metric("Total Bottles Sold", format_large_numbers(total_bottles))
col[2].metric("Average Sales/Bottle", f"${avg_sales_per_bottle:.2f}")
col[3].metric("Top Category", top_category)


col = st.columns(3, gap='medium')
# Top Products
with col[0]:
    st.header("Top Selling Products")
    top_products = data.groupby('Category.Name')['Bottles.Sold'].sum().sort_values(ascending=False).head(15).reset_index()

    # Create the bar chart
    fig = px.bar(
        top_products,
        y='Category.Name',  # Use the column directly from the DataFrame
        x='Bottles.Sold',
        labels={'x': 'Bottles Sold', 'y': 'Type of alcohol'}, 
        #color_discrete_sequence=px.colors.qualitative.Pastel, 
        color='Bottles.Sold',
        log_x=True
    )

    # Reverse the y-axis to show the largest values at the top
    fig.update_layout(
        yaxis=dict(
            autorange="reversed",  # Reverse the order of the y-axis
            tickfont=dict(size=10)  # Adjust font size for readability
        ),
        xaxis_title='', 
        yaxis_title='',
        #margin=dict(l=300, r= 100)  # Adjust left margin for long labels
    )
    st.plotly_chart(fig)

with col[1]:
    st.header("Geographic Sales Distribution top Counties")
    county_sales = data.groupby('County')['Sales'].sum().reset_index().sort_values('Sales',ascending=False).head(10)
    fig = px.bar(
        county_sales,
        x='County',
        y='Sales',
        labels={"County": "County", "Sales": "Sales ($)"},
        color='Sales',
        #color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(xaxis_tickangle=-45)  # Rotate labels if necessary
    st.plotly_chart(fig)

# Right Column: Filters and Tables
with col[2]:

    # Filter the data for 'AMERICAN VODKAS' category
    filtered_data = data[data['Category.Name'].isin(['AMERICAN VODKAS'])]

    # Group by store name and sum the sales
    top_stores = filtered_data.groupby('Store.Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()

    # Add a header for the section
    st.header("Top Stores by Sales (American vodkas)")

    # Create the tree map
    fig = px.treemap(
        top_stores,
        path=['Store.Name'],  # The hierarchy for the treemap (one level: Store.Name)
        values='Sales',  # Values used for the size of the blocks
        labels={'Sales': 'Total Sales ($)', 'Store.Name': 'Store Name'},
        color='Sales',  # Color the blocks based on sales
        color_discrete_sequence=px.colors.qualitative.Pastel # Color scale for the blocks
    )

    # Show the tree map
    st.plotly_chart(fig)


col = st.columns(3)

with col[0]:
    st.header("Vendor Contribution for top")
    vendor_sales = filtered_data.groupby('Vendor.Name')['Sales'].sum().reset_index()
    fig_vendor = px.pie(
        vendor_sales,
        values='Sales',
        names='Vendor.Name',
        title='Vendor Contribution to Total Sales',
        color_discrete_sequence=px.colors.qualitative.Pastel ,

    )
    st.plotly_chart(fig_vendor)

with col[1]:
    st.header('Sales Evolution')
    data['Date'] = pd.to_datetime(data['Date'])
    sales_trend = data.groupby('Date')['Sales'].sum().reset_index()
    fig = px.line(
        sales_trend,
        x='Date',
        y='Sales',
        labels={"Sales": "Sales ($)", "Date": "Date"}
    )
    st.plotly_chart(fig)







