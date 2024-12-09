from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_process_receipt():
    response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
        ],
        "total": "35.35"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_points():
    # First, create a receipt
    post_response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
        ],
        "total": "35.35"
    })
    receipt_id = post_response.json()["id"]

    get_response = client.get(f"/receipts/{receipt_id}/points")
    assert get_response.status_code == 200
    assert "points" in get_response.json()
    assert get_response.json()["points"] > 0

def test_invalid_receipt_id():

    get_response = client.get("/receipts/invalid-id/points")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Receipt not found"}
