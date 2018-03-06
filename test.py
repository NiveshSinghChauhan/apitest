from flask_testing import TestCase
from geoapi import app
import unittest

class BaseTestCase(TestCase):

    def create_app(self):
        return app


class APITest(BaseTestCase):

    # post location test when all property are not given
    def test_post_location_error_propertyNotGiven(self):
        response = self.client.post('post_location')
        self.assertIn(b'Error, Required Popety are not given', response.data)

    # post location test when pincode already exist
    def test_post_location_error_pincodeAlreadyExist(self):
        response = self.client.post('post_location', data = {
            "pincode": 305001
            })
        self.assertIn(b'pincode already exist.', response.data)

    def test_get_location(self):
        response = self.client.get('/get_location/305001')
        self.assert200(response)

    def test_get_location_error_pincodeNotExist(self):
        response = self.client.get('/get_location/30123')
        self.assertIn(b'pincode did not exist.', response.data)

    def test_get_using_postgres(self):
        response = self.client.get('/get_using_postgres', query_string = {
            "latitude": 26.45,
            "longitude": 74.6333,
            "radius": 50000
        })

        self.assert200(response)

    def test_get_using_self(self):
        response = self.client.get('/get_using_self', query_string = {
            "latitude": 26.45,
            "longitude": 74.6333,
            "radius": 50000
        })

        self.assert200(response)

    def test_get_place(self):
        response = self.client.get('/get_place', query_string={
            "latitude": 72.9302,
            "longitude": 18.9594
        })

        self.assert200(response)

    def test_get_place_error_placeDidnotExistInDB(self):
        response = self.client.get('/get_place', query_string={
            "latitude": 74.679116,
            "longitude": 26.458222
        })

        self.assertIn(b'Place did not contains the given coordinates.', response.data)


if __name__ == '__main__':
    unittest.main()