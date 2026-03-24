# ============================================================
# Customer Segmentation & Retention Analysis Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIG — must be first streamlit command
# ============================================================
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — makes it look professional
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2C3E50;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .insight-box {
        background-color: #EBF5FB;
        border-left: 4px solid #3498DB;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    .segment-champion  { color: #27AE60; font-weight: bold; }
    .segment-loyal     { color: #2980B9; font-weight: bold; }
    .segment-atrisk    { color: #E67E22; font-weight: bold; }
    .segment-lost      { color: #E74C3C; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================
import os

@st.cache_data
def load_data():
    # Get the path relative to the app directory
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'sample_data.csv')
    
    # Load data (no InvoiceDate in sample_data, so don't parse it)
    customer_df = pd.read_csv(data_path)
    return customer_df

customer_df = load_data()


# ============================================================
# RE-CREATE SEGMENTS (if not already in customer_df)
# ============================================================
@st.cache_data
def create_segments(customer_df):
    if 'Segment' not in customer_df.columns:
        features = ['Recency', 'Frequency', 'Monetary']
        X = np.log1p(customer_df[features])
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        customer_df['Cluster'] = kmeans.fit_predict(X_scaled)
        cluster_means = customer_df.groupby('Cluster')[['Recency','Frequency','Monetary']].mean()
        sorted_clusters = cluster_means.sort_values('Monetary', ascending=False)
        labels = ['Champions', 'Loyal Customers', 'At-Risk', 'Lost']
        segment_map = {cid: labels[i] for i, cid in enumerate(sorted_clusters.index)}
        customer_df['Segment'] = customer_df['Cluster'].map(segment_map)
    return customer_df

customer_df = create_segments(customer_df)


# ============================================================
# SIDEBAR — FILTERS
# ============================================================
st.sidebar.title("🎛️ Dashboard Filters")

# Country filter
all_countries = ['All'] + sorted(customer_df['Country'].unique().tolist())
selected_country = st.sidebar.selectbox("🌍 Select Country", all_countries)

# Segment filter
all_segments = customer_df['Segment'].unique().tolist()
selected_segment = st.sidebar.multiselect(
    "👥 Select Segment(s)",
    options=all_segments,
    default=all_segments
)

# Recency filter
max_recency = int(customer_df['Recency'].max())
recency_range = st.sidebar.slider(
    "📅 Recency Range (days)",
    0, max_recency, (0, max_recency)
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Built for:** Customer Segmentation Project")
st.sidebar.markdown("**Tools:** Python · Streamlit · Plotly · Scikit-learn")


# ============================================================
# APPLY FILTERS
# ============================================================
filtered_customers = customer_df.copy()

if selected_country != 'All':
    filtered_customers = filtered_customers[filtered_customers['Country'] == selected_country]

if selected_segment:
    filtered_customers = filtered_customers[filtered_customers['Segment'].isin(selected_segment)]

filtered_customers = filtered_customers[
    (filtered_customers['Recency'] >= recency_range[0]) &
    (filtered_customers['Recency'] <= recency_range[1])
]


# ============================================================
# MAIN HEADER
# ============================================================
st.markdown('<p class="main-header">📊 Customer Segmentation & Retention Dashboard</p>',
            unsafe_allow_html=True)
st.markdown("---")


# ============================================================
# TAB LAYOUT
# ============================================================
tab1, tab2, tab3 = st.tabs([
    "🏠 Overview",
    "👥 Segments",
    "🔮 Churn Risk"
])


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================
with tab1:
    st.subheader("📌 Key Business Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Customers", f"{len(filtered_customers):,}")
    with col2:
        st.metric("Total Revenue", f"£{filtered_customers['Monetary'].sum():,.0f}")
    with col3:
        st.metric("Avg Order Value", f"£{filtered_customers['Monetary'].mean():,.0f}")
    with col4:
        st.metric("Avg Recency", f"{filtered_customers['Recency'].mean():.0f} days")
    with col5:
        churn_rate = (filtered_customers['Recency'] > 90).mean() * 100
        st.metric("Churn Rate", f"{churn_rate:.1f}%")

    st.markdown("---")
    
    # Segment distribution pie
    st.subheader("Segment Distribution")
    seg_counts = filtered_customers['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    color_map = {
        'Champions'       : '#27AE60',
        'Loyal Customers' : '#2980B9',
        'At-Risk'         : '#E67E22',
        'Lost'            : '#E74C3C'
    }
    fig = px.pie(seg_counts, names='Segment', values='Count',
                 color='Segment', color_discrete_map=color_map)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# TAB 2 — SEGMENTS
# ============================================================
with tab2:
    st.subheader("👥 Customer Segments Overview")

    color_map = {
        'Champions'       : '#27AE60',
        'Loyal Customers' : '#2980B9',
        'At-Risk'         : '#E67E22',
        'Lost'            : '#E74C3C'
    }

    col1, col2 = st.columns(2)

    # Segment distribution pie
    with col1:
        st.markdown("**Segment Distribution**")
        seg_counts = filtered_customers['Segment'].value_counts().reset_index()
        seg_counts.columns = ['Segment', 'Count']
        fig = px.pie(seg_counts, names='Segment', values='Count',
                     color='Segment', color_discrete_map=color_map, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    # Segment revenue bar
    with col2:
        st.markdown("**Revenue by Segment**")
        seg_revenue = filtered_customers.groupby('Segment')['Monetary'].sum().reset_index()
        fig = px.bar(seg_revenue, x='Segment', y='Monetary',
                     color='Segment', color_discrete_map=color_map,
                     labels={'Monetary': 'Total Revenue (£)'})
        st.plotly_chart(fig, use_container_width=True)

    # Segment summary table
    st.subheader("📋 Segment Summary")
    seg_summary = filtered_customers.groupby('Segment').agg(
        Customers     = ('Customer ID', 'count'),
        Avg_Recency   = ('Recency', 'mean'),
        Avg_Frequency = ('Frequency', 'mean'),
        Total_Revenue = ('Monetary', 'sum')
    ).round(1).reset_index()
    st.dataframe(seg_summary, use_container_width=True)


# ============================================================
# TAB 3 — CHURN RISK
# ============================================================
with tab3:
    st.subheader("🔮 Churn Risk Analysis")

    color_map = {
        'Champions'       : '#27AE60',
        'Loyal Customers' : '#2980B9',
        'At-Risk'         : '#E67E22',
        'Lost'            : '#E74C3C'
    }

    # Churn by segment
    churn_seg = filtered_customers.groupby('Segment').agg(
        Total    = ('Customer ID', 'count'),
        Churned  = ('Recency', lambda x: (x > 90).sum())
    ).reset_index()
    churn_seg['ChurnRate'] = (churn_seg['Churned'] / churn_seg['Total'] * 100).round(1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Churn Rate by Segment**")
        fig = px.bar(churn_seg.sort_values('ChurnRate', ascending=False),
                     x='Segment', y='ChurnRate',
                     color='Segment', color_discrete_map=color_map,
                     labels={'ChurnRate':'Churn Rate (%)'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Recency Distribution**")
        fig = px.box(filtered_customers, x='Segment', y='Recency',
                     color='Segment', color_discrete_map=color_map,
                     labels={'Recency':'Days Since Last Purchase'})
        st.plotly_chart(fig, use_container_width=True)
