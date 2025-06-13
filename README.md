# Technical Assessment: Demand Forecasting + UI for Hospital Supplies

## Objective:
Build a simple UI + backend workflow that allows a hospital team to:
1. Upload weekly usage history data(Attached)
2. Process and forecast future demand​
3. View prediction results​

## Data Provided in the following format:

(Find file in the Github repository)

| Sr.No | Column | Description |
|-------|--------|-------------|
| 1 | Item_Code | Unique Code identifying the hospital supply Item |
| 2 | Item_Description | Name Of the Item |
| 3 | Patient_Footfall | Number of patients for that week (Approximate which affects demand) |
| 4 | Last_Week_Usage | Quantity used in the previous Week |
| 5 | Public_Holiday | Binary Indicator 1=Public holiday, 0 = no public holiday |
| 6 | Rain_Impact | Binary Indicator 1=There was rain , 0 = no rain |
| 7 | Quantity_used | Actual quantity used for that item in the given week |


## Part 1: UI + Upload Mechanism

### Task:
Build a simple user interface (UI) to:
- Allow the user to upload a .csv/excel file​
- Trigger the demand forecasting model​
- Display the forecast results (table and chart)​

### Tools You Can Use:
- Python + Streamlit / Flask / Django/Fast API​
- OR Node.js + React/Vue​
- OR any full-stack framework of your choice​

## Part 2: Demand Forecasting Model

### Requirements:
1. Use Random Forest, Prophet, (or any other time-series model of your choice)​
2. Forecast the next 8 weeks​
3. Show Actual vs Predicted chart for the last 8weeks (Read Below Notes)
   a. **Split the data** Use data up to week 148 (out of 156 weeks) as training data
   b. **Train model** Train your Random Forest (or other model) only on this training portion
   c. **Predict** Use the model to predict demand for week 149 to 156d.​ 
   d. **Compare** Match your predictions to the actuals in week 149–156 from the dataset
4. Print accuracy metrics: MAPE(Mean Absolute Percentage Error), RMSE(Root Mean Squared Error), MAE(Mean Absolute Error)

## Evaluation Criteria:

| Area | Weight |
|------|--------|
| UI Design & Functionality | 15% |
| Data Preprocessing | 15% |
| Forecast Model & Logic | 35% |
| Evaluation & Visualization | 20% |
| Code Quality & Comments | 15% |

## Deliverables:
- Source code (Python/JS/Other) (Push your code to github following Github link)
  - https://github.com/Anushika123/Odin-Technical-Assessment.git
  - Create a branch in your name and raise the PR​
- README.md with setup instructions​
- Screenshot or screen recording of the working application​
- Jupyter Notebook/Google Colab (if used , not mandatory) for model logic

## Getting Started
- Fork/clone the repository
- Create a new branch with your name
- Implement the solution following the requirements
- Test your application thoroughly
- Document your setup process in README.md
- Submit via pull request
