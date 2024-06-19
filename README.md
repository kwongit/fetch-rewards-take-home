# Receipt Processor

This is a Flask web application that processes receipts and calculates points based on specified rules.

## Table of Contents

- [Features](#features)
- [API Endpoints](#api-endpoints)
  - [Process Receipts](#process-receipts)
  - [Get Points](#get-points)
- [Running the Application](#running-the-application)
  - [Prerequisites](#prerequisites)
  - [Build and Run with Docker](#build-and-run-with-docker)
  - [Environment Variables](#environment-variables)
  - [Directory Structure](#directory-structure)
- [Sample JSON Payload for `/receipts/process`](#sample-json-payload-for-receiptsprocess)
- [Example Responses](#example-responses)
- [Testing the API Endpoints with `curl`](#testing-the-api-endpoints-with-curl)
  - [Test the `/receipts/process` Endpoint](#test-the-receiptsprocess-endpoint)
  - [Test the `/receipts/<receipt_id>/points` Endpoint](#test-the-receiptsreceipt_idpoints-endpoint)
- [Running Unit Tests](#running-unit-tests)
- [Development](#development)

## Features

- Process receipts and return a unique ID.
- Retrieve points awarded for a specific receipt.

## API Endpoints

### Process Receipts

- **URL:** `/receipts/process`
- **Method:** `POST`
- **Payload:** JSON receipt
- **Response:** JSON containing a unique ID for the receipt.

### Get Points

- **URL:** `/receipts/<receipt_id>/points`
- **Method:** `GET`
- **Response:** JSON containing the number of points awarded.

## Running the Application

You can run this application using Docker. Follow the steps below to set up and run the application.

### Prerequisites

- Docker must be installed on your system.

### Build and Run with Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kwongit/receipt-processor.git
   cd receipt-processor
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t receipt-processor .
   ```

3. **Run the Docker container:**

   ```bash
   docker run -p 5000:5000 receipt-processor
   ```

   The application will be available at `http://localhost:5000`.

### Environment Variables

The application uses the following environment variables, which are set in the Dockerfile:

- `FLASK_APP`: The Flask application to run (set to `app`).
- `FLASK_ENV`: The environment in which the Flask app is running (set to `development`).
- `FLASK_DEBUG`: Enables or disables the debug mode (set to `True`).

### Directory Structure

The project directory structure is as follows:

```
receipt-processor/
├── app/
│   └── __init__.py
├── tests/
│   └── test_app.py
├── .flaskenv
├── .dockerignore
├── Dockerfile
├── requirements.txt
├── README.md
```

### Sample JSON Payload for `/receipts/process`

```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },
    {
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },
    {
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },
    {
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },
    {
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}
```

### Example Responses

**Process Receipts Response:**

```json
{
  "id": "e0c8c1c0-848e-4a74-9a0d-9d5f9d3b8cf6"
}
```

**Get Points Response:**

```json
{
  "points": 28
}
```

## Testing the API Endpoints with `curl`

You can test the API endpoints using the `curl` command. Here are the steps:

### Test the `/receipts/process` Endpoint

Use the following `curl` command to send a POST request to process a receipt:

```bash
curl -X POST http://localhost:5000/receipts/process -H "Content-Type: application/json" -d '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },
    {
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },
    {
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },
    {
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },
    {
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}'
```

Example response:

```json
{
  "id": "e0c8c1c0-848e-4a74-9a0d-9d5f9d3b8cf6"
}
```

### Test the `/receipts/<receipt_id>/points` Endpoint

Use the receipt ID from the previous response to fetch the points for that receipt:

```bash
curl -X GET http://localhost:5000/receipts/e0c8c1c0-848e-4a74-9a0d-9d5f9d3b8cf6/points
```

Example response:

```json
{
  "points": 28
}
```

## Running Unit Tests

To run the unit tests, follow these steps:

1. **Navigate to the project directory:**

   ```bash
   cd receipt-processor
   ```

2. **Run the unit tests:**

   ```bash
   python -m unittest discover -s tests
   ```

   This command will discover and run all the tests in the `tests` directory.

## Development

To set up a development environment, follow these steps:

1. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   flask run
   ```

   The application will be available at `http://localhost:5000`.
