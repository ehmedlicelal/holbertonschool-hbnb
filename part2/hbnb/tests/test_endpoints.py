import unittest
from app import create_app

class TestHbnbEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up the test client before each test."""
        self.app = create_app()
        self.client = self.app.test_client()

    # --- User Tests ---
    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("jane.doe@example.com", response.get_data(as_text=True))

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "not-an-email"
        })
        self.assertEqual(response.status_code, 400)

    # --- Amenity Tests ---
    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.assertEqual(response.status_code, 201)

    # --- Place Tests ---
    def test_create_place_invalid_coords(self):
        # We try to create a place with an invalid latitude (100)
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid Place",
            "price": 100.0,
            "latitude": 100.0,
            "longitude": 0.0,
            "owner_id": "any-id"
        })
        # Should be 400 because owner won't be found OR coords are wrong
        self.assertEqual(response.status_code, 400)

    def test_get_non_existent_user(self):
        response = self.client.get('/api/v1/users/invalid-uuid')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()