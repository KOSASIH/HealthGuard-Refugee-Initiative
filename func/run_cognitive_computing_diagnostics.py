# func/run_cognitive_computing_diagnostics.py

from bci_refugee_initiative.func.Cognitive_Computing_Diagnostics import cognitive_computing_diagnostics

# Define the path to the medical text data file
data_path = "medical_text_data.csv"

# Run the cognitive computing diagnostics
metrics = cognitive_computing_diagnostics(data_path)

# Print the evaluation metrics for the cognitive computing diagnostics
print(metrics)
