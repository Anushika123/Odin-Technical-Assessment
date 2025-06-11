# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from forecasting import train_and_forecast

# Configure page
st.set_page_config(page_title="📊 Hospital Supply Demand Forecast", layout="wide")

# Hide Streamlit footer and menu
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding: 2rem 1.5rem;}
    </style>
""", unsafe_allow_html=True)

# Page header
st.title("🏥 Hospital Supply Demand Forecasting")
st.markdown("Upload hospital supply usage data to generate an 8-week demand forecast.")

# Upload section
with st.container():
    st.subheader("📁 Upload Data File")
    uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")

    # Data preview
    with st.expander("🔍 Preview Uploaded Data"):
        st.dataframe(df.head(), use_container_width=True)

    # Forecast trigger
    if st.button("🚀 Run Forecast", use_container_width=True):
        result_df, metrics = train_and_forecast(df)

        # Layout in two columns
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📈 Forecast Results")
            st.dataframe(result_df, use_container_width=True)

        with col2:
            st.subheader("📊 Accuracy Metrics (Overall)")
            overall_metrics = metrics.get("Overall", {})
            st.metric("📉 MAPE (%)", f"{overall_metrics.get('MAPE (%)', 'N/A'):.2f}")
            st.metric("📐 RMSE", f"{overall_metrics.get('RMSE', 'N/A'):.2f}")
            st.metric("📏 MAE", f"{overall_metrics.get('MAE', 'N/A'):.2f}")

        # Chart section
        st.subheader("📊 Actual vs Predicted Chart")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=result_df, x='Week', y='Actual', label='Actual', marker='o')
        sns.lineplot(data=result_df, x='Week', y='Predicted', label='Predicted', marker='X')
        ax.set_title("📉 Demand Forecast (Last 8 Weeks)")
        ax.set_xlabel("Week")
        ax.set_ylabel("Quantity Used")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)
