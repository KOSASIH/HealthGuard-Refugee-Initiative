import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


def train_classifier(features, labels, classifier_type="SVM", kernel="linear"):
    """
    Function to train a classifier using extracted features and corresponding labels.

    Args:
        features (numpy array):
                                The extracted features.
        labels (numpy array):
                                The corresponding labels.
        classifier_type (str):
                                The type of classifier to use.
                                Options: 'SVM', 'Random Forest', 'KNN'.
        kernel (str):
                      The type of kernel to use for SVM.
                      Options: 'linear', 'rbf', 'poly'.

    Returns:
        classifier (object):
                        The trained classifier.
    """

    # Initialize classifier
    if classifier_type == "SVM":
        classifier = SVC(kernel=kernel)
    elif classifier_type == "Random Forest":
        classifier = RandomForestClassifier()
    elif classifier_type == "KNN":
        classifier = KNeighborsClassifier()
    else:
        raise ValueError("Invalid classifier type")

    # Train classifier
    classifier.fit(features, labels)

    return classifier


def predict_labels(classifier, features):
    """
    Function to predict labels using the trained classifier.

    Args:
        classifier (object):
                        The trained classifier.
        features (numpy array):
                                The features to predict labels for.

    Returns:
        labels (numpy array):
                            The predicted labels.
    """

    # Predict labels
    labels = classifier.predict(features)

    return labels


def prioritize_interventions(classifier, features, priority_type="most_severe"):
    """
    Function to prioritize healthcare interventions based on the severity of refugee health conditions and available resources.

    Args:
        classifier (object):
                        The trained classifier.
        features (numpy array):
                                The features to predict labels for.
        priority_type (str):
                            The type of priority to use.
                            Options: 'most_severe', 'most_critical', 'most_effective'.

    Returns:
        prioritized_interventions (list):
                                     The prioritized healthcare interventions.
    """

    # Predict labels
    labels = predict_labels(classifier, features)

    # Prioritize interventions
    if priority_type == "most_severe":
        sorted_labels = sorted(enumerate(labels), key=lambda x: x[1], reverse=True)
    elif priority_type == "most_critical":
        sorted_labels = sorted(
            enumerate(labels), key=lambda x: (x[1], x[0]), reverse=True
        )
    elif priority_type == "most_effective":
        sorted_labels = sorted(
            enumerate(labels), key=lambda x: (x[1], -x[0]), reverse=True
        )
    else:
        raise ValueError("Invalid priority type")

    # Extract prioritized interventions
    prioritized_interventions = [i[0] for i in sorted_labels]

    return prioritized_interventions


# Example usage
classifier = np.random.rand(100, 100)
features = np.random.rand(100, 100)
prioritized_interventions = prioritize_interventions(
    classifier, features, priority_type="most_severe"
)
