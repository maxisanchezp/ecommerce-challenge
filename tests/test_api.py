from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    
def test_create_order():
    order_payload = {
        "customer_id": 1,
        "items":[
            {"product_id": 1, "quantity": 3}
        ]
    }
    
    response = client.post("/orders", json=order_payload)
    assert response.status_code in [200,400]
    

def test_external_product():
    response = client.get("/external-products/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data