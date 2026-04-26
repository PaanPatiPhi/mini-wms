from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.task import Task
from app.models.agv import AGV
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskRead)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    """
    สร้าง task ใหม่
    ถ้าไม่ระบุ agv_id จะ auto-assign ให้ AGV ที่ idle อยู่
    """
    agv_id = data.agv_id

    # Auto-assign ถ้าไม่ได้ระบุ AGV
    if agv_id is None:
        idle_agv = db.query(AGV).filter(
            AGV.state == "idle",
            AGV.battery > 20  # เช็คว่า battery พอ
        ).first()
        if idle_agv:
            agv_id = idle_agv.id

    task = Task(
        from_location_id=data.from_location_id,
        to_location_id=data.to_location_id,
        priority=data.priority,
        agv_id=agv_id,
        order_id=data.order_id,
        status="queued"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=List[TaskRead])
def get_tasks(status: str | None = None, agv_id: int | None = None, db: Session = Depends(get_db)):
    """
    ดู tasks ทั้งหมด
    filter by status หรือ agv_id ได้
    เช่น /tasks?status=queued หรือ /tasks?agv_id=1
    """
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if agv_id:
        query = query.filter(Task.agv_id == agv_id)
    return query.order_by(Task.created_at.desc()).all()

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """ดู task ตาม id"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}/status", response_model=TaskRead)
def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    """
    อัปเดต status ของ task
    simulator จะเรียกตอน task เสร็จ
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if status not in ["queued", "running", "done", "failed"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    task.status = status
    if status in ["done", "failed"]:
        task.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task