from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class AGV(Base):
    __tablename__ = "agvs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    state = Column(String, default="idle")  # idle, moving, picking, delivering, charging
    battery = Column(Float, default=100.0)
    current_row = Column(Integer, default=11)
    current_col = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())