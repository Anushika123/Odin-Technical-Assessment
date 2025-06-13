# 🏥 Hospital Demand Forecasting System

A web-based demand forecasting system built with **Django** and **Random Forest** model that predicts hospital supply demand for the next 8 weeks. Users can upload weekly usage data as a CSV or Excel file and receive forecasted demand, visualizations, and evaluation metrics.

---

## 📌 Features

- 📂 Upload `.csv` or `.xlsx` file containing weekly hospital supply usage
- 🤖 Demand forecasting using **Random Forest Regressor**
- 📊 Forecasts for weeks 149–156 based on training data from weeks 1–148
- 📈 Visualization of **Actual vs Predicted** demand
- ✅ Evaluation metrics:
  - MAPE (Mean Absolute Percentage Error)
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)
- 💻 Simple and intuitive web interface using Django

---

## 🛠 Tech Stack

| Layer         | Technology          |
|---------------|---------------------|
| Backend       | Django               |
| Forecasting   | Random Forest (scikit-learn) |
| Frontend      | HTML + Django Template Engine |
| Visualization | Matplotlib          |
| File Support  | CSV, Excel (via `pandas`) |

---
## ⚙️ Screenshots
![Screenshot 1](Screenshots/Screenshot%201.png)

### Forecast Results
![Screenshot 2](Screenshots/Screenshot%202.png)

### Accuracy Metrics
![Screenshot 3](Screenshots/Screenshot%203.png)



