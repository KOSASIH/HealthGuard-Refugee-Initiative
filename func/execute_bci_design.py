# func/execute_bci_design.py

import os
import sys
import numpy as np
import mne
from bci_refugee_initiative.func.Brain-Computer_Interface_Control import create_bci_system, load_bci_data, preprocess_bci_data, extract_bci_features, train_bci_model, execute_bci_design

# Load the trained BCI model
model = np.load("trained_bci_model.npy", allow_pickle=True).item()

# Load the BCI data
bci_data = load_bci_data("bci_data.txt")

# Preprocess the BCI data
preprocessed_data = preprocess_bci_data(bci_data["raw_data"])

# Extract the BCI features
features = extract_bci_features(preprocessed_data)

# Define the BCI design
design = {
    "features": features,
    "labels": bci_data["labels"]
}

# Create the BCI system
bci_system = create_bci_system()

# Execute the BCI design
execute_bci_design(bci_system, design, model)
