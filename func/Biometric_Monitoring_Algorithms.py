import cv2
import numpy as np
import os

def detect_facial_landmarks(image):
    """
    Detect facial landmarks in an image using the dlib library.

    Args:
    image (numpy.ndarray): The input image in grayscale format.

    Returns:
    list: A list of (x, y) coordinates representing the facial landmarks.
    """
    detector = cv2.face.createFacelandmarkDetectorML()
    faces, landmarks = detector.detect(image, landmarkIdx=cv2.face.FACELANDMARK_5_POINTS)
    return landmarks[0].tolist()

def extract_heart_rate(video_file):
    """
    Extract heart rate information from a video file using the OpenCV library.

    Args:
    video_file (str): The path to the input video file.

    Returns:
    float: The estimated heart rate in beats per minute (bpm).
    """
    cap = cv2.VideoCapture(video_file)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    success, frame = cap.read()
    r, g, b = cv2.split(frame)
    r_mean = np.mean(r)
    g_mean = np.mean(g)
    b_mean = np.mean(b)
    cap.release()

    # Calculate the heart rate using the red, green, and blue color channels
    r_diff = r_mean - np.mean(r)
    g_diff = g_mean - np.mean(g)
    b_diff = b_mean - np.mean(b)
    heart_rate = 60 * (r_diff + g_diff + b_diff) / (3 * total_frames)

    return heart_rate

def detect_emotion(image):
    """
    Detect the emotion in an image using the OpenCV library.

    Args:
    image (numpy.ndarray): The input image in grayscale format.

    Returns:
    str: The detected emotion.
    """
    face_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return "Neutral"

    (x, y, w, h) = faces[0]
    face = image[y:y+h, x:x+w]
    face = cv2.resize(face, (96, 96))
    face = face.astype("float") / 255.0
    face = np.expand_dims(face, axis=0)

    # Load the pre-trained emotion model
    model = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000_fp16.caffemodel")

    # Perform emotion detection
    preds = model.forward()
    emotion = np.argmax(preds[0])

    # Map the emotion index to the corresponding emotion label
    emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
    emotion_label = emotion_labels[emotion]

    return emotion_label

def monitor_biometrics(video_file):
    """
    Monitor the biometrics of a person in a video file.

    Args:
    video_file (str): The path to the input video file.

    Returns:
    dict: A dictionary containing the detected facial landmarks, heart rate, and emotion.
    """
    cap = cv2.VideoCapture(video_file)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
   frame_count = 0
    landmarks_list = []
    heart_rate_list = []
    emotion_list = []

    while True:
        success, frame = cap.read()
        if not success:
            break

        if frame_count % 10 == 0:
            landmarks = detect_facial_landmarks(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            landmarks_list.append(landmarks)

        if frame_count % 30 == 0:
            heart_rate = extract_heart_rate(video_file)
            heart_rate_list.append(heart_rate)

        if frame_count % 60 == 0:
            face = cv2.resize(frame, (96, 96))
            face = face.astype("float") / 255.0
            face = np.expand_dims(face, axis=0)
            emotion = detect_emotion(face)
            emotion_list.append(emotion)

        frame_count += 1

    cap.release()

    # Calculate the average heart rate, emotion, and facial landmarks
    avg_heart_rate = np.mean(heart_rate_list)
    avg_emotion = np.mean(emotion_list)
    avg_emotion_label = emotion_labels[int(avg_emotion)]
    avg_landmarks = np.mean(landmarks_list, axis=0)

    # Convert the average landmarks from a list of tuples to a NumPy array
    avg_landmarks = np.array(avg_landmarks)

    # Return the results as a dictionary
    results = {
        'avg_heart_rate': avg_heart_rate,
        'avg_emotion': avg_emotion_label,
        'avg_landmarks': avg_landmarks.tolist()
    }

    return results

# Example usage:
results = monitor_biometrics('input.mp4')
print(results)
