from sqlalchemy.orm import Session
from sqlmodel import select
from datetime import datetime
from typing import Optional
from models.transport import TransportSchedule, Car, Driver

# Car

def get_or_create_car(db: Session, reg_num: str, car_type: Optional[str] = None, car_size: Optional[str] = None, comment: str = ""):
    """Check if the car exists by registration number, otherwise create a new one."""
    existing_car = db.execute(select(Car).where(Car.reg_num == reg_num)).scalars().first()
    if existing_car:
        return existing_car  # Return existing car if found

    new_car = Car(car_type=car_type, reg_num=reg_num, car_size=car_size, comment=comment)
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car  # Return the newly created car


def get_all_cars(db: Session):
    """Fetch all cars from the database."""
    return db.execute(select(Car)).scalars().all()

# Driver

def get_or_create_driver(db: Session, driver_name: str, comment: str = ""):
    """Check if the driver exists, otherwise create a new one."""
    existing_driver = db.execute(select(Driver).where(Driver.driver_name == driver_name)).scalars().first()
    if existing_driver:
        return existing_driver  # Return existing driver if found

    new_driver = Driver(driver_name=driver_name, comment=comment)
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver  # Return the newly created driver

def get_unassigned_driver(db: Session):
    """Fetch the 'unassigned' driver, create one if not exists."""
    unassigned_driver = db.execute(select(Driver).where(Driver.driver_name == "unassigned")).scalars().first()
    if not unassigned_driver:
        unassigned_driver = Driver(driver_name="unassigned", comment="Default driver for unassigned trips")
        db.add(unassigned_driver)
        db.commit()
        db.refresh(unassigned_driver)
    return unassigned_driver

def get_all_drivers(db: Session):
    """Fetch all drivers from the database."""
    return db.execute(select(Driver)).scalars().all()

# Transport

def create_transport(db: Session, car_type: str, reg_num: str, car_size: str, pickup_time: datetime, dropoff_time: datetime, location_from: str, location_to: str, number_guests: int, comment: str = ""):
    """Create a new transport entry with the specified car and default driver."""
    car = get_or_create_car(db, car_type, reg_num, car_size, comment)
    driver = get_unassigned_driver(db)

    new_transport = TransportSchedule(
        car_id=car.car_id,
        driver_id=driver.driver_id,
        pickup_time=pickup_time,
        dropoff_time=dropoff_time,
        location_from=location_from,
        location_to=location_to,
        number_guests=number_guests,
        comment=comment
    )

    db.add(new_transport)
    db.commit()
    db.refresh(new_transport)
    return new_transport

def get_all_transports(db: Session):
    """Fetch all transports from the database."""
    return db.execute(select(TransportSchedule)).scalars().all()
