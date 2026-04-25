from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    """
    ข้อมูลที่ส่งมาตอนสร้าง task ใหม่
    บอกว่าให้ AGV ไปรับของจากที่ไหน ส่งไปที่ไหน
    """
    from_location_id: int   # รับของจาก location นี้
    to_location_id: int     # ส่งไปที่ location นี้
    priority: str = "mid"   # high, mid, low
    agv_id: int | None = None       # ถ้าไม่ระบุ จะ auto-assign ให้
    order_id: int | None = None     # optional เชื่อมกับ order ได้

class TaskRead(BaseModel):
    """
    ข้อมูล task ที่ส่งกลับไปให้ frontend
    """
    id: int
    status: str             # queued, running, done, failed
    priority: str
    from_location_id: int
    to_location_id: int
    agv_id: int | None = None
    order_id: int | None = None
    created_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True