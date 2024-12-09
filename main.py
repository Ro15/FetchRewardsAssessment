from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import uuid

app = FastAPI()
receipts = {}

class ReceiptItem(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str = Field(..., min_length=1, description="Retailer name must not be empty")
    purchaseDate: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date must be in YYYY-MM-DD format")
    purchaseTime: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="Time must be in HH:MM format")
    items: List[ReceiptItem]
    total: str = Field(..., pattern=r"^\d+(\.\d{2})?$", description="Total must be a valid currency format")

def calculate_points(receipt: Receipt) -> int:
    points = 0

    points += sum(c.isalnum() for c in receipt.retailer)

    if float(receipt.total).is_integer():
        points += 50

    if float(receipt.total) % 0.25 == 0:
        points += 25

    points += (len(receipt.items) // 2) * 5

    for item in receipt.items:
        desc_length = len(item.shortDescription.strip())
        if desc_length % 3 == 0:
            points += int(float(item.price) * 0.2)

    day = int(receipt.purchaseDate.split("-")[-1])
    if day % 2 != 0:
        points += 6

    hour, minute = map(int, receipt.purchaseTime.split(":"))
    if 14 <= hour < 16:
        points += 10

    return points

@app.post("/receipts/process")
def process_receipt(receipt: Receipt):

    receipt_id = str(uuid.uuid4())

    points = calculate_points(receipt)

    receipts[receipt_id] = {"receipt": receipt.dict(), "points": points}

    return {"id": receipt_id}

@app.get("/receipts/{id}/points")
def get_points(id: str):

    if id not in receipts:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return {"points": receipts[id].get("points", 0)}
