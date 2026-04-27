from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class OrderItemCreate(BaseModel):
    """
    ข้อมูลสินค้าแต่ละรายการใน order ที่ส่งมาตอนสร้าง
    เช่น { product_id: 1, quantity: 3 }
    """
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    """
    ข้อมูลที่ frontend ส่งมาตอนสร้าง order
    ส่งมาเป็น list ของสินค้าที่ต้องการ
    """
    items: List[OrderItemCreate]  # เช่น [{product_id:1, quantity:2}, {product_id:3, quantity:1}]

class OrderItemRead(BaseModel):
    """
    ข้อมูลสินค้าแต่ละรายการใน order ที่ส่งกลับไป
    มีข้อมูลครบกว่า OrderItemCreate
    """
    model_config = ConfigDict(from_attributes=True)  

    id: int
    product_id: int
    quantity: int
    picked: bool   # ถูก pick แล้วหรือยัง



class OrderRead(BaseModel):
    """
    ข้อมูล order ที่ส่งกลับไปให้ frontend
    มี items เป็น list ของสินค้าในนั้น
    """
    model_config = ConfigDict(from_attributes=True)  
    
    id: int
    status: str         # pending, picking, packed, dispatched
    created_at: datetime
    completed_at: datetime | None = None
    items: List[OrderItemRead]
