import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.markdown("""
<style>

/* Background */
.stApp{
    background-color:#0E1117;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#1E1E2F;
}

/* Main Title */
h1{
    color:#4CAF50;
    font-weight:bold;
}

/* Sub Heading */
h2,h3{
    color:white;
}

/* Buttons */
.stButton>button{
    background:#4CAF50;
    color:white;
    border-radius:10px;
    border:none;
}

.stButton>button:hover{
    background:#45a049;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    background:#1F2937;
    padding:20px;
    border-radius:15px;
    border:1px solid #2D3748;
}

/* DataFrame */
[data-testid="stDataFrame"]{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Read CSV File
# -----------------------------
# -----------------------------
# Upload CSV / Excel File
# -----------------------------
uploaded_file = st.sidebar.file_uploader(
    "📂 Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    df = pd.read_csv("Data/sales_data.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Create Sales column
df["Sales"] = df["Quantity"] * df["Price"]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📋 Dashboard Menu")

st.sidebar.success("🟢 Dashboard Ready")

st.sidebar.info("""
📊 Sales Analytics Dashboard

👨‍💻 Developed by:
Jai Prakash

🛠 Technologies Used

✔ Python
✔ Pandas
✔ Streamlit
✔ Plotly
✔ Plotly Express
""")

st.sidebar.markdown("---")

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(df["Category"].unique())
)

# Apply Category Filter
if category != "All":
    df = df[df["Category"] == category]

# Date Filter
start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Date"].max()
)

# Apply Date Filter
df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]
if df.empty:
    st.warning("⚠ No data available for the selected filters.")
    st.stop()
# -----------------------------
# Product Search
# -----------------------------
search_product = st.sidebar.text_input("🔍 Search Product")

if search_product:
    df = df[
        df["Product"].str.contains(
            search_product,
            case=False,
            na=False
        )
    ]


# -----------------------------
# Dashboard Title
# -----------------------------
st.title("📊 Sales Analytics Dashboard")

st.markdown("""
### Welcome to the Sales Performance Dashboard

Analyze your business performance using interactive charts,
filters and KPIs.

""")

st.success("Dashboard Loaded Successfully ✅")

st.info(
    "📊 This dashboard helps analyze sales performance using interactive charts, filters, and KPIs."
)
st.progress(100)

st.caption("Project Status: 100% Completed ✅")
# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "📈 Charts",
    "📋 Reports",
    "ℹ About"
])

# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background:#1F2937;padding:20px;border-radius:15px;text-align:center;">
        <h3>💰 Total Sales</h3>
        <h1 style="color:#00FF99;">₹{df['Sales'].sum():,.0f}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:#1F2937;padding:20px;border-radius:15px;text-align:center;">
        <h3>📦 Orders</h3>
        <h1 style="color:#4FC3F7;">{len(df)}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background:#1F2937;padding:20px;border-radius:15px;text-align:center;">
        <h3>🛒 Products</h3>
        <h1 style="color:#FFD54F;">{df['Product'].nunique()}</h1>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Dashboard Summary
# -----------------------------
st.markdown("---")
st.subheader("📋 Dashboard Summary")
st.write(f"Showing **{len(df)}** records.")

# -----------------------------
# Sales Data
# -----------------------------
st.subheader("Sales Data")
st.dataframe(df, use_container_width=True)
st.markdown("---")
st.subheader("📈 Dataset Statistics")

st.write(df.describe())

# -----------------------------
# Category Wise Sales
# -----------------------------
category_sales = df.groupby("Category")["Sales"].sum().reset_index()
# Create Bar Chart
fig_bar = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    text_auto=True,
    title="Sales by Category"
)

# Create Pie Chart
fig_pie = px.pie(
    category_sales,
    names="Category",
    values="Sales",
    hole=0.4,
    title="Sales Distribution by Category"
)

st.markdown("---")


col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Category Wise Sales")
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🥧 Sales Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)


# -----------------------------
# Daily Sales Trend
# -----------------------------

daily_sales = df.groupby("Date")["Sales"].sum().reset_index()

st.markdown("---")
st.subheader("📈 Daily Sales Trend")

fig_line = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="📈 Sales Trend",
    markers=True
)

fig_line.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales (₹)",
    hovermode="x unified",
    template="plotly_dark",
    height=500
)

fig_line.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(fig_line, use_container_width=True)

# -----------------------------
# Top 10 Products
# -----------------------------

# Top 10 products by Sales
top_products = (
    df.groupby("Product")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

st.markdown("---")
st.subheader("🏆 Top 10 Products")

fig_top = px.bar(
    top_products,
    x="Product",
    y="Sales",
    color="Sales",
    text_auto=True,
    title="Top 10 Products by Sales"
)

fig_top.update_layout(
    xaxis_title="Product",
    yaxis_title="Sales (₹)",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig_top, use_container_width=True)

# -----------------------------
# Monthly Sales
# -----------------------------
df["Month"] = df["Date"].dt.strftime("%B")

monthly_sales = (
    df.groupby("Month")["Sales"]
      .sum()
      .reset_index()
)
month_order = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

st.markdown("---")
st.subheader("📅 Monthly Sales Comparison")

fig_month = px.bar(
    monthly_sales,
    x="Month",
    y="Sales",
    color="Sales",
    text_auto=True,
    title="Monthly Sales Comparison"
)

fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales (₹)",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig_month, use_container_width=True)
# -----------------------------
# Download Button
# -----------------------------
st.markdown("---")

st.download_button(
    label="⬇ Download Filtered Data",
    data=df.to_csv(index=False),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;padding:15px;background:#1f2937;
    border-radius:10px;color:white">

    <h3>📊 Sales Analytics Dashboard</h3>

    <p>
    Developed by <b>Jai Prakash</b>
    </p>

    <p>
    Python | Pandas | Streamlit | Plotly
    </p>

    <p>
    © 2026 All Rights Reserved
    </p>

    </div>
    """,
    unsafe_allow_html=True
)
