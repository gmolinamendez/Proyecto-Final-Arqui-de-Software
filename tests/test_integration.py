import unittest
from main import app
from database import database
from sqlalchemy import text

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.db = database()

    def test_full_event_flow(self):
        """Integration Test: Create an event, verify it exists, then delete it to keep DB clean."""
        # 1. Crear un evento POST /api/events
        payload = {
            "name": "Integration Test Event",
            "date": "2026-10-10",
            "location": "Virtual Integration"
        }
        response = self.client.post('/api/events', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        event_id = data.get("id")
        self.assertIsNotNone(event_id)

        # 2. Consultar el evento GET /api/events/<id> para verificar lectura exitosa
        get_response = self.client.get(f'/api/events/{event_id}')
        self.assertEqual(get_response.status_code, 200)
        get_data = get_response.get_json()
        self.assertEqual(get_data.get("name"), "Integration Test Event")
        self.assertEqual(get_data.get("location"), "Virtual Integration")

        # 3. Eliminar el evento DELETE /api/events/<id> para limpiar DB (End-to-End real)
        delete_response = self.client.delete(f'/api/events/{event_id}')
        self.assertEqual(delete_response.status_code, 200)

        # 4. Verificar que se haya eliminado correctamente de la base de datos
        verify_response = self.client.get(f'/api/events/{event_id}')
        self.assertEqual(verify_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
