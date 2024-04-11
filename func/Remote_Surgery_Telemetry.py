import cv2
import numpy as np
import time

def start_telemetry_stream(video_source, telemetry_port):
    """
    Start a remote surgery telemetry stream from the specified video source.

    Args:
    video_source (str): The source of the video stream (e.g. a camera index or URL).
    telemetry_port (int): The port number to send the telemetry data to.

    Returns:
    None
    """
    # Open the video stream
    cap = cv2.VideoCapture(video_source)

    # Check if the stream was opened successfully
    if not cap.isOpened():
        print(f"Error: Unable to open video source {video_source}")
        return

    # Set the frame rate of the stream
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Initialize the telemetry socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', telemetry_port))
    s.listen(1)

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("Error: Unable to read frame from video stream")
            break

        # Resize the frame for telemetry
        frame = cv2.resize(frame, (224, 224))

        # Convert the frame to a byte array for telemetry
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

        # Send the telemetry data to the specified port
        conn, addr = s.accept()
        conn.sendall(frame_bytes)
        conn.close()

    # Release the video stream
    cap.release()

# Example usage:
if __name__ == '__main__':
    video_source = 0  # Use the first available camera
    telemetry_port = 12345  # Use port 12345 for telemetry
    start_telemetry_stream(video_source, telemetry_port)
