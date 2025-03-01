from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# TicketHolder
class TicketHolderBase(BaseModel):
    ticket_holder_name: str
    ticket_holder_type_id: int

class TicketHolderCreate(TicketHolderBase):
    pass

class TicketHolderRead(TicketHolderBase):
    ticket_holder_id: int
    class Config:
        from_attributes = True

# TicketHolderGuest
class TicketHolderGuestBase(BaseModel):
    ticket_holder_guest_name: str
    guest_to_id: int

class TicketHolderGuestCreate(TicketHolderGuestBase):
    pass

class TicketHolderGuestRead(TicketHolderGuestBase):
    ticket_holder_guest_id: int
    class Config:
        from_attributes = True

# IssuedTicket
class IssuedTicketBase(BaseModel):
    ticket_holder_id: Optional[int] = None
    ticket_holder_guest_id: Optional[int] = None
    used: bool
    ticket_type_id: int

class IssuedTicketCreate(IssuedTicketBase):
    pass

class IssuedTicketRead(IssuedTicketBase):
    ticket_id: int
    class Config:
        from_attributes = True

# TicketHolderType
class TicketHolderTypeBase(BaseModel):
    ticket_holder_type: str

class TicketHolderTypeCreate(TicketHolderTypeBase):
    pass

class TicketHolderTypeRead(TicketHolderTypeBase):
    ticket_holder_id: int
    class Config:
        from_attributes = True

# TicketType
class TicketTypeBase(BaseModel):
    ticket_type_name: str

class TicketTypeCreate(TicketTypeBase):
    pass

class TicketTypeRead(TicketTypeBase):
    ticket_type_id: int
    class Config:
        from_attributes = True

# Artist
class ArtistBase(BaseModel):
    ticket_holder_id: int
    artist_name: str
    comment: Optional[str] = None
    pr_text: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class ArtistRead(ArtistBase):
    artist_id: int
    class Config:
        from_attributes = True

# Rider
class RiderBase(BaseModel):
    filename: str
    file_path: str
    artist_id: int

class RiderCreate(RiderBase):
    pass

class RiderRead(RiderBase):
    file_id: int
    class Config:
        from_attributes = True

# Picture
class PictureBase(BaseModel):
    filename: str
    file_path: str
    artist_id: int

class PictureCreate(PictureBase):
    pass

class PictureRead(PictureBase):
    file_id: int
    class Config:
        from_attributes = True

# Volounteer
class VolounteerBase(BaseModel):
    volounteer_name: str

class VolounteerCreate(VolounteerBase):
    pass

class VolounteerRead(VolounteerBase):
    volounteer_id: int
    class Config:
        from_attributes = True

# TransportSchedule
class TransportScheduleBase(BaseModel):
    car_id: int
    pickup_time: datetime
    dropoff_time: datetime
    location_from: str
    location_to: str
    number_guests: int
    comments: Optional[str] = None
    booked: bool = False
    confirmed: bool = False

class TransportScheduleCreate(TransportScheduleBase):
    pass

class TransportScheduleRead(TransportScheduleBase):
    transport_id: int
    class Config:
        from_attributes = True

# Car
class CarBase(BaseModel):
    car_type: str

class CarCreate(CarBase):
    pass

class CarRead(CarBase):
    car_id: int
    class Config:
        from_attributes = True

# Lodge
class LodgeBase(BaseModel):
    lodge_name: str
    lodge_size: str
    comments: Optional[str] = None

class LodgeCreate(LodgeBase):
    pass

class LodgeRead(LodgeBase):
    lodge_id: int
    class Config:
        from_attributes = True

# LodgeSchedule
class LodgeScheduleBase(BaseModel):
    lodge_id: int
    start_time: datetime
    end_time: datetime
    comments: Optional[str] = None

class LodgeScheduleCreate(LodgeScheduleBase):
    pass

class LodgeScheduleRead(LodgeScheduleBase):
    lodge_schedule_id: int
    class Config:
        from_attributes = True

# Act
class ActBase(BaseModel):
    act_name: str
    stage_id: int
    start_time: datetime
    end_time: datetime
    comments: Optional[str] = None

class ActCreate(ActBase):
    pass

class ActRead(ActBase):
    act_id: int
    class Config:
        from_attributes = True

# Stage
class StageBase(BaseModel):
    stage_name: str

class StageCreate(StageBase):
    pass

class StageRead(StageBase):
    stage_id: int
    class Config:
        from_attributes = True
