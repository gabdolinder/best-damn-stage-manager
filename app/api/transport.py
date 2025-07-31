from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud.transport import get_or_create_car, get_or_create_driver, get_all_cars, get_all_drivers, create_transport, get_all_transports
from models.transport import Car, Driver, TransportSchedule
from datetime import datetime
from typing import Optional


router = APIRouter()

#Car
@router.post("/cars/", response_model=Car)
def create_car(
    reg_num: str,
    car_type: Optional[str] = None,
    car_size: Optional[str] = None,
    comment: str = "",
    db: Session = Depends(get_db),
):
    """
    Create a new car if it doesn't exist, or return the existing one.
    """
    return get_or_create_car(db, reg_num=reg_num, car_type=car_type, car_size=car_size, comment=comment)


@router.get("/cars/", response_model=list[Car])
def fetch_cars(db: Session = Depends(get_db)):
    """Retrieve all cars."""
    return get_all_cars(db)

#Driver
@router.post("/drivers/", response_model=Driver)
def create_driver(driver_name: str, comment: str = "", db: Session = Depends(get_db)):
    """
    Create a new driver if they don't exist, or return the existing one.
    """
    return get_or_create_driver(db, driver_name=driver_name, comment=comment)

@router.get("/drivers/", response_model=list[Driver])
def fetch_drivers(db: Session = Depends(get_db)):
    """Retrieve all drivers."""
    return get_all_drivers(db)

#Transport
@router.post("/transport/", response_model=TransportSchedule)
def add_transport(
    location_from: str,
    location_to: str,
    number_guests: int,
    reg_num: str,
    comment: str = "",
    pickup_time: Optional[datetime] = None,
    dropoff_time: Optional[datetime] = None,
    car_type: Optional[str] = None,
    car_size: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Create a new transport schedule."""
    return create_transport(db, car_type, reg_num, car_size, pickup_time, dropoff_time, location_from, location_to, number_guests, comment)

@router.get("/transport/", response_model=list[TransportSchedule])
def get_all_transports(db: Session = Depends(get_db)):
    """Fetch all transport schedules."""
    return get_all_transports(db)