from pydantic import BaseModel
from datetime import datetime

class AGVRead(BaseModel):
    """
    ข้อมูล AGV ที่ส่งกลับไปให้ frontend
    frontend จะเอาไปแสดงบน warehouse map
    """
    id: int
    name: str           # เช่น "AGV-01"
    state: str          # idle, moving, picking, delivering, charging
    battery: float      # 0.0 - 100.0
    current_row: int    # ตำแหน่งปัจจุบันบน grid
    current_col: int

    class Config:
        from_attributes = True

class AGVStateUpdate(BaseModel):
    """
    ใช้ตอน simulator อัปเดต state ของ AGV
    เช่น เปลี่ยนจาก idle เป็น moving
    """
    state: str
    battery: float | None = None     # optional อัปเดตหรือไม่ก็ได้
    current_row: int | None = None
    current_col: int | None = None