from flask import Flask, jsonify, request
import uuid
import math

app = Flask(__name__)

# Dictionary to store receipt data in memory
receipts = {}

def calculate_points(receipt):
  """
  Calculate points for the given receipt based on specific rules.
  """
  points = 0

  # Rule 1: One point for every alphanumeric character in the retailer name.
  retailer_name = receipt.get('retailer', '')
  for char in retailer_name:
    if char.isalnum():
      points += 1

  # Rule 2: 50 points if the total is a round dollar amount with no cents.
  float_total = float(receipt.get('total', '0'))
  if float_total.is_integer():
    points += 50

  # Rule 3: 25 points if the total is a multiple of 0.25.
  if float_total % 0.25 == 0:
    points += 25

  # Rule 4: 5 points for every two items on the receipt.
  items = receipt.get('items', [])
  points += 5 * (len(items) // 2)

  # Rule 5: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
  for item in items:
    item_description = item.get('shortDescription', '')
    trimmed = len(item_description.strip()) % 3 == 0
    if trimmed:
      float_price = float(item.get('price', 0))
      points += math.ceil(float_price * 0.2)

  # Rule 6: 6 points if the day in the purchase date is odd.
  purchase_date = receipt.get('purchaseDate', '')
  day = purchase_date.split('-')[2]
  if int(day) % 2 != 0:
    points += 6

  # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
  purchase_time = receipt.get('purchaseTime', '')
  hour = purchase_time.split(':')[0]
  if 14 <= int(hour) < 16:
    points += 10

  return points

@app.route('/receipts/process', methods=['POST'])
def process_receipts():
  """
  Handle POST requests to process a receipt and return a unique ID.
  """
  # Get the JSON data from the request body
  receipt = request.json

  # Generate a random UUID object and convert it to a string
  receipt_id = str(uuid.uuid4())

  # Calculate points per receipt
  points = calculate_points(receipt)

  # Store the receipt data and calculated points in the receipts dictionary using the receipt_id as the key
  receipts[receipt_id] = {'receipt_data': receipt, 'total_points': points}

  # Return a JSON response containing the generated receipt_id
  return jsonify({'id': receipt_id})


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
  """
  Handle GET requests to retrieve the points awarded for a specific receipt.
  """
  # Look up the receipt by its UUID
  receipt = receipts.get(receipt_id)

  # Handle case where UUID not found; return 404
  if receipt is None:
    return jsonify({'error': 'Receipt not found'}), 404

  # Return a JSON response containing the points awarded
  return jsonify({'points': receipt['total_points']})

if __name__ == '__main__':
    app.run(debug=True)
