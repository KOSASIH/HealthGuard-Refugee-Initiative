import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class HealthMonitoringModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = None

    def load_data(self):
        # Load the health data from a CSV file
        data = pd.read_csv(self.data_path)

        # Preprocess the data as necessary
        # ...

        # Split the data into features (X) and labels (y)
        X = data.drop('label', axis=1)
        y = data['label']

        return X, y

    def train_model(self):
        # Load the data
        X, y = self.load_data()

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model using a Random Forest Classifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model on the testing set
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(classification_report(y_test, y_pred))

        return accuracy

    def predict(self, X):
        # Make predictions on new data using the trained model
        if self.model is None:
            raise ValueError("Model not trained")

        return self.model.predict(X)
