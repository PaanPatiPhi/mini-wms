from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    agv_id = Column(Integer, ForeignKey("agvs.id"), nullable=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    from_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    to_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    status = Column(String, default="queued")  # queued, running, done, failed
    priority = Column(String, default="mid")   # high, mid, low
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    agv = relationship("AGV")
    order = relationship("Order")