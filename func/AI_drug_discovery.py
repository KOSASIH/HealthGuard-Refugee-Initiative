import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def load_drug_discovery_data(data_dir):
    """
    Load raw drug discovery data from disk.

    Parameters:
    data_dir (str): Path to directory containing raw drug discovery data.

    Returns:
    pd.DataFrame: Raw drug discovery data.
    """
    raw_data_path = os.path.join(data_dir, "raw", "drug_discovery_data.csv")
    raw_data = pd.read_csv(raw_data_path)
    return raw_data


def process_drug_discovery_data(raw_data):
    """
    Process raw drug discovery data into interim data.

    Parameters:
    raw_data (pd.DataFrame): Raw drug discovery data.

    Returns:
    pd.DataFrame: Interim drug discovery data.
    """
    interim_data = raw_data.copy()
    # Example processing step: Extract relevant columns
    interim_data = interim_data[
        ["CompoundID", "Activity", "MolecularWeight", "LogP", "HBA", "ROTB"]
    ]
    return interim_data


def train_drug_discovery_model(interim_data):
    """
    Train a machine learning model to predict drug activity based on compound features.

    Parameters:
    interim_data (pd.DataFrame): Interim drug discovery data.

    Returns:
    sklearn.ensemble.RandomForestClassifier: Trained machine learning model.
    """
    X = interim_data[["MolecularWeight", "LogP", "HBA", "ROTB"]]
    y = interim_data["Activity"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def save_drug_discovery_model(model, model_dir):
    """
    Save trained machine learning model to disk.

    Parameters:
    model (sklearn.ensemble.RandomForestClassifier): Trained machine learning model.
    model_dir (str): Path to directory for saving trained model.
    """
    model_path = os.path.join(model_dir, "drug_discovery_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)


def load_drug_discovery_model(model_dir):
    """
    Load trained machine learning model from disk.

    Parameters:
    model_dir (str): Path to directory containing trained machine learning model.

    Returns:
    sklearn.ensemble.RandomForestClassifier: Trained machine learning model.
    """
    model_path = os.path.join(model_dir, "drug_discovery_model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


def predict_drug_activity(model, compound_features):
    """
    Predict the activity of a compound based on its features using a trained machine learning model.

    Parameters:
    model (sklearn.ensemble.RandomForestClassifier): Trained machine learning model.
    compound_features (dict): Features of the compound to predict activity for.

    Returns:
    int: Predicted activity of the compound (1: Active, 0: Inactive).
    """
    activity_pred = model.predict([compound_features])[0]
    return activity_pred
