from pydantic import BaseModel
from datetime import datetime
from app.schemas.product import ProductRead
from app.schemas.location import LocationRead

class InventoryRead(BaseModel):
    """
    ใช้ตอนดูสต็อกสินค้า
    แสดงข้อมูล product และ location แบบ nested
    เช่น { product: {name: "หน้ากาก"}, location: {code: "A1"}, quantity: 50 }
    """
    id: int
    quantity: int
    updated_at: datetime
    product: ProductRead      # ดึงข้อมูล product มาแสดงด้วยเลย
    location: LocationRead    # ดึงข้อมูล location มาแสดงด้วยเลย

    class Config:
        from_attributes = True

class InventoryUpdate(BaseModel):
    """
    ใช้ตอนอัปเดตจำนวนสต็อก
    รับแค่ quantity อย่างเดียว
    """
    quantity: int