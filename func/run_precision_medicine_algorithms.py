# func/run_precision_medicine_algorithms.py

import os
import sys
import time
import numpy as np
import pandas as pd
from bci_refugee_initiative.func.Precision_Medicine_Algorithms import precision_medicine_algorithms

# Define the path to the precision medicine data file
data_path = "precision_medicine_data.csv"

# Run the precision medicine algorithms
metrics = precision_medicine_algorithms(data_path)

# Print the evaluation metrics for the precision medicine algorithms
print(metrics)
