
import unittest
import json
from app import app, db
from models import Resource, Prediction

class LifeGuardTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_dashboard_api(self):
        """Test that the dashboard API returns correct structure"""
        response = self.client.get('/api/dashboard')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predictions', data)
        self.assertIn('resources', data)
        self.assertIn('statistics', data)

    def test_database_persistence(self):
        """Test that we can add and retrieve data from DB"""
        with app.app_context():
            res = Resource(resource_type="test_res", total_quantity=100, available_quantity=80)
            db.session.add(res)
            db.session.commit()

            retrieved = Resource.query.filter_by(resource_type="test_res").first()
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.available_quantity, 80)

if __name__ == '__main__':
    unittest.main()
