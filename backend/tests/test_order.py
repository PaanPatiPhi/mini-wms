from tests.conftest import *
from app.models.product import Product
from app.models.location import Location
from app.models.inventory import Inventory

def setup_test_data(db):
    """helper function สร้างข้อมูลพื้นฐานสำหรับ test"""
    product = Product(sku="TEST-001", name="Test Product", weight=0.1)
    location = Location(code="TEST-A1", zone="shelf", row=1, col=1)
    db.add_all([product, location])
    db.flush()
    inventory = Inventory(product_id=product.id, location_id=location.id, quantity=50)
    db.add(inventory)
    db.commit()
    return product

def test_create_order(client, db):
    """สร้าง order สำเร็จ"""
    product = setup_test_data(db)
    response = client.post("/api/v1/orders/", json={
        "items": [{"product_id": product.id, "quantity": 2}]
    })
    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    assert len(response.json()["items"]) == 1

def test_create_order_insufficient_stock(client, db):
    """สร้าง order ไม่สำเร็จเพราะ stock ไม่พอ"""
    product = setup_test_data(db)
    response = client.post("/api/v1/orders/", json={
        "items": [{"product_id": product.id, "quantity": 999}]  # เกิน stock
    })
    assert response.status_code == 400

def test_get_orders_empty(client):
    """ถ้าไม่มี order ควรได้ list เปล่า"""
    response = client.get("/api/v1/orders/")
    assert response.status_code == 200
    assert response.json() == []

def test_update_order_status(client, db):
    """อัปเดต status ของ order"""
    product = setup_test_data(db)
    # สร้าง order ก่อน
    create_response = client.post("/api/v1/orders/", json={
        "items": [{"product_id": product.id, "quantity": 1}]
    })
    order_id = create_response.json()["id"]

    # อัปเดต status
    response = client.patch(f"/api/v1/orders/{order_id}/status?status=picking")
    assert response.status_code == 200
    assert response.json()["status"] == "picking"