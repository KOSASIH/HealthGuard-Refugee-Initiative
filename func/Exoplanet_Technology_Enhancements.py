import numpy as np
import cv2
import matplotlib.pyplot as plt

def detect_biosignatures(image):
    """
    Detect biosignatures in an image using a machine learning model.

    Args:
    image (numpy.ndarray): A 2D numpy array representing the image.

    Returns:
    dict: A dictionary containing the detected biosignatures and their locations.
    """
    # Load the machine learning model for detecting biosignatures
    model = load_model('biosignature_model.h5')

    # Preprocess the image for input into the model
    image = cv2.resize(image, (224, 224))
    image = image.astype('float32') / 255.0
    image = np.expand_dims(image, axis=0)

    # Make a prediction using the model
    predictions = model.predict(image)

    # Postprocess the predictions to extract the detected biosignatures and their locations
    biosignatures = {}
    for i, prediction in enumerate(predictions[0]):
        if prediction > 0.5:
            x, y, w, h = get_bbox(i)
            biosignatures[f'biosignature_{i}'] = {'location': (x, y, w, h), 'confidence': float(prediction)}

    return biosignatures

def get_bbox(class_id):
    """
    Get the bounding box for a given class ID.

    Args:
    class_id (int): The class ID for the biosignature.

    Returns:
    tuple: A tuple containing the bounding box coordinates (x, y, width, height).
    """
    # Define the bounding boxes for each class ID
    bboxes = [
        (0, 0, 32, 32), (32, 0, 32, 32), (64, 0, 32, 32), (96, 0, 32, 32),
        (0, 32, 32, 32), (32, 32, 32, 32), (64, 32, 32, 32), (96, 32, 32, 32),
        (0, 64, 32, 32), (32, 64, 32, 32), (64, 64, 32, 32), (96, 64, 32, 32),
        (0, 96, 32, 32), (32, 96, 32, 32), (64, 96, 32, 32), (96, 96, 32, 32)
    ]

    # Return the bounding box for the given class ID
    return bboxes[class_id]

def visualize_biosignatures(image, biosignatures):
    """
    Visualize the detected biosignatures in an image.

    Args:
    image (numpy.ndarray): A 2D numpy array representing the image.
    biosignatures (dict): A dictionary containing the detected biosignatures and their locations.

    Returns:
    None
    """
    # Loop through the detected biosignatures and draw bounding boxes around them
    for biosignature in biosignatures.values():
        x, y, w, h = biosignature['location']
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image with the detected biosignatures
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

# Example usage:
image_path = 'example_image.jpg'
image = cv2.imread(image_path)
biosignatures =detect_biosignatures(image)
visualize_biosignatures(image, biosignatures)
