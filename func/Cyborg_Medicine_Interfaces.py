import threading
import time

import cyborg
import cyborg.actuators
import cyborg.core
import cyborg.devices
import cyborg.interfaces
import cyborg.sensors
import numpy as np


def connect_cyborg_interface(interface_type, interface_params):
    """
    Function to connect to a cyborg interface.

    Args:
        interface_type (str):
                            The type of cyborg interface to connect to.
                            Options: 'sensor', 'actuator', 'device'.
        interface_params (dict):
                                A dictionary of parameters for the interface.

    Returns:
        interface (object):
                        The connected cyborg interface.
    """

    # Connect to the interface
    if interface_type == "sensor":
        interface = cyborg.sensors.Sensor(**interface_params)
    elif interface_type == "actuator":
        interface = cyborg.actuators.Actuator(**interface_params)
    elif interface_type == "device":
        interface = cyborg.devices.Device(**interface_params)
    else:
        raise ValueError("Invalid interface type")

    # Initialize the interface
    interface.initialize()

    return interface


def read_sensor_data(interface):
    """
    Function to read data from a cyborg sensor interface.

    Args:
        interface (object):
                        The connected cyborg sensor interface.

    Returns:
        data (numpy array):
                            The sensor data.
    """

    # Read data from the sensor interface
    data = interface.read()

    return data


def write_actuator_command(interface, command):
    """
    Function to write a command to a cyborg actuator interface.

    Args:
        interface (object):
                        The connected cyborg actuator interface.
        command (numpy array):
                            The command to write to the actuator.
    """

    # Write the command to the actuator interface
    interface.write(command)


def control_cyborg_device(interface, command_function, data_function, interval=0.1):
    """
    Function to control a cyborg device using a command function and data function.

    Args:
        interface (object):
                        The connected cyborg device interface.
        command_function (function):
                                A function to generate a command based on the sensor data.
                                The function should take a numpy array of sensor data as input and return a numpy array of command values.
        data_function (function):
                                A function to extract sensor data from the cyborg sensor interface.
                                The function should take no input and return a numpy array of sensor data.
        interval (float):
                        The interval between each command and data update.

    Returns:
        None
    """

    # Start a thread to continuously update the command
    def update_command():
        while True:
            # Read sensor data
            data = data_function()

            # Generate a command based on the sensor data
            command = command_function(data)

            # Write the command to the actuator interface
            write_actuator_command(interface, command)

            # Wait for the next update
            time.sleep(interval)

    threading.Thread(target=update_command).start()


# Example usage
interface_params = {"name": "example_interface", "port": "/dev/ttyACM0"}
interface = connect_cyborg_interface("device", interface_params)


def command_function(data):
    # Example command function that generates a command based on the sensor data
    return np.array([np.mean(data)])


def data_function():
    # Example data function that extracts sensor data from the cyborg sensor interface
    return read_sensor_data(interface)


control_cyborg_device(interface, command_function, data_function)
