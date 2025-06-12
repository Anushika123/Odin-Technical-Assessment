import streamlit as st
import pandas as pd
from forecast_model import forecast_demand

st.set_page_config(layout="wide")

st.title("🏥 Hospital Supply Demand Forecasting")

uploaded_file = st.file_uploader("Upload weekly usage history data (.csv)", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Uploaded Data Preview")
    st.dataframe(df.head())

    if st.button("Run Forecast"):
        with st.spinner("Forecasting..."):
            result_df, metrics, fig = forecast_demand(df)

        st.success("Forecast complete!")

        st.subheader("📊 Forecast Results")
        st.dataframe(result_df)

        st.subheader("📈 Actual vs Predicted Chart")
        st.pyplot(fig)

        st.subheader("📌 Evaluation Metrics")
        st.markdown(f"- **MAPE**: {metrics['MAPE']:.2f}")
        st.markdown(f"- **RMSE**: {metrics['RMSE']:.2f}")
        st.markdown(f"- **MAE**: {metrics['MAE']:.2f}")
