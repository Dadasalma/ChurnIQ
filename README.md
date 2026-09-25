# ChurnIQ — AI-Powered Customer Churn Prediction & Retention Analytics

ChurnIQ is an end-to-end Data Science and Machine Learning project designed to identify customers at risk of churn and support retention analysis through an interactive dashboard.

The project uses the IBM Telco Customer Churn dataset, compares multiple machine learning models, selects the best-performing model, segments customers by churn risk, estimates revenue exposure, and provides an interactive Streamlit dashboard for business-oriented exploration.

## Live Dashboard

[Open ChurnIQ Dashboard](https://dadasalma-churniq-appdashboard-glu7ob.streamlit.app/)

## Project Overview

Customer churn is an important business challenge because losing existing customers can directly affect recurring revenue.

ChurnIQ was built to transform raw telecom customer data into actionable retention insights.

The workflow includes:

- Data cleaning and preprocessing
- Feature engineering
- Exploratory data analysis
- Machine learning model training
- Model comparison
- Churn probability prediction
- Risk segmentation
- Revenue-at-risk estimation
- Interactive analytics dashboard
- Customer retention prioritization

## Dataset

The project uses the IBM Telco Customer Churn sample dataset.

Dataset characteristics:

- 7,043 customers
- 21 original features
- Customer demographic information
- Account information
- Contract details
- Internet and phone services
- Billing information
- Customer churn status

Overall churn rate:

**26.54%**

The dataset represents a fictional telecommunications company and is used for educational and portfolio purposes.

## Machine Learning Models

Three supervised machine learning models were evaluated:

- Logistic Regression
- Random Forest
- XGBoost

The models were compared using classification metrics including:

- ROC-AUC
- Accuracy
- Precision
- Recall
- F1-score

For the current training run, **XGBoost was selected as the best-performing model based on ROC-AUC**.

## Feature Engineering

Additional features were created to improve the analytical workflow, including:

- `ServiceCount`
- `HasInternet`
- `IsMonthToMonth`
- `UsesElectronicCheck`
- `AvgMonthlyValue`

The dataset was split into training and testing sets using an 80/20 stratified split.

## Churn Risk Segmentation

The test set contains:

**1,409 customers**

Customers were segmented according to predicted churn probability:

| Risk Level | Customers |
|---|---:|
| High Risk | 122 |
| Medium Risk | 292 |
| Low Risk | 995 |

Risk thresholds:

- High Risk: probability ≥ 70%
- Medium Risk: probability ≥ 40%
- Low Risk: probability < 40%

Average predicted churn probability on the test population:

**26.38%**

## Revenue-at-Risk Analysis

ChurnIQ estimates potential revenue exposure using predicted churn probability and monthly customer charges.

Estimated revenue exposure on the test population:

- **Monthly revenue at risk: 27,539.05**
- **Annual revenue at risk: 330,468.61**

These values represent analytical estimates based on model probabilities.

They should not be interpreted as realized revenue losses or causal financial predictions.

## Interactive Dashboard

The Streamlit dashboard provides multiple analytical views.

### Overview

Displays:

- Number of customers
- Average churn probability
- High-risk customers
- Estimated monthly revenue at risk
- Estimated annual revenue at risk
- Churn risk distribution
- Customer segmentation insights

### Risk Analytics

Allows exploration of churn risk across:

- Contract type
- Internet service
- Payment method
- Monthly charges
- Customer segments

Interactive filters allow users to dynamically analyze specific customer groups.

### Model & Drivers

Displays:

- Model comparison results
- Best selected model
- Model performance metrics
- Observed churn-risk patterns

### Customer Priorities

Provides a prioritized customer retention queue including:

- Customer ID
- Churn probability
- Risk level
- Monthly charges
- Revenue exposure
- Customer characteristics

Users can also export filtered customer data for further analysis.

## Observed High-Risk Patterns

In the analyzed test population, several characteristics frequently appeared among higher-risk customers, including:

- Month-to-month contracts
- Fiber optic internet service
- Short customer tenure
- Electronic check payments

These are descriptive patterns observed in the dataset and model outputs.

They should not be interpreted as proof of causal relationships.

## Tech Stack

### Data Science & Machine Learning

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Joblib

### Data Visualization

- Plotly
- Matplotlib

### Dashboard

- Streamlit

### Development

- Google Colab
- GitHub
- Streamlit Community Cloud

## Project Structure

```text
ChurnIQ/
│
├── app/
│   └── dashboard.py
│
├── data/
│   └── churniq_predictions.csv
│
├── reports/
│   └── metrics.json
│
├── requirements.txt
└── README.md
