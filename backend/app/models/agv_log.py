from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class AGVLog(Base):
    __tablename__ = "agv_logs"

    id = Column(Integer, primary_key=True, index=True)
    agv_id = Column(Integer, ForeignKey("agvs.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    from_row = Column(Integer)
    from_col = Column(Integer)
    to_row = Column(Integer)
    to_col = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())