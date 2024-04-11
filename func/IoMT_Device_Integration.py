import json

import requests


def get_device_data(device_id):
    """
    Retrieve data from a specified IoMT device.

    Args:
    device_id (str): The unique identifier of the IoMT device.

    Returns:
    dict: A dictionary containing the data from the IoMT device.
    """
    # Make a GET request to the HealthGuard API to retrieve data from the specified IoMT device
    response = requests.get(f"https://api.healthguard.com/devices/{device_id}/data")

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Return the data as a dictionary
        return data
    else:
        # If the request was not successful, return an error message
        return {
            "error": f"Failed to retrieve data from device {device_id}. Status code: {response.status_code}"
        }


def send_alert(device_id, message):
    """
    Send an alert to the HealthGuard system for a specified IoMT device.

    Args:
    device_id (str): The unique identifier of the IoMT device.
    message (str): The message to be sent as an alert.

    Returns:
    bool: True if the alert was sent successfully, False otherwise.
    """
    # Make a POST request to the HealthGuard API to send an alert for the specified IoMT device
    response = requests.post(
        f"https://api.healthguard.com/devices/{device_id}/alerts",
        json={"message": message},
    )

    # Check if the request was successful
    if response.status_code == 201:
        # If the alert was sent successfully, return True
        return True
    else:
        # If the request was not successful, return False
        return False


def integrate_device(device_id):
    """
    Integrate a specified IoMT device into the HealthGuard system.

    Args:
    device_id (str): The unique identifier of the IoMT device.

    Returns:
    bool: True if the device was integrated successfully, False otherwise.
    """
    # Make a POST request to the HealthGuard API to integrate the specified IoMT device
    response = requests.post(
        f"https://api.healthguard.com/devices", json={"id": device_id}
    )

    # Check if the request was successful
    if response.status_code == 201:
        # If the device was integrated successfully, return True
        return True
    else:
        # If the request was not successful, return False
        return False


def main():
    # Integrate a new IoMT device into the HealthGuard system
    device_id = "1234567890"
    if integrate_device(device_id):
        print(
            f"Device {device_id} has been successfully integrated into the HealthGuard system."
        )
    else:
        print(f"Failed to integrate device {device_id} into the HealthGuard system.")

    # Retrieve data from the IoMT device
    data = get_device_data(device_id)
    if data["error"]:
        print(data["error"])
    else:
        print(f"Data from device {device_id}: {data}")

    # Send an alert to the HealthGuard system for the IoMT device
    message = "Urgent: Refugee health status has changed significantly."
    if send_alert(device_id, message):
        print(f"Alert sent to HealthGuard system for device {device_id}: {message}")
    else:
        print(
            f"Failed to send alert to HealthGuard system for device {device_id}: {message}"
        )


if __name__ == "__main__":
    main()
