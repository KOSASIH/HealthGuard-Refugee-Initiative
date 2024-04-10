import unittest
import requests

class TestFrontend(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5000"

    def test_get_health_data(self):
        # Send a GET request to the frontend to get the health data
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected HTML
        self.assertIn(b"<h1>HealthGuard Refugee Initiative</h1>", response.content)
        self.assertIn(b"<button id='get-health-data-btn'>Get Health Data</button>", response.content)

    def test_get_health_data_api(self):
        # Send a GET request to the backend API to get the health data
        response = requests.get(f"{self.base_url}/api/health-data")
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected JSON
        data = response.json()
        self.assertIn("heart_rate", data)
        self.assertIn("blood_pressure", data)
        self.assertIn("temperature", data)

    def test_post_health_data_api(self):
        # Send a POST request to the backend API to create a new health data record
        data = {
            "heart_rate": 80,
            "blood_pressure": "120/80",
            "temperature": 37.5
        }
        response = requests.post(f"{self.base_url}/api/health-data", json=data)
        self.assertEqual(response.status_code, 201)

        # Check that the new health data record was created
        response = requests.get(f"{self.base_url}/api/health-data")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["heart_rate"], 80)
        self.assertEqual(data["blood_pressure"], "120/80")
        self.assertEqual(data["temperature"], 37.5)

if __name__ == "__main__":
    unittest.main()
