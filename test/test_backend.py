import json
import unittest

from app import create_app
from database import db
from models import HealthData


class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_health_data(self):
        # Create a new health data record
        health_data = HealthData(
            heart_rate=80, blood_pressure="120/80", temperature=37.5
        )
        db.session.add(health_data)
        db.session.commit()

        # Send a GET request to the API to get the health data
        response = self.client.get("/api/health-data")
        data = json.loads(response.data)

        # Check that the response is successful and contains the expected data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["heart_rate"], 80)
        self.assertEqual(data["blood_pressure"], "120/80")
        self.assertEqual(data["temperature"], 37.5)

    def test_post_health_data(self):
        # Send a POST request to the API to create a new health data record
        data = {"heart_rate": 80, "blood_pressure": "120/80", "temperature": 37.5}
        response = self.client.post("/api/health-data", json=data)
        self.assertEqual(response.status_code, 201)

        # Check that the new health data record was created
        health_data = HealthData.query.first()
        self.assertIsNotNone(health_data)
        self.assertEqual(health_data.heart_rate, 80)
        self.assertEqual(health_data.blood_pressure, "120/80")
        self.assertEqual(health_data.temperature, 37.5)


if __name__ == "__main__":
    unittest.main()
