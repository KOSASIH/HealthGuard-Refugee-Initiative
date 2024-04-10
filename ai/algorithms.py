from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

def logistic_regression(**kwargs):
    """
    Create a logistic regression model.

    Keyword arguments:
    - **kwargs: Any keyword arguments to pass to the LogisticRegression constructor.

    Returns:
    A LogisticRegression model.
    """
    return LogisticRegression(**kwargs)

def random_forest_classifier(**kwargs):
"""
    Create a random forest classifier.

    Keyword arguments:
    - **kwargs: Any keyword arguments to pass to the RandomForestClassifier constructor.

    Returns:
    A RandomForestClassifier model.
    """
    return RandomForestClassifier(**kwargs)

def support_vector_machine(**kwargs):
    """
Create a support vector machine classifier.

    Keyword arguments:
    - **kwargs: Any keyword arguments to pass to the SVC constructor.

    Returns:
    A SVC model.
    """
    return SVC(**kwargs)
