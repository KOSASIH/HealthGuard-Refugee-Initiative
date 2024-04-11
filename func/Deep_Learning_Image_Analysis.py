import cv2
import keras
import numpy as np
import tensorflow as tf


def load_image(image_path):
    """
    Loads and preprocesses an image.

    Args:
    image_path (str): The path to the image file.

    Returns:
    A preprocessed image tensor.
    """
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = image.astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)
    return image


def build_cnn(num_classes):
    """
    Builds a convolutional neural network.

    Args:
    num_classes (int): The number of output classes.

    Returns:
    A compiled Keras model.
    """
    model = keras.Sequential(
        [
            keras.layers.Conv2D(
                32, (3, 3), activation="relu", input_shape=(224, 224, 3)
            ),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation="relu"),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(128, (3, 3), activation="relu"),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def train_cnn(model, x_train, y_train, x_val, y_val, epochs):
    """
    Trains a convolutional neural network.

    Args:
    model (keras.Model): The model to train.
    x_train (np.ndarray): The training images.
    y_train (np.ndarray): The training labels.
    x_val (np.ndarray): The validation images.
    y_val (np.ndarray): The validation labels.
    epochs (int): The number of training epochs.

    Returns:
    A trained model.
    """
    model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=epochs)
    return model


def predict_image(model, image_path):
    """
    Predicts the class of an image.

    Args:
    model (keras.Model): The trained model.
    image_path (str): The path to the image file.

    Returns:
    The predicted class.
    """
    image = load_image(image_path)
    prediction = model.predict(image)
    return np.argmax(prediction)
