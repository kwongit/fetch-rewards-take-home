from flask import Flask, jsonify
import uuid

app = Flask(__name__)

# Dictionary to store receipt data in memory
receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipts():
  """
  Handle POST requests to process a receipt and return a unique ID.
  """
  # Generate a random UUID object and convert it to a string
  receipt_id = str(uuid.uuid4())

  # Return a JSON response containing the generated receipt_id
  return jsonify({'id': receipt_id})
