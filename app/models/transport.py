from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TransportSchedule(SQLModel, table=True):
    __tablename__ = 'transport_schedule'
    transport_id: int = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="car.car_id")
    driver_id: int = Field(foreign_key="driver.driver_id")
    pickup_time: Optional[datetime] = Field(default=None)
    dropoff_time: Optional[datetime] = Field(default=None)
    location_from: str
    location_to: str
    number_guests: int
    comment: Optional[str] = Field(default="", max_length=10000)
    booked: bool = False
    confirmed: bool = False

class Car(SQLModel, table=True):
    car_id: int = Field(default=None, primary_key=True)
    car_type: Optional[str] = Field(default=None)
    reg_num: str
    car_size: Optional[str] = Field(default=None)
    comment: Optional[str] = Field(default="", max_length=10000)

class Driver(SQLModel, table=True):
    driver_id: int = Field(default=None, primary_key=True)
    driver_name: str
    comment: Optional[str] = Field(default="", max_length=10000)
