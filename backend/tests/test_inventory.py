from tests.conftest import *
from app.models.product import Product
from app.models.location import Location
from app.models.inventory import Inventory

def test_get_inventory_empty(client):
    """ถ้าไม่มีข้อมูลควรได้ list เปล่า"""
    response = client.get("/api/v1/inventory/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_inventory_with_data(client,db):
    """ถ้ามีข้อมูลควรได้ list ของ inventory"""
    product = Product(sku="TEST-001", name="Test Product", weight=0.1)
    location = Location(code="TEST-A1", zone="shelf", row=1, col=1)
    db.add_all([product, location])
    db.flush()

    inventory = Inventory(product_id=product.id, location_id = location.id, quantity=10)
    db.add(inventory)
    db.commit()

    response = client.get("/api/v1/inventory/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["quantity"] == 10

def test_get_inventory_not_found(client):
    """ถ้าหา id ทื่ไม่มีควรได้ 404"""
    response = client.get("/api/v1/inventory/999")
    assert response.status_code == 404