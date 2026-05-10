import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
from sklearn.linear_model import LinearRegression

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💰",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

section[data-testid="stSidebar"] {
    background-color: #1A1A2E;
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1E1E2F, #2A2A40);
    border: 1px solid #444;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    margin-top: 10px;
}

.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

header_html = """
<div style="
    background: linear-gradient(90deg, #141E30, #243B55);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 25px;
    text-align:center;
">

    <h1 style="
        color:white;
        font-size:48px;
        margin-bottom:10px;
    ">
        💰 FinSight AI
    </h1>

    <p style="
        color:#EAEAEA;
        font-size:20px;
    ">
        Smart Expense Tracking • Financial Intelligence • AI Analytics
    </p>

</div>
"""

components.html(header_html, height=180)

# =========================================
# BASE DIRECTORY
# =========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# =========================================
# LOAD DATA
# =========================================

file_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_expenses.csv"
)

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

# =========================================
# SIDEBAR
# =========================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2489/2489756.png",
    width=90
)

st.sidebar.title("📊 FinSight Controls")

selected_category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

selected_payment = st.sidebar.multiselect(
    "Payment Method",
    options=df["Payment_Method"].unique(),
    default=df["Payment_Method"].unique()
)

selected_location = st.sidebar.multiselect(
    "Location",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)

# =========================================
# FILTER DATA
# =========================================

filtered_df = df[
    (df["Category"].isin(selected_category)) &
    (df["Payment_Method"].isin(selected_payment)) &
    (df["Location"].isin(selected_location))
]

# =========================================
# KPI METRICS
# =========================================

total_spending = filtered_df["Amount"].sum()
average_spending = filtered_df["Amount"].mean()
highest_expense = filtered_df["Amount"].max()
transaction_count = len(filtered_df)

# =========================================
# KPI SECTION
# =========================================

st.subheader("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Spending",
    f"₹ {total_spending:,.2f}",
    delta="+12%"
)

col2.metric(
    "📈 Average Spending",
    f"₹ {average_spending:,.2f}",
    delta="+4%"
)

col3.metric(
    "🔥 Highest Expense",
    f"₹ {highest_expense:,.2f}",
    delta="-2%"
)

col4.metric(
    "🧾 Transactions",
    transaction_count,
    delta="+8%"
)

# =========================================
# BUDGET TRACKER
# =========================================

st.subheader("🎯 Monthly Budget Tracker")

budget = 3000000

progress = min(total_spending / budget, 1.0)

st.progress(progress)

st.write(f"Budget Used: ₹ {total_spending:,.2f} / ₹ {budget:,.2f}")

# =========================================
# AI INSIGHT BOX
# =========================================

highest_category = (
    filtered_df.groupby("Category")["Amount"]
    .sum()
    .idxmax()
)

st.markdown(f"""
<div style="
    background-color:#1E1E2F;
    padding:20px;
    border-radius:15px;
    margin-top:20px;
    margin-bottom:20px;
    border-left:5px solid #00D4FF;
">

<h3 style="color:white;">🤖 AI Financial Insight</h3>

<p style="color:#D3D3D3; font-size:16px;">
Your highest spending category is <b>{highest_category}</b>. 
Consider reducing non-essential purchases to improve monthly savings and budget efficiency.
</p>

</div>
""", unsafe_allow_html=True)

# =========================================
# CATEGORY CHART
# =========================================

category_spending = (
    filtered_df.groupby("Category")["Amount"]
    .sum()
    .reset_index()
)

fig1 = px.pie(
    category_spending,
    names="Category",
    values="Amount",
    hole=0.6,
    title="Category-wise Spending",
    color_discrete_sequence=px.colors.sequential.Tealgrn
)

fig1.update_layout(template="plotly_dark")

# =========================================
# MONTHLY TREND
# =========================================

monthly_spending = (
    filtered_df.groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    monthly_spending,
    x="Month",
    y="Amount",
    markers=True,
    title="Monthly Expense Trend"
)

fig2.update_layout(template="plotly_dark")

# =========================================
# PAYMENT ANALYSIS
# =========================================

payment_analysis = (
    filtered_df.groupby("Payment_Method")["Amount"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    payment_analysis,
    x="Payment_Method",
    y="Amount",
    text_auto=True,
    title="Payment Method Analysis",
    color="Payment_Method"
)

fig3.update_layout(template="plotly_dark")

# =========================================
# HEATMAP
# =========================================

st.subheader("🔥 Spending Heatmap")

heatmap_data = (
    filtered_df.groupby(["Month", "Category"])["Amount"]
    .sum()
    .reset_index()
)

heatmap_pivot = heatmap_data.pivot(
    index="Category",
    columns="Month",
    values="Amount"
)

fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index
    )
)

fig_heatmap.update_layout(
    template="plotly_dark"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# =========================================
# FORECASTING
# =========================================

st.subheader("🔮 Expense Forecasting")

monthly_numeric = (
    filtered_df.groupby(filtered_df["Date"].dt.month)["Amount"]
    .sum()
    .reset_index()
)

X = monthly_numeric.iloc[:, 0].values.reshape(-1, 1)
y = monthly_numeric.iloc[:, 1].values

model = LinearRegression()
model.fit(X, y)

future_month = np.array([[13]])

prediction = model.predict(future_month)[0]

forecast_fig = px.line(
    monthly_numeric,
    x=monthly_numeric.columns[0],
    y="Amount",
    markers=True,
    title="Future Expense Forecast"
)

forecast_fig.add_scatter(
    x=[13],
    y=[prediction],
    mode="markers",
    name="Predicted Next Month"
)

forecast_fig.update_layout(template="plotly_dark")

st.plotly_chart(forecast_fig, use_container_width=True)

st.success(
    f"Predicted Expense For Next Month: ₹ {prediction:,.2f}"
)

# =========================================
# CHART SECTION
# =========================================

st.subheader("📈 Expense Insights")

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig1, use_container_width=True)

with right_col:
    st.plotly_chart(fig2, use_container_width=True)

st.plotly_chart(fig3, use_container_width=True)

# =========================================
# TRANSACTION TABLE
# =========================================

st.subheader("📋 Expense Transactions")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =========================================
# DOWNLOAD BUTTON
# =========================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_expenses.csv",
    mime="text/csv"
)

# =========================================
# FOOTER
# =========================================

st.markdown("""
---
<center>

### 🚀 FinSight AI

Smart Financial Intelligence Platform built with Python, Streamlit, Plotly & Machine Learning

</center>
""", unsafe_allow_html=True)