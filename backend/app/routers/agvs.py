from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.agv import AGV
from app.schemas.agv import AGVRead, AGVStateUpdate

router = APIRouter(prefix="/agvs", tags=["AGVs"])

@router.get("/", response_model=List[AGVRead])
def get_agvs(db: Session = Depends(get_db)):
    """ดู AGV ทั้งหมดพร้อม state และ position"""
    return db.query(AGV).all()

@router.get("/{agv_id}", response_model=AGVRead)
def get_agv(agv_id: int, db: Session = Depends(get_db)):
    """ดู AGV ตัวเดียวตาม id"""
    agv = db.query(AGV).filter(AGV.id == agv_id).first()
    if not agv:
        raise HTTPException(status_code=404, detail="AGV not found")
    return agv

@router.patch("/{agv_id}/state", response_model=AGVRead)
def update_agv_state(agv_id: int, data: AGVStateUpdate, db: Session = Depends(get_db)):
    """
    อัปเดต state ของ AGV
    simulator จะเรียก endpoint นี้ทุกครั้งที่ robot เคลื่อนที่
    """
    agv = db.query(AGV).filter(AGV.id == agv_id).first()
    if not agv:
        raise HTTPException(status_code=404, detail="AGV not found")

    # อัปเดตเฉพาะ field ที่ส่งมา ถ้าไม่ส่งมาไม่ต้องแก้
    agv.state = data.state
    if data.battery is not None:
        agv.battery = data.battery
    if data.current_row is not None:
        agv.current_row = data.current_row
    if data.current_col is not None:
        agv.current_col = data.current_col

    db.commit()
    db.refresh(agv)
    return agv