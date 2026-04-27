from pydantic import BaseModel, ConfigDict
from datetime import datetime

# BaseModel คือ "แม่แบบ" ของ Pydantic
# ทุก Schema จะ inherit จากตัวนี้

class ProductBase(BaseModel):
    """
    ข้อมูลกลาง ที่ทั้ง create และ read ใช้ร่วมกัน
    """
    sku: str           # รหัสสินค้า เช่น "SKU-001"
    name: str          # ชื่อสินค้า
    description: str | None = None   # optional — ใส่หรือไม่ก็ได้
    weight: float = 0.0

class ProductCreate(ProductBase):
    """
    ใช้ตอน frontend ส่งข้อมูลมาสร้างสินค้าใหม่
    รับแค่ field ที่ user กรอก ไม่มี id หรือ created_at
    """
    pass  # รับ field เดียวกับ ProductBase ทั้งหมด

class ProductRead(ProductBase):
    """
    ใช้ตอน backend ส่งข้อมูลกลับไปให้ frontend
    มี id และ created_at เพิ่มมาด้วย
    """
    model_config = ConfigDict(from_attributes=True)  

    id: int
    created_at: datetime
