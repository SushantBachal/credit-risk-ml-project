import pickle
import os

# Load model once when file is imported
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'models.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

def predict(processed_df):
    """
    Takes preprocessed DataFrame
    Returns default probability and prediction
    """
    probability = model.predict_proba(processed_df)[:, 1][0]
    prediction = model.predict(processed_df)[0]
    return probability, prediction