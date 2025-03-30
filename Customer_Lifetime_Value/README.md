# CLV Classification & Regression Analysis

This repository contains two comprehensive projects for Customer Lifetime Value (CLV) analysis:

----------CLV Classification Project-------
Aim:
Segment customers into Low, Medium, and High groups to drive targeted marketing and retention strategies.

Key Steps & Importance:-

1)Data Preparation & Feature Engineering:-
Calculate TotalPrice and aggregate data by CustomerID (computing TotalSpent, PurchaseFrequency, and TotalQuantity) to quantify customer value.

2)Customer Segmentation:-
Use pd.qcut to create three quantiles (Low, Medium, High) for balanced class distribution, then encode these categories for modeling.
3)Visualization:-
Implement custom binning with pd.cut to plot the exact distribution of customers across spending categories, highlighting natural spending patterns.
4)Model Training & Evaluation:-
Train models (Random Forest, AdaBoost, Gradient Boosting, etc.) and evaluate them using accuracy and classification reports, ensuring effective segmentation.

------------CLV Regression Project--------
Aim:
Predict an exact numerical CLV for each customer to support precise forecasting and strategic planning.

Key Steps & Importance:-

1)Data Cleaning & EDA:-
Clean the dataset (handle missing values, duplicates, and outliers) and perform EDA (visualizing revenue, top customers, and monthly sales) to understand data trends.
2)Customer-Level Aggregation & CLV Calculation:-
Compute Recency, Frequency, Monetary value, and AOV, then calculate CLV using industry-standard assumptions (churn rate and profit margin) to quantify customer lifetime value.
3)Model Building:-
Split data, standardize features, and train regression models (Random Forest, AdaBoost, Gradient Boosting, and HistGradientBoosting) for precise CLV predictions.
4)Evaluation & Visualization:-
Assess models with MAE, MSE, R² Score, and a scatter plot comparing actual vs. predicted CLV, ensuring reliable forecasts for data-driven decision-making.

---

## Repository Structure

- `CLV_classification.ipynb`: Jupyter Notebook for the CLV Classification project.
- `CLV_regression.ipynb`: Jupyter Notebook for the CLV Regression project.
- `requirements.txt`: Lists all Python packages required for both projects.
- `README.md`: This file, which contains project details and collaboration guidelines.

Usage:-
Jupyter Notebook:
Open the notebooks (CLV_classification.ipynb and CLV_regression.ipynb) using JupyterLab or VS Code with the Jupyter extension.

Run Sequentially:
Execute the cells sequentially to perform data cleaning, EDA, feature engineering, model training, and evaluation.

Visualizations & Metrics:
Explore the generated plots and performance metrics to understand model performance and gain data insights.