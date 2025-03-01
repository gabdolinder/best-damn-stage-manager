from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import List
from datetime import datetime

class TicketHolder(SQLModel, table=True):
    ticket_holder_id: int = Field(default=None, primary_key=True)
    ticket_holder_name: str
    ticket_holder_type_id: int = Field(foreign_key="ticketholdertype.ticket_holder_id")
    guests: List["TicketHolderGuest"] = Relationship(back_populates="ticket_holder")
    tickets: List["IssuedTicket"] = Relationship(back_populates="ticket_holder")
    
    class Config:
        table_args = (
            UniqueConstraint('ticket_holder_id', 'ticket_holder_name', name='unikey_ticket_holder_id_ticket_holder_name'),
        )

class TicketHolderGuest(SQLModel, table=True):
    ticket_holder_guest_id: int = Field(default=None, primary_key=True)
    ticket_holder_guest_name: str
    guest_to_id: int = Field(foreign_key="ticketholder.ticket_holder_id")
    ticket_holder: TicketHolder = Relationship(back_populates="guests")

class IssuedTicket(SQLModel, table=True):
    ticket_id: int = Field(default=None, primary_key=True)
    ticket_holder_id: int = Field(foreign_key="ticketholder.ticket_holder_id")
    ticket_holder_guest_id: int = Field(foreign_key="ticketholderguest.ticket_holder_guest_id")
    used: bool = True
    ticket_type_id: int = Field(foreign_key="tickettype.ticket_type_id")
    ticket_holder: TicketHolder = Relationship(back_populates="tickets")

class TicketHolderType(SQLModel, table=True):
    ticket_holder_id: int = Field(default=None, primary_key=True)
    ticket_holder_type: str

class TicketType(SQLModel, table=True):
    ticket_type_id: int = Field(default=None, primary_key=True)
    ticket_type_name: str

class Artist(SQLModel, table=True):
    artist_id: int = Field(default=None, primary_key=True)
    ticket_holder_id: int = Field(foreign_key="ticketholder.ticket_holder_id")
    artist_name: str
    comment: str = Field(default="", max_length=10000)
    pr_text: str = Field(default="", max_length=10000)
    riders: List["Rider"] = Relationship(back_populates="artist")
    pictures: List["Picture"] = Relationship(back_populates="artist")

class Rider(SQLModel, table=True):
    file_id: int = Field(default=None, primary_key=True)
    filename: str
    file_path: str
    artist_id: int = Field(foreign_key="artist.artist_id")
    artist: Artist = Relationship(back_populates="riders")

class Picture(SQLModel, table=True):
    file_id: int = Field(default=None, primary_key=True)
    filename: str
    file_path: str
    artist_id: int = Field(foreign_key="artist.artist_id")
    artist: Artist = Relationship(back_populates="pictures")

class TransportSchedule(SQLModel, table=True):
    transport_id: int = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="car.car_id")
    pickup_time: datetime
    dropoff_time: datetime
    location_from: str
    location_to: str
    number_guests: int
    comment: str = Field(default="", max_length=5000)
    booked: bool = False
    confirmed: bool = False

class Car(SQLModel, table=True):
    car_id: int = Field(default=None, primary_key=True)
    car_type: str

class LodgeSchedule(SQLModel, table=True):
    lodge_schedule_id: int = Field(default=None, primary_key=True)
    lodge_id: int = Field(foreign_key="lodge.lodge_id")
    start_time: datetime
    end_time: datetime
    comment: str = Field(default="", max_length=5000)

class Lodge(SQLModel, table=True):
    lodge_id: int = Field(default=None, primary_key=True)
    lodge_name: str
    lodge_size: str
    comment: str = Field(default="", max_length=5000)

class Act(SQLModel, table=True):
    act_id: int = Field(default=None, primary_key=True)
    act_name: str
    stage_id: int = Field(foreign_key="stage.stage_id")
    start_time: datetime
    end_time: datetime
    comment: str = Field(default="", max_length=5000)

class Stage(SQLModel, table=True):
    stage_id: int = Field(default=None, primary_key=True)
    stage_name: str
