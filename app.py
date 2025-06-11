import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import backend_pipeline

# ----------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="🏥 Hospital Demand Forecasting",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------- HEADER ------------------------
st.title("🏥 Hospital Demand Forecasting App")
st.markdown("Upload your weekly hospital supply data and forecast demand using machine learning.")

# ----------------- FILE UPLOADER -----------------
st.header("📤 Upload Data")
uploaded_file = st.file_uploader(
    label="Upload a `.csv` or `.xlsx` file",
    type=["csv", "xlsx"]
)

# ----------------- MAIN LOGIC -----------------
if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    st.subheader("📄 Preview of Uploaded Data")
    st.dataframe(df.head(), use_container_width=True)

    # ----------------- RUN FORECAST -----------------
    st.subheader("🔍 Step: Run Demand Forecasting Model")
    if st.button("Run Model"):
        with st.spinner("⏳ Training model and forecasting..."):
            try:
                metrics, evaluation_df = backend_pipeline(df)
                st.success("✅ Forecast completed successfully!")
            except Exception as e:
                st.error(f"❌ Forecast failed: {e}")
                st.stop()

        # ----------------- RESULTS TABLE -----------------
        st.subheader("📈 Actual vs Predicted (Test Set - 25%)")
        st.dataframe(evaluation_df, use_container_width=True)

        # ----------------- CHART (Matplotlib) -----------------
        st.markdown("### 📉 Visualization: Demand Comparison")

        try:
            plt.figure(figsize=(10, 5))
            plt.plot(evaluation_df['Week'], evaluation_df['Actual'], marker='o', label='Actual', color='blue')
            plt.plot(evaluation_df['Week'], evaluation_df['Predicted'], marker='o', label='Predicted', color='orange')
            plt.title("Actual vs Predicted Demand (Test Set)")
            plt.xlabel("Week")
            plt.ylabel("Quantity Used")
            plt.legend()
            plt.grid(True)
            st.pyplot(plt.gcf())  # Show current figure
        except Exception as e:
            st.warning("⚠️ Could not generate chart. Check column names: 'Week', 'Actual', 'Predicted'.")

        # ----------------- METRICS -----------------
        st.subheader("📊 Forecast Accuracy Metrics")
        st.json(metrics)

# ----------------- FOOTER -----------------
st.markdown("---")



