# func/run_precision_medicine_algorithms.py

from bci_refugee_initiative.func.Precision_Medicine_Algorithms import precision_medicine_algorithms

# Define the path to the precision medicine data file
data_path = "precision_medicine_data.csv"

# Run the precision medicine algorithms
metrics = precision_medicine_algorithms(data_path)

# Print the evaluation metrics for the precision medicine algorithms
print(metrics)
