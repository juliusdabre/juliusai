
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Property Market Analysis", layout="wide")
st.title(Property Market Analysis Dashboard)

# Load data
df = pd.read_excel('Suburb Excel and Radar January 2025.xlsx', sheet_name='SA3')
df.columns = df.columns.str.strip()

# Sidebar - Suburb selection
suburbs = df['SA3'].dropna().unique()
selected_suburb = st.sidebar.selectbox('Select a Suburb (SA3) for Details', suburbs)

# Investment Score
if 'Investment_Score' not in df.columns:
    df['Investment_Score'] = (
        df['12M Price Change'].rank(pct=True) * 0.3 +
        df['Yield'].rank(pct=True) * 0.3 +
        df['Sales Turnover'].rank(pct=True) * 0.2 +
        df['Buy Affordability'].rank(pct=True) * 0.2
    )

# Main KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Median Price", f"${df['Median'].median():,.0f}")
col2.metric("12M Price Change", f"{df['12M Price Change'].median():.2f}%")
col3.metric("Yield", f"{df['Yield'].median():.2f}%")
col4.metric("Buy Affordability", f"{df['Buy Affordability'].median():.2f}")

# Top Investment Opportunities
top_investment = df.nlargest(10, 'Investment_Score')[['SA3', 'Median', '12M Price Change', 'Yield', 'Sales Turnover', 'Buy Affordability']]
st.subheader("Top 10 Investment Opportunities")
st.dataframe(top_investment, use_container_width=True)

# Correlation Heatmap
st.subheader("Market Metrics Correlation Heatmap")
corr = df[['Median', '12M Price Change', 'Yield', 'Sales Turnover', 'Buy Affordability', 'Rent Affordability']].corr()
fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu', title="Correlation Heatmap")
st.plotly_chart(fig_corr, use_container_width=True)

# Price Distribution
st.subheader("Property Price Distribution")
fig_dist = px.histogram(df, x='Median', nbins=30, title='Distribution of Property Prices')
st.plotly_chart(fig_dist, use_container_width=True)

# Suburb Radar Chart
def plot_radar(suburb):
    row = df[df['SA3'] == suburb].iloc[0]
    metrics = ['12M Price Change', 'Yield', 'Sales Turnover', 'Buy Affordability', 'Rent Affordability']
    values = [row[m] for m in metrics]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=metrics, fill='toself', name=suburb))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False, title=f"Radar Chart for {suburb}")
    return fig

st.subheader(f"Detailed Metrics for {selected_suburb}")
st.dataframe(df[df['SA3'] == selected_suburb], use_container_width=True)
st.plotly_chart(plot_radar(selected_suburb), use_container_width=True)

# Price vs Growth Scatter
st.subheader("Price vs 12M Price Change")
fig_scatter = px.scatter(df, x='Median', y='12M Price Change', color='Yield', size='Sales Turnover', hover_name='SA3',
                        title='Price vs 12M Price Change', labels={'Median': 'Median Price', '12M Price Change': '12M Price Change (%)'})
st.plotly_chart(fig_scatter, use_container_width=True)
