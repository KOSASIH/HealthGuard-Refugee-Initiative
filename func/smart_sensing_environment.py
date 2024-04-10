import time
import random
import numpy as np
import matplotlib.pyplot as plt

# Define a function to simulate sensor data
def simulate_sensor_data(num_sensors, num_samples):
    """
    Simulates sensor data for a set of sensors over a period of time.

    Args:
        num_sensors (int): Number of sensors to simulate.
        num_samples (int): Number of samples to generate for each sensor.

    Returns:
        ndarray: A 2D array of shape (num_sensors, num_samples) containing simulated sensor data.
    """
    sensor_data = np.zeros((num_sensors, num_samples))
    for i in range(num_sensors):
        sensor_data[i] = np.random.normal(loc=50 + 10 * np.sin(np.linspace(0, 2 * np.pi, num_samples)), scale=5, size=num_samples)
    return sensor_data

# Define a function to visualize sensor data
def visualize_sensor_data(sensor_data, num_sensors, num_samples):
    """
    Visualizes sensor data for a set of sensors over time.

    Args:
        sensor_data (ndarray): A 2D array of shape (num_sensors, num_samples) containing sensor data.
        num_sensors (int): Number of sensors.
        num_samples (int): Number of samples.
    """
    fig, axs = plt.subplots(num_sensors, 1, figsize=(10, 5))
    for i in range(num_sensors):
        axs[i].plot(sensor_data[i])
        axs[i].set_ylabel('Sensor {}'.format(i))
        axs[i].set_xlabel('Sample')
    plt.show()

# Define a function to analyze sensor data for anomalies
def analyze_sensor_data(sensor_data, threshold=10):
    """
Analyzes sensor data for anomalies based on a threshold value.

    Args:
        sensor_data (ndarray): A 2D array of shape (num_sensors, num_samples) containing sensor data.
        threshold (int): Threshold value for anomaly detection.

    Returns:
        list: List of tuples containing the indices of any detected anomalies.
    """
    anomalies = []
    for i in range(sensor_data.shape[0]):
        sensor_data_i = sensor_data[i]
        for j in range(sensor_data_i.size):
            if np.abs(sensor_data_i[j] - np.mean(sensor_data_i)) > threshold:
                anomalies.append((i, j))
    return anomalies

# Define a function to simulate IoT device behavior
def simulate_iot_device(name, sensor_data):
    """
    Simulates the behavior of an IoT device based on its sensor readings.

    Args:
        name (str): Name of the IoT device.
        sensor_data (ndarray): A 2D array of shape (num_sensors, num_samples) containing sensor data.
    """
    print('IoT device {} reading sensor data...'.format(name))
    time.sleep(1)
    sensor_readings = {}
    for i in range(sensor_data.shape[0]):
        sensor_readings[i] = sensor_data[i][-1]
    print('IoT device {} readings: {}'.format(name, sensor_readings))

# Define a function to simulate a sensor network
def simulate_sensor_network(num_sensors, num_samples):
    """
    Simulates a sensor network by generating sensor data and simulating IoT device behavior.

    Args:
        num_sensors (int): Number of sensors.
        num_samples (int): Number of samples.
    """
    sensor_data = simulate_sensor_data(num_sensors, num_samples)
    visualize_sensor_data(sensor_data, num_sensors, num_samples)
    anomalies = analyze_sensor_data(sensor_data)
    print('Anomalies detected:')
    for i, j in anomalies:
        print('Sensor {} at sample {}'.format(i, j))
    print()
    num_devices = random.randint(1, 3)
    devices = []
    for i in range(num_devices):
        device_name = 'Device {}'.format(i)
        devices.append(device_name)
        simulate_iot_device(device_name, sensor_data)

# Example usage
num_sensors = 10
num_samples = 100
simulate_sensor_network(num_sensors, num_samples)
