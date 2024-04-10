import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

def preprocess_data(X, Y):
    """Preprocess the input data and labels.

    Args:
        X (ndarray): The input data, shape (n_samples, n_features).
        Y (ndarray): The input labels, shape (n_samples, n_labels).

    Returns:
        (tuple) Preprocessed input data and labels.
    """
    # Normalize the input data
    X = (X - np.min(X)) / (np.max(X) - np.min(X))

    # One-hot encode the labels
    Y = tf.keras.utils.to_categorical(Y, num_classes=Y.max() + 1)

    return X, Y

def build_neural_network(input_shape, n_classes):
    """Build a neural network model for health condition diagnosis.

    Args:
        input_shape (tuple): The shape of the input data.
        n_classes (int): The number of output classes.

    Returns:
        (tf.keras.Model) The neural network model.
    """
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=input_shape))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(n_classes, activation='softmax'))

    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model

def train_model(model, X, Y, batch_size=32, epochs=10):
    """Train the neural network model.

    Args:
        model (tf.keras.Model): The neural network model.
        X (ndarray): The input data, shape (n_samples, n_features).
        Y (ndarray): The input labels, shape (n_samples, n_labels).
        batch_size (int): The batch size for training.
        epochs (int): The number of epochs for training.

    Returns:
        (float) The training accuracy of the model.
    """
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    history = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2)

    return history.history['accuracy'][-1]

def predict_health_condition(model, X):
    """Predict the health condition of the input data.

    Args:
        model (tf.keras.Model): The neural network model.
        X (ndarray): The input data, shape (n_samples, n_features).

    Returns:
        (list) The predicted health conditions.
    """
    predictions = model.predict(X)

    return [np.argmax(prediction) for prediction in predictions]

def recommend_intervention(health_condition_predictions):
    """Recommend an appropriate intervention based on the predicted health conditions.

    Args:
        health_condition_predictions (list): The predicted health conditions.

    Returns:
        (str) The recommended intervention.
    """
    interventions = {0: 'Take medication A',
                     1: 'Visit a specialist for condition B',
                     2: 'Undergo a check-up for condition C'}

    return interventions[max(health_condition_predictions, key=health_condition_predictions.count)]
