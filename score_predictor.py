# score_predictor.py

import pandas as pd
import joblib

# Load models and scaler once
placement_model = joblib.load("placement_model.pkl")
company_model = joblib.load("company_fit_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_score(input_data):
    """
    input_data: dict from form inputs
    returns: dict with both model predictions
    """
    print(input_data)
    df = pd.DataFrame([input_data])

    # One-hot encode categorical columns if any (like 'Branch')
    df_encoded = pd.get_dummies(df)

    # Ensure all expected features exist (fill missing with 0)
    df_encoded = df_encoded.reindex(columns=scaler.feature_names_in_, fill_value=0)

    # Scale the inputs
    scaled_input = scaler.transform(df_encoded)

    # Predict with both models
    print(scaled_input)
    placement_prediction = placement_model.predict(scaled_input)[0]
    company_prediction = company_model.predict(scaled_input)[0]

    return {
        "placement_readiness": placement_prediction,
        "company_fit": company_prediction
    }


