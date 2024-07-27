from pydantic import BaseModel

# Base schema for TicketHolder, used to define shared attributes and validation rules
class TicketHolderBase(BaseModel):
    ticket_holder_name: str
    #pers_num: str
    related_act: str
    #ticket_holder_type_id: int

    class Config:
        orm_mode = True  # Enables ORM mode to work with SQLAlchemy models

# Schema used for creating a new TicketHolder, inheriting from TicketHolderBase
class TicketHolderCreate(TicketHolderBase):
    pass

# Base schema for TicketHolderGuest, used to define shared attributes and validation rules
class TicketHolderGuestBase(BaseModel):
    ticket_holder_guest_name: str
    #pers_num: str
    guest_to_artist_id: int
    artist_related_act: str

    class Config:
        orm_mode = True  # Enables ORM mode to work with SQLAlchemy models

# Schema used for creating a new TicketHolderGuest, inheriting from TicketHolderGuestBase
class TicketHolderGuestCreate(TicketHolderGuestBase):
    pass

# Base schema for IssuedTicket, used to define shared attributes and validation rules
class IssuedTicketBase(BaseModel):
    ticket_holder_id: int
    ticket_holder_guest_id: int
    used: bool
    ticket_type_id: int

    class Config:
        orm_mode = True  # Enables ORM mode to work with SQLAlchemy models

# Schema used for creating a new IssuedTicket, inheriting from IssuedTicketBase
class IssuedTicketCreate(IssuedTicketBase):
    pass

# Base schema for TicketHolderType, used to define shared attributes and validation rules
class TicketHolderTypeBase(BaseModel):
    ticket_holder_type: str

    class Config:
        orm_mode = True  # Enables ORM mode to work with SQLAlchemy models

# Schema used for creating a new TicketHolderType, inheriting from TicketHolderTypeBase
class TicketHolderTypeCreate(TicketHolderTypeBase):
    pass

# Base schema for TicketType, used to define shared attributes and validation rules
class TicketTypeBase(BaseModel):
    ticket_type_name: str

    class Config:
        orm_mode = True  # Enables ORM mode to work with SQLAlchemy models

# Schema used for creating a new TicketType, inheriting from TicketTypeBase
class TicketTypeCreate(TicketTypeBase):
    pass