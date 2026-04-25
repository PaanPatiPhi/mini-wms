from sqlalchemy import Column, Integer, String
from app.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)  # เช่น "A1", "INBOUND-1"
    zone = Column(String, nullable=False)               # shelf, inbound, outbound, charge
    row = Column(Integer, nullable=False)               # ตำแหน่งบน grid
    col = Column(Integer, nullable=False)