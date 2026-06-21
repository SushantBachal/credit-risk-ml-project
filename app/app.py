import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib.pyplot as plt
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.preprocess import preprocess_input
from src.predict import predict, model

@st.cache_data
def load_training_data():
    path = os.path.join(BASE_DIR, 'data', 'processed_data', 'X_train.csv')
    return pd.read_csv(path)

X_train_res = load_training_data()

# Page config
st.set_page_config(
    page_title="Credit Risk Predictor",
    page_icon="💳",
    layout="centered"
)

# Title
st.title("💳 Credit Risk Predictor")
st.markdown("Enter your details below to check your credit default risk.")

# Input form
st.header("Your Financial Details")

age = st.number_input(
    "Your Age",
    min_value=18, max_value=100, value=35,
    help="Enter your current age in years")

monthly_income = st.number_input(
    "Your Monthly Income (₹)",
    min_value=0.0, max_value=10000000.0, value=50000.0,
    help="Enter your total monthly take home income in rupees")

credit_limit = st.number_input(
    "Your Total Credit Card Limit (₹)",
    min_value=1.0, max_value=10000000.0, value=100000.0,
    help="Total credit limit across all your credit cards combined")

outstanding_balance = st.number_input(
    "Your Current Outstanding Credit Card Balance (₹)",
    min_value=0.0, max_value=10000000.0, value=30000.0,
    help="Total amount you currently owe on all credit cards")

monthly_debt = st.number_input(
    "Your Total Monthly Debt Payments (₹)",
    min_value=0.0, max_value=10000000.0, value=10000.0,
    help="Total monthly payments for all loans and credit cards combined")

open_credit = st.number_input(
    "How Many Credit Cards and Loans Do You Have?",
    min_value=0, max_value=50, value=3,
    help="Count all active credit cards, personal loans, car loans etc.")

times_90_late = st.number_input(
    "How Many Times Have You Been 90+ Days Late on a Payment?",
    min_value=0, max_value=20, value=0,
    help="Number of times you were more than 90 days late on any payment")

real_estate = st.number_input(
    "How Many Home Loans or Mortgages Do You Have?",
    min_value=0, max_value=20, value=0,
    help="Number of active home loans or mortgage accounts")

dependents = st.number_input(
    "How Many People Depend on You Financially?",
    min_value=0, max_value=20, value=0,
    help="Include children, spouse, parents or anyone you financially support")

# Calculate ratios in backend
revolving = outstanding_balance / credit_limit if credit_limit > 0 else 0
debt_ratio = monthly_debt / monthly_income if monthly_income > 0 else 0

# Predict button
if st.button("Check My Credit Risk"):

    # Build input dictionary
    user_input = {
        'RevolvingUtilizationOfUnsecuredLines': revolving,
        'age': age,
        'DebtRatio': debt_ratio,
        'MonthlyIncome': monthly_income,
        'NumberOfOpenCreditLinesAndLoans': open_credit,
        'NumberOfTimes90DaysLate': times_90_late,
        'NumberRealEstateLoansOrLines': real_estate,
        'NumberOfDependents': dependents
    }

    # Preprocess
    processed = preprocess_input(user_input)

    # Predict
    probability, prediction = predict(processed)

    # Show result
    st.header("Your Credit Risk Result")

    if prediction == 1:
        st.error(f"⚠️ HIGH RISK — Default Probability: {probability:.1%}")
        st.markdown("Your profile suggests a higher chance of financial default. Consider reducing outstanding balances and avoiding late payments.")
    else:
        st.success(f"✅ LOW RISK — Default Probability: {probability:.1%}")
        st.markdown("Your profile looks financially healthy. Keep maintaining good payment habits.")

    st.metric("Default Probability", f"{probability:.1%}")

    # Show calculated ratios for transparency
    st.subheader("Calculated Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Credit Utilization", f"{revolving:.1%}")
    with col2:
        st.metric("Debt to Income Ratio", f"{debt_ratio:.2f}")

    # SHAP explanation
    st.header("Why This Prediction?")
    st.markdown("This chart shows which factors influenced your risk score the most.")

    explainer = shap.Explainer(model, X_train_res)
    shap_values = explainer(processed)

    fig, ax = plt.subplots()
    shap.plots.waterfall(shap_values[0], show=False)
    st.pyplot(fig)