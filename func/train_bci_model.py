# func/train_bci_model.py

import os
import sys
import numpy as np
import mne
from bci_refugee_initiative.func.Brain-Computer_Interface_Control import create_bci_system, load_bci_data, preprocess_bci_data, extract_bci_features, train_bci_model

# Load the BCI data
bci_data = load_bci_data("bci_data.txt")

# Preprocess the BCI data
preprocessed_data = preprocess_bci_data(bci_data["raw_data"])

# Extract the BCI features
features = extract_bci_features(preprocessed_data)

# Train the BCI model
model = train_bci_model(features, bci_data["labels"])

# Save the trained BCI model
np.save("trained_bci_model.npy", model)
