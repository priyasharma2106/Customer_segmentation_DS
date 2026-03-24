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
import os
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
# CUSTOM CSS
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
    .insight-box {
        background-color: #EBF5FB;
        border-left: 4px solid #3498DB;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    # Get path relative to app directory for Streamlit Cloud
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'sample_data.csv')
    
    customer_df = pd.read_csv(data_path)
    
    # Create synthetic transaction data with multiple transactions per customer over time
    # This enables proper cohort analysis with retention variation
    np.random.seed(42)
    transactions = []
    start_date = pd.Timestamp('2023-01-01')
    
    for idx, customer in customer_df.iterrows():
        customer_id = customer['Customer ID']
        num_transactions = np.random.randint(3, 12)  # 3-11 transactions per customer
        
        # First transaction (cohort month)
        first_trans_month_offset = np.random.randint(0, 6)
        first_date = start_date + pd.DateOffset(months=first_trans_month_offset)
        
        for trans_idx in range(num_transactions):
            # Add random days and months between transactions
            days_offset = np.random.randint(5, 45)
            trans_date = first_date + pd.Timedelta(days=trans_idx * days_offset)
            
            # Skip if date goes beyond data range
            if trans_date > start_date + pd.DateOffset(months=12):
                break
                
            transactions.append({
                'Customer ID': customer_id,
                'Country': customer['Country'],
                'Recency': customer['Recency'],
                'Frequency': customer['Frequency'],
                'Monetary': customer['Monetary'],
                'Segment': customer['Segment'],
                'InvoiceDate': trans_date,
                'TotalPrice': np.random.uniform(20, 200),
                'Invoice': f"{customer_id}-{trans_idx}"
            })
    
    df = pd.DataFrame(transactions)
    df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek
    df['Hour'] = np.random.randint(0, 24, len(df))
    
    return df, customer_df

df, customer_df = load_data()

# ============================================================
# CREATE SEGMENTS
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
st.sidebar.markdown("**Dataset:** Sample Customer Data")
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

filtered_df = df.copy()

# ============================================================
# MAIN HEADER
# ============================================================
st.markdown('<p class="main-header">📊 Customer Segmentation & Retention Dashboard</p>',
            unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Overview",
    "👥 Segments",
    "📈 Retention",
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
    col_left, col_right = st.columns(2)

    # Monthly Revenue Trend
    with col_left:
        st.subheader("📈 Monthly Revenue Trend")
        monthly_rev = filtered_df.groupby(
            filtered_df['InvoiceDate'].dt.to_period('M')
        )['TotalPrice'].sum().reset_index()
        monthly_rev['InvoiceDate'] = monthly_rev['InvoiceDate'].astype(str)
        fig = px.area(monthly_rev, x='InvoiceDate', y='TotalPrice',
                      color_discrete_sequence=['#3498DB'],
                      labels={'TotalPrice': 'Revenue (£)', 'InvoiceDate': 'Month'})
        fig.update_layout(height=350, margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)

    # Revenue by Country
    with col_right:
        st.subheader("🌍 Revenue by Country (Top 10)")
        country_rev = filtered_df.groupby('Country')['TotalPrice'].sum()\
                        .sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(country_rev, x='TotalPrice', y='Country',
                     orientation='h',
                     color='TotalPrice',
                     color_continuous_scale='Blues',
                     labels={'TotalPrice': 'Revenue (£)'})
        fig.update_layout(height=350, margin=dict(t=20), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Purchase Heatmap
    st.subheader("🕐 Purchase Activity Heatmap (Day vs Hour)")
    heatmap_data = filtered_df.groupby(
        ['DayOfWeek', 'Hour']
    )['Invoice'].nunique().unstack(fill_value=0)
    heatmap_data.index = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    fig = px.imshow(heatmap_data,
                    color_continuous_scale='YlOrRd',
                    labels=dict(x="Hour of Day", y="Day of Week", color="Orders"),
                    title="When Do Customers Shop?")
    fig.update_layout(height=320, margin=dict(t=40))
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
        fig.update_layout(height=350, margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)

    # Segment revenue bar
    with col2:
        st.markdown("**Revenue by Segment**")
        seg_revenue = filtered_customers.groupby('Segment')['Monetary'].sum().reset_index()
        fig = px.bar(seg_revenue, x='Segment', y='Monetary',
                     color='Segment', color_discrete_map=color_map,
                     labels={'Monetary': 'Total Revenue (£)'},
                     text='Monetary')
        fig.update_traces(texttemplate='£%{text:,.0f}', textposition='outside')
        fig.update_layout(height=350, margin=dict(t=20), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # RFM scatter 3D
    st.subheader("🔵 3D RFM Scatter — Customer Positioning")
    sample = filtered_customers.sample(min(1000, len(filtered_customers)), random_state=42)
    fig = px.scatter_3d(
        sample,
        x='Recency', y='Frequency', z='Monetary',
        color='Segment',
        color_discrete_map=color_map,
        opacity=0.7,
        size_max=8,
        labels={'Recency':'Recency (days)',
                'Frequency':'Frequency (orders)',
                'Monetary':'Monetary (£)'},
        title='3D RFM Customer Segmentation'
    )
    fig.update_layout(height=550)
    st.plotly_chart(fig, use_container_width=True)

    # Segment summary table
    st.subheader("📋 Segment Summary Table")
    seg_summary = filtered_customers.groupby('Segment').agg(
        Customers     = ('Customer ID', 'count'),
        Avg_Recency   = ('Recency', 'mean'),
        Avg_Frequency = ('Frequency', 'mean'),
        Avg_Monetary  = ('Monetary', 'mean'),
        Total_Revenue = ('Monetary', 'sum')
    ).round(1).reset_index()
    seg_summary['Total_Revenue'] = seg_summary['Total_Revenue'].apply(lambda x: f"£{x:,.0f}")
    st.dataframe(seg_summary, use_container_width=True)

    # Business recommendations
    st.subheader("💡 Business Recommendations by Segment")
    recommendations = {
        "🏆 Champions"       : "Reward them. Launch VIP loyalty program. Ask for reviews. They are your brand ambassadors.",
        "💙 Loyal Customers" : "Upsell premium products. Offer early access to new items. Send personalised thank-you notes.",
        "⚠️ At-Risk"         : "Send win-back campaigns with discount codes. Ask for feedback. Act before they leave.",
        "❌ Lost"            : "Last-resort reactivation email. Heavy discount offer. If no response, accept churn."
    }
    for seg, rec in recommendations.items():
        st.markdown(f'<div class="insight-box"><b>{seg}:</b> {rec}</div>',
                    unsafe_allow_html=True)

# ============================================================
# TAB 3 — RETENTION
# ============================================================
with tab3:
    st.subheader("📈 Cohort Retention Analysis")

    try:
        # Build cohort table
        df_cohort = filtered_df.copy()
        df_cohort['CohortMonth']  = df_cohort.groupby('Customer ID')['InvoiceDate']\
                                              .transform('min').dt.to_period('M')
        df_cohort['InvoiceMonth'] = df_cohort['InvoiceDate'].dt.to_period('M')

        cohort_data = df_cohort.groupby(
            ['CohortMonth','InvoiceMonth']
        )['Customer ID'].nunique().reset_index()
        cohort_data.columns = ['CohortMonth','InvoiceMonth','Customers']
        cohort_data['CohortIndex'] = (
            cohort_data['InvoiceMonth'] - cohort_data['CohortMonth']
        ).apply(lambda x: x.n)

        cohort_table = cohort_data.pivot_table(
            index='CohortMonth', columns='CohortIndex', values='Customers'
        )
        cohort_size      = cohort_table.iloc[:, 0]
        retention_table  = cohort_table.divide(cohort_size, axis=0).round(3) * 100
        retention_table.index = retention_table.index.astype(str)

        fig = px.imshow(
            retention_table,
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=50,
            zmin=0,
            zmax=100,
            labels=dict(x="Months Since First Purchase",
                        y="Cohort Month", color="Retention %"),
            title="Monthly Cohort Retention Heatmap (%)",
            text_auto='.0f'
        )
        fig.update_layout(
            height=550, 
            margin=dict(t=50),
            coloraxis_colorbar=dict(thickness=15, len=0.7, x=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Average retention curve
        st.subheader("📉 Average Retention Curve")
        avg_ret = retention_table.mean()
        fig = px.line(x=avg_ret.index, y=avg_ret.values,
                      markers=True,
                      labels={'x':'Months Since First Purchase','y':'Avg Retention (%)'},
                      title='Average Retention Rate Across All Cohorts')
        fig.update_traces(line_color='#E74C3C', line_width=2.5)
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"Cohort analysis requires more transaction history")
        st.info("This feature works best with full transactional data from your actual dataset.")

# ============================================================
# TAB 4 — CHURN RISK
# ============================================================
with tab4:
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
    churn_seg['ActiveRate'] = 100 - churn_seg['ChurnRate']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Churn Rate by Segment**")
        fig = px.bar(churn_seg.sort_values('ChurnRate', ascending=False),
                     x='Segment', y='ChurnRate',
                     color='Segment', color_discrete_map=color_map,
                     labels={'ChurnRate':'Churn Rate (%)'},
                     text='ChurnRate')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Active vs Churned by Segment**")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Active',
                             x=churn_seg['Segment'],
                             y=churn_seg['ActiveRate'],
                             marker_color='#27AE60'))
        fig.add_trace(go.Bar(name='Churned',
                             x=churn_seg['Segment'],
                             y=churn_seg['ChurnRate'],
                             marker_color='#E74C3C'))
        fig.update_layout(barmode='stack', height=380,
                          yaxis_title='Percentage (%)')
        st.plotly_chart(fig, use_container_width=True)

    # High risk customers table
    st.subheader("⚠️ High Risk Customers (At-Risk + High Value)")
    high_risk = filtered_customers[
        (filtered_customers['Recency'] > 60) &
        (filtered_customers['Monetary'] > filtered_customers['Monetary'].quantile(0.75))
    ][['Customer ID','Segment','Recency','Frequency','Monetary']]\
      .sort_values('Monetary', ascending=False).head(20)

    if len(high_risk) > 0:
        st.dataframe(high_risk, use_container_width=True)
        st.markdown(
            '<div class="insight-box">⚠️ These are high-value customers who haven\'t purchased recently. '
            'Priority targets for win-back campaigns.</div>',
            unsafe_allow_html=True
        )
    else:
        st.info("No high-risk customers found in the current filter selection.")

    # Recency distribution by segment
    st.subheader("📊 Recency Distribution by Segment")
    fig = px.box(filtered_customers, x='Segment', y='Recency',
                 color='Segment', color_discrete_map=color_map,
                 title='How Recently Did Each Segment Purchase?',
                 labels={'Recency':'Days Since Last Purchase'})
    fig.add_hline(y=90, line_dash="dash", line_color="red",
                  annotation_text="90-day churn threshold")
    fig.update_layout(height=420, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
