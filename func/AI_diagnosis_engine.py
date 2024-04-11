import pickle

import numpy as np


def load_diagnosis_model():
    """
    Load the pre-trained diagnosis model from disk.

    Returns:
    - model (LogisticRegression): The pre-trained diagnosis model.
    """
    with open("models/diagnosis_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model


def diagnose_condition(biometric_data):
    """
    Diagnose the health condition of a patient based on the given biometric data.

    Args:
    - biometric_data (pandas.DataFrame): A DataFrame containing the biometric data.

    Returns:
    - diagnosis (str): The predicted health condition of the patient.
    """
    model = load_diagnosis_model()

    # Preprocess the biometric data for input into the diagnosis model
    X = biometric_data[["heart_rate", "blood_pressure", "temperature"]].values
    X = (X - np.min(X)) / (np.max(X) - np.min(X))

    # Make a prediction using the diagnosis model
    y_pred = model.predict(X)

    # Return the predicted health condition
    if y_pred[0] == 0:
        diagnosis = "Healthy"
    else:
        diagnosis = "Unhealthy"
    return diagnosis
