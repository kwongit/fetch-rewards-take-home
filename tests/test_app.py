from app import app, receipts, calculate_points
import unittest
import json

class ReceiptProcessorTestCase(unittest.TestCase):
  sample_receipt_data = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
    ],
    "total": "35.35"
  }

  def setUp(self):
    """
    Set up the test client and initialize the Flask application in testing mode.
    """
    self.app = app.test_client()
    self.app.testing = True

  def tearDown(self):
    """
    Clean up the receipts dictionary after each test to ensure isolation between tests.
    """
    receipts.clear()

  def test_process_receipts(self):
    """
    Tests the /receipts/process endpoint.
    """
    # Send POST request to process receipt
    response = self.app.post('/receipts/process',
                             data=json.dumps(self.sample_receipt_data),
                             content_type='application/json')

    # Check if response status code is 200 OK
    self.assertEqual(response.status_code, 200)

    # Check is response contains ID
    data = json.loads(response.data)
    self.assertIn('id', data)

    # Check if the receipt was store and points calculated correctly
    receipt_id = data['id']
    self.assertIn(receipt_id, receipts)
    self.assertEqual(receipts[receipt_id]['total_points'], calculate_points(self.sample_receipt_data))

  def test_get_points(self):
    """
    Tests the /receipts/<receipt_id>/points endpoint.
    """
    # Process receipt first to get ID
    post_response = self.app.post('/receipts/process',
                            data=json.dumps(self.sample_receipt_data),
                            content_type='application/json')
    post_data = json.loads(post_response.data)
    receipt_id = post_data['id']

    # Send GET request to retrieve points per receipt
    get_response = self.app.get(f'/receipts/{receipt_id}/points')

    # Check if response status code is 200 OK
    self.assertEqual(get_response.status_code, 200)

    # Check if response contains correct amount of points
    get_data = json.loads(get_response.data)
    self.assertIn('points', get_data)
    self.assertEqual(get_data['points'], calculate_points(self.sample_receipt_data))

  def test_get_points_receipt_not_found(self):
    """
    Tests the //receipts/<receipt_id>/points endpoint for an invalid receipt ID.
    """
    # Send GET request with invalid receipt ID
    response = self.app.get(f'/receipts/123-456-789/points')

    # Check if response status code is 404 Not Found
    self.assertEqual(response.status_code, 404)

    # Check is response contains the correct error message
    data = json.loads(response.data)
    self.assertIn('error', data)
    self.assertEqual(data['error'], 'Receipt not found')

if __name__ == '__main__':
    unittest.main()
