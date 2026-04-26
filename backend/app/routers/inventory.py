from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryRead, InventoryUpdate

# APIRouter คือ "กลุ่ม endpoints" ของ inventory
# prefix ทำให้ทุก route ใน file นี้ขึ้นต้นด้วย /inventory อัตโนมัติ
router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=List[InventoryRead])
def get_all_inventory(db: Session = Depends(get_db)):
    """
    ดูสต็อกสินค้าทั้งหมด
    Depends(get_db) คือขอ database session มาใช้
    FastAPI จะเรียก get_db() ให้อัตโนมัติทุกครั้ง
    """
    return db.query(Inventory).all()

@router.get("/low-stock", response_model=List[InventoryRead])
def get_low_stock(threshold: int = 10, db: Session = Depends(get_db)):
    """
    ดูสินค้าที่ quantity ต่ำกว่า threshold
    threshold เป็น query param เช่น /inventory/low-stock?threshold=5
    """
    return db.query(Inventory).filter(Inventory.quantity < threshold).all()

@router.get("/{inventory_id}", response_model=InventoryRead)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """
    ดูสต็อกสินค้าชิ้นเดียวตาม id
    ถ้าไม่เจอ ส่ง 404 กลับไป
    """
    item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return item

@router.put("/{inventory_id}", response_model=InventoryRead)
def update_inventory(inventory_id: int, data: InventoryUpdate, db: Session = Depends(get_db)):
    """
    อัปเดต quantity ของสินค้า
    data คือ body ที่ frontend ส่งมา เช่น { "quantity": 30 }
    """
    item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    item.quantity = data.quantity
    db.commit()
    db.refresh(item)  # โหลดข้อมูลล่าสุดจาก DB กลับมา
    return item