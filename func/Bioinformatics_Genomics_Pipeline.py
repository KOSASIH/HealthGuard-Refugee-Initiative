import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as sch
import seaborn as sns
import sklearn.decomposition
import sklearn.linear_model
import sklearn.metrics


def load_genomic_data(file_path):
    """
    Load genomic data from a file.

    Parameters:
    file_path (str): Path to the genomic data file.

    Returns:
    pandas.DataFrame: A DataFrame containing the genomic data.
    """
    genomic_data = pd.read_csv(file_path, sep="\t")

    return genomic_data


def preprocess_genomic_data(genomic_data):
    """
    Preprocess genomic data for downstream analysis.

    Parameters:
    genomic_data (pandas.DataFrame): A DataFrame containing the genomic data.

    Returns:
    pandas.DataFrame: A preprocessed DataFrame containing the genomic data.
    """
    # Remove rows with missing values
    genomic_data = genomic_data.dropna()

    # Filter for specific genetic markers of interest
    genomic_data = genomic_data[
        genomic_data["Marker"].isin(["Marker1", "Marker2", "Marker3"])
    ]

    # Convert categorical variables to numerical variables
    genomic_data["Disease"] = pd.Categorical(genomic_data["Disease"]).codes

    # Normalize numerical variables
    genomic_data[["Marker1", "Marker2", "Marker3"]] = (
        genomic_data[["Marker1", "Marker2", "Marker3"]]
        - genomic_data[["Marker1", "Marker2", "Marker3"]].mean()
    ) / genomic_data[["Marker1", "Marker2", "Marker3"]].std()

    return genomic_data


def exploratory_data_analysis(genomic_data):
    """
    Perform exploratory data analysis on genomic data.

    Parameters:
    genomic_data (pandas.DataFrame): A preprocessed DataFrame containing the genomic data.

    Returns:
    None
    """
    # Plot the distribution of each genetic marker
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    sns.histplot(genomic_data["Marker1"], ax=axs[0])
    sns.histplot(genomic_data["Marker2"], ax=axs[1])
    sns.histplot(genomic_data["Marker3"], ax=axs[2])
    plt.show()

    # Plot the correlation matrix of the genetic markers
    sns.heatmap(
        genomic_data[["Marker1", "Marker2", "Marker3"]].corr(),
        annot=True,
        cmap="coolwarm",
    )
    plt.show()

    # Perform hierarchical clustering on the genetic markers
    Z = sch.linkage(genomic_data[["Marker1", "Marker2", "Marker3"]], method="ward")
    fig = plt.figure(figsize=(10, 5))
    dn = sch.dendrogram(Z)
    plt.show()


def dimensionality_reduction(genomic_data):
    """
    Perform dimensionality reduction on genomic data using PCA.

    Parameters:
    genomic_data (pandas.DataFrame): A preprocessed DataFrame containing the genomic data.

    Returns:
    numpy.ndarray: The PCA transformed data.
    """
    pca = sklearn.decomposition.PCA(n_components=2)
    pca_transformed_data = pca.fit_transform(
        genomic_data[["Marker1", "Marker2", "Marker3"]]
    )

    return pca_transformed_data


def logistic_regression(genomic_data, pca_transformed_data):
    """
    Perform logistic regression analysis on genomic data using PCA transformed data.

    Parameters:
    genomic_data (pandas.DataFrame): A preprocessed DataFrame containing the genomic data.
    pca_transformed_data (numpy.ndarray): The PCA transformed data.

    Returns:
    None
    """
    logreg = sklearn.linear_model.LogisticRegression()
    logreg.fit(pca_transformed_data, genomic_data["Disease"])

    # Plot the ROC curve
    fpr, tpr, thresholds = sklearn.metrics.roc_curve(
        genomic_data["Disease"], logreg.predict_proba(pca_transformed_data)[:, 1]
    )
    roc_auc = sklearn.metrics.roc_auc_score(
        genomic_data["Disease"], logreg.predict_proba(pca_transformed_data)[:, 1]
    )

    plt.figure()
    plt.plot(
        fpr, tpr, color="darkorange", lw=2, label="ROC curve (area = %0.2f)" % roc_auc
    )
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver Operating Characteristic (ROC) Curve")
    plt.legend(loc="lower right")
    plt.show()


def build_genomic_pipeline(file_path):
    """
    Build a complete genomic data analysis pipeline.

    Parameters:
    file_path (str): Path to the genomic data file.

    Returns:
    None
    """
    genomic_data = load_genomic_data(file_path)
    genomic_data = preprocess_genomic_data(genomic_data)
    exploratory_data_analysis(genomic_data)
    pca_transformed_data = dimensionality_reduction(genomic_data)
    logistic_regression(genomic_data, pca_transformed_data)
