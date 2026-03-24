# RFM Customer Segmentation Dashboard

A comprehensive Streamlit dashboard for customer segmentation using RFM (Recency, Frequency, Monetary) analysis with K-Means clustering.

## Features

- **📊 Overview Tab**: Key metrics, revenue trends, and purchase activity heatmaps
- **👥 Segments Tab**: Customer segmentation visualization with RFM clustering
- **🔮 Churn Risk Tab**: Identify at-risk customers and churn analysis
- **🎛️ Interactive Filters**: Filter by country, segment, recency range
- **📈 Advanced Charts**: Pie charts, bar charts, heatmaps, 3D scatter plots

## Installation

1. Clone the repository:
```bash
git clone https://github.com/priyasharma2106/Customer_segmentation_DS.git
cd rfm-customer-segmentation
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app locally:
```bash
streamlit run app/streamlit_app.py
```

The dashboard will open at `http://localhost:8501`

## 🚀 Deploy to Streamlit Cloud (FREE)

### Step 1: Push to GitHub ✅ (Already done!)

### Step 2: Connect to Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account (if not already connected)
4. Select your repository: `priyasharma2106/Customer_segmentation_DS`
5. Select branch: `main`
6. Select the app file path: `rfm-customer-segmentation/app/streamlit_app.py`
7. Click **"Deploy"**

### Step 3: Configure Secrets (if needed)

If you use API keys or sensitive data, add them in Streamlit Cloud settings:
- Go to your app settings → Secrets
- Add any environment variables needed

### Live Demo URL

Once deployed, your app will be live at:
```
https://share.streamlit.io/priyasharma2106/Customer_segmentation_DS/main/rfm-customer-segmentation/app/streamlit_app.py
```

**Status**: 🟢 Ready to deploy!

## Project Structure

```
rfm-customer-segmentation/
├── app/
│   └── streamlit_app.py          # Main Streamlit dashboard
├── notebooks/
│   └── rfm_analysis.ipynb        # RFM analysis notebook
├── data/
│   └── sample_data.csv           # Sample customer data
├── assets/
│   └── screenshot.png            # Dashboard screenshot
├── README.md
├── requirements.txt
└── .gitignore
```

## Data Requirements

The dashboard expects customer data with the following columns:
- `Customer ID`
- `Country`
- `Recency` (days since last purchase)
- `Frequency` (number of purchases)
- `Monetary` (total spending)

## Segmentation

Customers are segmented into 4 groups based on RFM analysis:
- **Champions** 🏆: High value, frequent, recent
- **Loyal Customers** 💙: Consistent value, good frequency
- **At-Risk** ⚠️: Good historical value, declining engagement
- **Lost** ❌: Low value, haven't purchased recently

## Technologies Used

- **Python 3.8+**
- **Streamlit** - Web framework
- **Pandas** - Data processing
- **Scikit-learn** - K-Means clustering
- **Plotly** - Interactive visualizations

## Author

Priya Sharma

## License

MIT License

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
