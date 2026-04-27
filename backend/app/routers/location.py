from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.location import Location
from app.schemas.location import LocationRead

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/", response_model=List[LocationRead])
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()

@router.get("/{location_id}", response_model=LocationRead)
def get_location(location_id: int, db: Session = Depends(get_db)):
    loc = db.query(Location).filter(Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    return loc