import requests
import json

def schedule_consultation(patient_id, provider_id, date, time):
    """
    Schedule a consultation for the given patient with the given provider on the given date and time.

    Args:
    - patient_id (str): The ID of the patient.
    - provider_id (str): The ID of the provider.
    - date (str): The date of the consultation in YYYY-MM-DD format.
    - time (str): The time of the consultation in HH:MM:SS format.

    Returns:
    - consultation_id (str): The ID of the scheduled consultation.
    """
    url = "https://api.telemedicine.com/schedule_consultation"
    data = {
        "patient_id": patient_id,
        "provider_id": provider_id,
        "date": date,
        "time": time
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    consultation_id = response.json()["consultation_id"]
    return consultation_id

def conduct_consultation(consultation_id, patient_video_url, provider_video_url):
    """
    Conduct a consultation for the given consultation ID, with the patient and provider located at the given video URLs.

    Args:
    - consultation_id (str): The ID of the consultation.
    - patient_video_url (str): The URL of the video stream for the patient.
   - provider_video_url (str): The URL of the video stream for the provider.

    Returns:
    - None
    """
    url = f"https://api.telemedicine.com/conduct_consultation?consultation_id={consultation_id}"
    data = {
        "patient_video_url": patient_video_url,
        "provider_video_url": provider_video_url
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, data=json.dumps(data), headers=headers)

def end_consultation(consultation_id):
    """
    End the consultation with the given consultation ID.

    Args:
    - consultation_id (str): The ID of the consultation.

    Returns:
    - None
    """
    url = f"https://api.telemedicine.com/end_consultation?consultation_id={consultation_id}"
    requests.get(url)

def get_consultation_history(patient_id):
    """
    Get the consultation history for the given patient ID.

    Args:
    - patient_id (str): The ID of the patient.

    Returns:
    - consultation_history (list): A list of dictionaries containing information about each consultation in the patient's history.
    """
    url = f"https://api.telemedicine.com/get_consultation_history?patient_id={patient_id}"
    response = requests.get(url)
    consultation_history = response.json()["consultation_history"]
    return consultation_history
