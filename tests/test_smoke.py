import unittest
from flask import current_app
from database import test_connection
from main import app

class SmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_database_connection(self):
        """Smoke Test: Verify database connection works."""
        # Using the test_connection method from database.py
        is_connected = test_connection()
        self.assertTrue(is_connected, "Database connection failed")

    def test_users_endpoint(self):
        """Smoke Test: Verify /api/users endpoint is responding."""
        # Assuming '/api/users' returns a 200 OK
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200, "Users endpoint is not reachable")

    def test_events_endpoint(self):
        """Smoke Test: Verify /api/events endpoint is responding."""
        response = self.client.get('/api/events')
        self.assertEqual(response.status_code, 200, "Events endpoint is not reachable")

if __name__ == '__main__':
    unittest.main()
