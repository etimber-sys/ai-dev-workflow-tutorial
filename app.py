import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("data/sales-data.csv", parse_dates=["date"])
    null_count = int(df["total_amount"].isna().sum())
    df = df.dropna(subset=["total_amount"])
    if null_count > 0:
        st.info(f"{null_count} rows excluded due to missing amount values.")
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("Sales data file not found at data/sales-data.csv.")
    st.stop()

if df.empty:
    st.error("No sales data found. Please check that data/sales-data.csv is present and contains records.")
    st.stop()

st.title("Sales Performance Dashboard")

total_sales = df["total_amount"].sum()
total_orders = len(df)

col1, col2 = st.columns(2)
col1.metric(label="Total Sales", value=f"${total_sales:,.0f}")
col2.metric(label="Total Orders", value=f"{total_orders:,}")

df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
monthly = df.groupby("month")["total_amount"].sum().reset_index()

fig_trend = px.line(
    monthly,
    x="month",
    y="total_amount",
    title="Sales Trend Over Time",
    labels={"month": "Month", "total_amount": "Revenue ($)"},
)
st.plotly_chart(fig_trend, use_container_width=True)
