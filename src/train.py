import pandas as pd
import numpy as np
import pickle
import sys
import os
sys.path.append('..')

from src.db_connect import get_db_engine
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def train():
    """
    Complete training pipeline from database to saved model
    """
    # Step 1 — Load data
    engine = get_db_engine()
    df = pd.read_sql("SELECT * FROM creditcarddb.credit_card_info", con=engine)

    # Step 2 — Fix MonthlyIncome zeros
    df['MonthlyIncome'] = df['MonthlyIncome'].replace(0, np.nan)
    df['MonthlyIncome'] = df['MonthlyIncome'].fillna(df['MonthlyIncome'].median())

    # Step 3 — Drop unnecessary columns
    df = df.drop(columns=['id',
                          'NumberOfTime30-59DaysPastDueNotWorse',
                          'NumberOfTime60-89DaysPastDueNotWorse'])

    # Step 4 — Remove bad rows
    df = df[~df['NumberOfTimes90DaysLate'].isin([96, 98])]
    df = df[df['age'] >= 18]

    # Step 5 — Cap outliers
    df['RevolvingUtilizationOfUnsecuredLines'] = df['RevolvingUtilizationOfUnsecuredLines'].clip(upper=1)
    df['DebtRatio'] = df['DebtRatio'].clip(upper=10)

    # Step 6 — Split features and target
    X = df.drop(columns=['SeriousDlqin2yrs'])
    y = df['SeriousDlqin2yrs']

    # Step 7 — Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # Step 8 — SMOTE
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

    # Step 9 — Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_res, y_train_res)

    # Step 10 — Save model
    with open('../models/models.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Model trained and saved successfully")

if __name__ == "__main__":
    train()