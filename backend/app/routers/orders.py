from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.inventory import Inventory
from app.schemas.order import OrderCreate, OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderRead)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    """
    สร้าง order ใหม่
    1. เช็คว่า stock พอไหม
    2. สร้าง order
    3. สร้าง order items
    """
    # เช็ค stock ก่อนสร้าง order
    for item in data.items:
        inv = db.query(Inventory).filter(
            Inventory.product_id == item.product_id
        ).first()
        if not inv:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found in inventory")
        if inv.quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")

    # สร้าง order
    order = Order(status="pending")
    db.add(order)
    db.flush()  # flush เพื่อให้ได้ order.id ก่อน commit

    # สร้าง order items
    for item in data.items:
        db.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            picked=False
        ))

    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[OrderRead])
def get_orders(status: str | None = None, db: Session = Depends(get_db)):
    """
    ดู orders ทั้งหมด
    filter by status ได้ เช่น /orders?status=pending
    """
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    return query.order_by(Order.created_at.desc()).all()

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """ดู order detail ตาม id"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    """
    อัปเดต status ของ order
    flow: pending → picking → packed → dispatched
    """
    # กำหนด flow ที่ถูกต้อง
    valid_flow = {
        "pending": "picking",
        "picking": "packed",
        "packed": "dispatched"
    }
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if status not in ["picking", "packed", "dispatched"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    if valid_flow.get(order.status) != status:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change status from {order.status} to {status}"
        )

    order.status = status
    # ถ้า dispatched แล้วบันทึกเวลาที่เสร็จ
    if status == "dispatched":
        order.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order