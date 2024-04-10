import unittest
import numpy as np
from ai.models import HealthMonitoringModel

class TestAI(unittest.TestCase):
    def setUp(self):
        self.model = HealthMonitoringModel()

    def test_train_model(self):
        # Test training the model with some sample data
        X_train = np.array([[80, 120, 80], [90, 130, 70], [70, 110, 90]])
        y_train = np.array([1, 0, 0])
        self.model.train_model(X_train, y_train)

        # Check that the model was trained with the correct number of samples and features
        self.assertEqual(self.model.X_train.shape[0], 3)
        self.assertEqual(self.model.X_train.shape[1], 3)
        self.assertEqual(self.model.y_train.shape[0], 3)

    def test_predict(self):
        # Test predicting with some sample data
        X_test = np.array([[80, 120, 80], [90, 130, 70], [70, 110, 90]])
        self.model.X_train = X_test
        self.model.y_train = np.array([1, 0, 0])
        self.model.model = None
        self.model.train_model(X_test, self.model.y_train)

        # Check that the model predicts the correct labels for the test data
        y_pred = self.model.predict(X_test)
        self.assertEqual(y_pred.tolist(), [1, 0, 0])

if __name__ == "__main__":
    unittest.main()
