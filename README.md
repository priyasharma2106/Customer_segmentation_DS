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
