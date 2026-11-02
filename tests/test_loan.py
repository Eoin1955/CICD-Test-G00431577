import pytest

def json_payload(
    equipment_id: 1,
    borrower_name: "Eoin",
    loan_days: 5,
    purpose: "Car",
    status: "Pending",
):
    return{
        "equipment_id": equipment_id,
        "borrower_name": borrower_name,
        "loan_days": loan_days,
        "purpose": purpose,
        "status": status
    }

def test_create_loan_returns_201(client):
    response = client.post("/api/loans", json_payload())
    assert response.Status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["borrower_name"] == "Eoin"

def test_duplicate_loan_returns_409(client):
    client.post("/api/loans", json_payload())
    response = client.post(
        "/api/loans", json_payload(),
    )
    assert response.Status_code == 409
    assert "already exists" in response.json()["detail"].lower()


    