import unittest
from flask import Flask, jsonify
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
      self.app = app.test_client()  # Set test client
      self.app.testing = True  # Set unit testing

    def test_post_data(self):
        data = {
            "retailer": "Testretailerretailerretailerretailer",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "14:13",
            "total": "1.00",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }
        response = self.app.post('/receipts/process', json=data)
        res_data = response.get_json()
        print(res_data)

    def test_get_receipt_points(self):
        id = 'fb0537f6-2a8f-44ae-8ae5-e449eff2d9dc'
        response = self.app.get(f"/receipts/{id}/points")
        res_data = response.get_json()
        print(res_data)

if __name__ == '__main__':
    unittest.main()