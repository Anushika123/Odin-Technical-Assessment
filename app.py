import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from model_utils import train_random_forest, evaluate_model
from forecast_utils import preprocess_data, split_data

st.set_page_config(page_title="Hospital Supply Forecast", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #f0f5ff;
    }
    .stApp {
        background: linear-gradient(to right, #e0f7fa, #f1f8e9);
    }
    h2, h3 {
        font-family: 'Trebuchet MS', sans-serif;
        background: -webkit-linear-gradient(#0072ff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .css-1v3fvcr, .stButton > button {
        background-color: #0072ff !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    .stDownloadButton > button {
        background-color: #009688 !important;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    .metric-label, .metric-value {
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Hospital Supply Demand Forecasting</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload your hospital supplies data for demand prediction</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Drop your file here (CSV only)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean column names (replace spaces with underscores)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    st.write("✅ Cleaned columns:", df.columns.tolist())  # For confirmation

    # Preprocess data
    df = preprocess_data(df)

    items = df['Item_Code'].unique()

    for item in items:
        st.subheader(f"📦 {df[df['Item_Code'] == item]['Item_Description'].iloc[0]}")
        item_df = df[df['Item_Code'] == item]
        train, test = split_data(item_df)

        features = ['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact']
        
        X_train = train[features]
        y_train = train['Quantity_Used']

        X_test = test[features]
        y_test = test['Quantity_Used']  # ✅ Fixed: now matches cleaned column name

        model = train_random_forest(X_train, y_train)
        predictions = model.predict(X_test)

        mae, mape, rmse = evaluate_model(y_test, predictions)

        # Performance Metrics
        st.markdown("### 📊 Model Performance Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("MAE", f"{mae:.2f}")
        col2.metric("MAPE", f"{mape:.2f}%")
        col3.metric("RMSE", f"{rmse:.2f}")

        # Forecast Visualization
        st.markdown("### 📈 Forecast Visualization")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=test.index, y=y_test, mode='lines+markers', name='Actual'))
        fig.add_trace(go.Scatter(x=test.index, y=predictions, mode='lines+markers', name='Random Forest Prediction'))
        fig.update_layout(xaxis_title='Week Index', yaxis_title='Quantity Used', template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

        # Forecast Table
        st.markdown("### 📋 Detailed Forecast Data")
        result_df = pd.DataFrame({
            'Week': test.index,
            'Actual': y_test.values,
            'RF_Prediction': predictions
        })
        st.dataframe(result_df.style.format({"Actual": "{:.2f}", "RF_Prediction": "{:.2f}"}), use_container_width=True)

        # Export Button
        st.download_button(
        label="📁 Export as CSV",
        data=result_df.to_csv(index=False),
        file_name=f"{item}_forecast_results.csv",
        mime='text/csv',
        key=f"download_button_{item}"  # ✅ Unique key for each item
)

