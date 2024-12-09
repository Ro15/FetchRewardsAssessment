FastAPI Receipts API
This project is a web service built using FastAPI. It provides two endpoints to process receipts and calculate points based on specific rules. The application stores receipt data in memory and calculates points for each receipt.

Features
Process Receipts:
Submit a receipt JSON payload.
Returns a unique ID for the receipt.
Retrieve Points:
Use the receipt ID to get the points awarded for the receipt.
API Endpoints
1. POST /receipts/process
Description: Processes a receipt and returns a unique receipt ID.
Request Body:
json
Copy code
{
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
    ],
    "total": "35.35"
}
Response:
json
Copy code
{
    "id": "unique-receipt-id"
}
2. GET /receipts/{id}/points
Description: Retrieves the points awarded for a specific receipt ID.
Path Parameter: id (the unique ID of the receipt).
Response:
json
Copy code
{
    "points": 28
}
Rules for Points Calculation
The following rules determine how many points are awarded for a receipt:

1 Point: For every alphanumeric character in the retailer's name.
50 Points: If the total is a round dollar amount with no cents.
25 Points: If the total is a multiple of 0.25.
5 Points: For every two items on the receipt.
Variable Points:
If the length of an item's description (trimmed) is a multiple of 3:
Multiply the item price by 0.2 and round up to the nearest integer.
Add the result to the total points.
6 Points: If the purchase day (from purchaseDate) is odd.
10 Points: If the purchase time (from purchaseTime) is between 2:00 PM and 4:00 PM.
Setup Instructions
1. Prerequisites
Python 3.8 or later.
Install pip (Python package manager).
2. Install Dependencies
Clone the repository or download the code.
Navigate to the project folder in your terminal.
Create a virtual environment:
bash
Copy code
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies:
bash
Copy code
pip install fastapi uvicorn
3. Run the Application
Start the FastAPI server:

bash
Copy code
uvicorn main:app --reload
The server will run at http://127.0.0.1:8000.

Testing the Application
1. Interactive API Documentation
Visit the Swagger UI at:

arduino
Copy code
http://127.0.0.1:8000/docs
You can test the endpoints directly from the browser.

2. Using cURL
Test the POST /receipts/process endpoint:

bash
Copy code
curl -X POST "http://127.0.0.1:8000/receipts/process" -H "Content-Type: application/json" -d '{
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
    ],
    "total": "35.35"
}'
Test the GET /receipts/{id}/points endpoint:

bash
Copy code
curl -X GET "http://127.0.0.1:8000/receipts/{id}/points"
Replace {id} with the receipt ID returned from the POST endpoint.

Running Tests
To run automated tests:

Install pytest:
bash
Copy code
pip install pytest
Run tests:
bash
Copy code
pytest
Limitations
Data is stored in memory and will be lost if the application restarts.
No database is used for persistence.
Future Improvements
Add database support for persistent storage.
Enhance the user interface with a frontend.
Add deployment scripts for hosting the application.