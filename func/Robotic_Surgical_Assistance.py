import cv2
import mediapipe as mp
import numpy as np
import time
import torch
import math
from utils import transform_to_3d

def capture_webcam_frame():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

def process_pose_landmarks(landmarks):
    shoulder_left = landmarks[5]
    shoulder_right = landmarks[6]
    elbow_left = landmarks[7]
    elbow_right = landmarks[8]
    wrist_left = landmarks[9]
    wrist_right = landmarks[10]

    # Compute the 3D positions of the landmarks
    shoulder_left_3d = transform_to_3d(shoulder_left)
    shoulder_right_3d = transform_to_3d(shoulder_right)
    elbow_left_3d = transform_to_3d(elbow_left)
    elbow_right_3d = transform_to_3d(elbow_right)
    wrist_left_3d = transform_to_3d(wrist_left)
    wrist_right_3d = transform_to_3d(wrist_right)

    return shoulder_left_3d, shoulder_right_3d, elbow_left_3d, elbow_right_3d, wrist_left_3d, wrist_right_3d

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

def control_robotic_arm(pose_landmarks):
    shoulder_left_3d, shoulder_right_3d, elbow_left_3d, elbow_right_3d, wrist_left_3d, wrist_right_3d = process_pose_landmarks(pose_landmarks)

    # Compute the distances between the shoulder, elbow, and wrist points
    shoulder_to_elbow_left = calculate_distance(shoulder_left_3d, elbow_left_3d)
    shoulder_to_elbow_right = calculate_distance(shoulder_right_3d, elbow_right_3d)
    elbow_to_wrist_left = calculate_distance(elbow_left_3d, wrist_left_3d)
    elbow_to_wrist_right = calculate_distance(elbow_right_3d, wrist_right_3d)

    # Adjust the robotic arm's joint angles based on the computed distances
    # This is a simplified version and may need to be adjusted based on your specific robotic arm hardware and calibration
    joint_angles = []
    joint_angles.append(math.degrees(math.acos((shoulder_to_elbow_left ** 2 + shoulder_to_elbow_right ** 2 - elbow_to_wrist_left ** 2) / (2 * shoulder_to_elbow_left * shoulder_to_elbow_right))))
    joint_angles.append(math.degrees(math.acos((shoulder_to_elbow_left ** 2 + shoulder_to_elbow_right ** 2 - elbow_to_wrist_right ** 2) / (2 * shoulder_to_elbow_left * shoulder_to_elbow_right))))

    return joint_angles

def robotic_surgical_assistance(model, pose_estimator):
    for frame in capture_webcam_frame():
        # Estimate the pose landmarks using MediaPipe
        pose_landmarks = pose_estimator(frame)

        # Calculate the joint angles for the robotic arm based on the pose landmarks
        joint_angles = control_robotic_arm(pose_landmarks)

        # Control the robotic arm using the joint angles
        # This part is hardware-specific and depends on the actual robotic arm hardware and interface you are using

        # Render the estimated pose landmarks on the frame
        for landmark in pose_landmarks:
            cv2.circle(frame, (int(landmark[0]), int(landmark[1])), 5, (255, 0, 0), cv2.FILLED)

        # Display the frame
        cv2.imshow('Robotic Surgical Assistance', frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy the window
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Load the pose estimation model
    model = tf.keras.models.load_model('pose_model.h5')

    # Initialize the pose estimator with the pose estimation model
    pose_estimator = MediaPipePoseEstimator(model)

    # Run the robotic surgical assistance application
    robotic_surgical_assistance(model, pose_estimator)

if __name__ == '__main__':
    main()
