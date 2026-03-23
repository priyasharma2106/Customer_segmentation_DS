# Customer_segmentation_DS
# Customer Segmentation using RFM Analysis

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![License](https://img.shields.io/badge/License-MIT-green)

**Live Demo →** [rfm-dashboard.streamlit.app](https://your-app.streamlit.app)

## Problem statement
E-commerce businesses lose revenue by treating all customers the same.
This project segments customers using RFM (Recency, Frequency, Monetary)
analysis so marketing teams can target the right customers with the right
campaign — reducing churn and increasing repeat purchases.

## Results
| Segment | Customers | Avg Spend | Action |
|---|---|---|---|
| Champions | 23% | ₹4,200 | Reward & upsell |
| At Risk | 18% | ₹1,800 | Re-engagement campaign |
| Lost | 31% | ₹420 | Win-back or ignore |

## What I built
- RFM feature engineering from raw transaction data
- Log transformation to handle skewed distributions
- KMeans clustering with elbow method for optimal K
- DBSCAN for outlier/noise detection
- Interactive 3D cluster visualization
- Streamlit dashboard for non-technical business users

## Tech stack
Python · Pandas · Scikit-learn · Plotly · Streamlit

## Run locally
git clone https://github.com/yourusername/rfm-customer-segmentation
cd rfm-customer-segmentation
pip install -r requirements.txt
streamlit run app/streamlit_app.py

## Dataset
Uses the [UCI Online Retail dataset](https://archive.ics.uci.edu/ml/datasets/online+retail).
A sample of 1,000 rows is included in `/data/sample_data.csv`.

## Key learnings
- Why log1p transformation matters for distance-based algorithms
- How to choose K using elbow method + silhouette score
- Business framing of ML outputs for non-technical stakeholders
