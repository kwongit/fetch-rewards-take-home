from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# Dictionary to store receipt data in memory
receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipts():
  """
  Handle POST requests to process a receipt and return a unique ID.
  """
  # Get the JSON data from the request body
  receipt = request.json

  # Generate a random UUID object and convert it to a string
  receipt_id = str(uuid.uuid4())

  # Store the receipt data and initial points (0) in the receipts dictionary using the receipt_id as the key
  receipts[receipt_id] = {'receipt_data': receipt, 'points': 0}

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
  return jsonify({'points': receipt['points']})
