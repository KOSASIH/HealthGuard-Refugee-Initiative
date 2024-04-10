class TelemedicineIntegration:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.telemedicine.com/v1"

    def get_patient_data(self, patient_id):
        """
        Get the patient data from the telemedicine system.

        Args:
        - patient_id: The ID of the patient to get data for.

        Returns:
        A dictionary containing the patient data.
        """
        url = f"{self.base_url}/patients/{patient_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def send_alert(self, patient_id, message):
        """
        Send an alert to the telemedicine system.

        Args:
        - patient_id: The ID of the patient to send the alert for.
        - message: The message to send in the alert.
        """
        url = f"{self.base_url}/alerts"
        data = {
            "patient_id": patient_id,
            "message": message
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
