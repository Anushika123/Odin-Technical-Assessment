# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from forecasting import train_and_forecast

st.set_page_config(page_title="📊 Hospital Supply Demand Forecast", layout="wide")
st.markdown("""

""", unsafe_allow_html=True)

st.title("🏥 Hospital Supply Demand Forecasting")

uploaded_file = st.file_uploader("📁 Upload your Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")

    st.subheader("🔍 Preview of Uploaded Data")
    st.dataframe(df.head(), use_container_width=True)

    if st.button("🚀 Run Forecast"):
        result_df, metrics = train_and_forecast(df)

        st.subheader("📈 Forecast Results")
        st.dataframe(result_df, use_container_width=True)

        st.subheader("📊 Accuracy Metrics (Overall)")
        overall_metrics = metrics.get("Overall", {})
        st.metric("MAPE (%)", f"{overall_metrics.get('MAPE (%)', 'N/A'):.2f}")
        st.metric("RMSE", f"{overall_metrics.get('RMSE', 'N/A'):.2f}")
        st.metric("MAE", f"{overall_metrics.get('MAE', 'N/A'):.2f}")

        st.subheader("📉 Actual vs Predicted Chart")
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=result_df, x='Week', y='Actual', label='Actual', marker='o')
        sns.lineplot(data=result_df, x='Week', y='Predicted', label='Predicted', marker='X')
        plt.xlabel("Week")
        plt.ylabel("Quantity Used")
        plt.title("Actual vs Predicted Demand (Last 8 Weeks)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt.gcf())
