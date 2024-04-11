import json
import os

import pandas as pd


def load_genetic_data(data_dir):
    """
    Load raw genetic data from disk.

    Parameters:
    data_dir (str): Path to directory containing raw genetic data.

    Returns:
    pd.DataFrame: Raw genetic data.
    """
    raw_data_path = os.path.join(data_dir, "raw", "genetic_data.csv")
    raw_data = pd.read_csv(raw_data_path)
    return raw_data


def process_genetic_data(raw_data):
    """
    Process raw genetic data into interim data.

    Parameters:
    raw_data (pd.DataFrame): Raw genetic data.

    Returns:
    pd.DataFrame: Interim genetic data.
    """
    interim_data = raw_data.copy()
    # Example processing step: Extract relevant columns
    interim_data = interim_data[["RefugeeID", "Chromosome", "Position", "Genotype"]]
    return interim_data


def analyze_genetic_data(interim_data):
    """
    Analyze interim genetic data to identify potential health risks and personalized treatment options.

    Parameters:
    interim_data (pd.DataFrame): Interim genetic data.

    Returns:
    dict: Analysis results, including potential health risks and personalized treatment options.
    """
    analysis_results = {}
    # Example analysis step: Calculate allele frequencies
    allele_freqs = interim_data["Genotype"].value_counts(normalize=True)
    analysis_results["AlleleFrequencies"] = allele_freqs.to_dict()
    # Example analysis step: Identify potential health risks
    risk_genotypes = ["0/1", "1/1"]
    health_risks = interim_data[interim_data["Genotype"].isin(risk_genotypes)]
    analysis_results["HealthRisks"] = health_risks[
        ["RefugeeID", "Chromosome", "Position"]
    ].to_dict("records")
    # Example analysis step: Identify personalized treatment options
    treatment_genotypes = ["1/2"]
    treatment_options = interim_data[interim_data["Genotype"].isin(treatment_genotypes)]
    analysis_results["TreatmentOptions"] = treatment_options[
        ["RefugeeID", "Chromosome", "Position"]
    ].to_dict("records")
    return analysis_results


def save_analysis_results(analysis_results, data_dir):
    """
    Save analysis results to disk.

    Parameters:
    analysis_results (dict): Analysis results.
    data_dir (str): Path to directory for saving analysis results.
    """
    processed_data_path = os.path.join(
        data_dir, "processed", "genetic_analysis_results.json"
    )
    with open(processed_data_path, "w") as f:
        json.dump(analysis_results, f)
