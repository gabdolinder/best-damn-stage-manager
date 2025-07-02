from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import List, Optional

class TicketHolder(SQLModel, table=True):
    __tablename__ = 'ticket_holder'
    ticket_holder_id: int = Field(default=None, primary_key=True)
    ticket_holder_name: str
    ticket_holder_type_id: int = Field(foreign_key="ticket_holder_type.ticket_holder_id")
    guests: List["TicketHolderGuest"] = Relationship(back_populates="ticket_holder")
    tickets: List["IssuedTicket"] = Relationship(back_populates="ticket_holder")

class TicketHolderGuest(SQLModel, table=True):
    __tablename__ = 'ticket_holder_guest'
    ticket_holder_guest_id: int = Field(default=None, primary_key=True)
    ticket_holder_guest_name: str
    guest_to_id: int = Field(foreign_key="ticket_holder.ticket_holder_id")
    ticket_holder_type_id: int = Field(foreign_key="ticket_holder_type.ticket_holder_id")
    ticket_holder: TicketHolder = Relationship(back_populates="guests")
    tickets: List["IssuedTicket"] = Relationship(back_populates="ticket_holder_guest")

class IssuedTicket(SQLModel, table=True):
    __tablename__ = 'issued_ticket'
    ticket_id: int = Field(default=None, primary_key=True)
    ticket_holder_id: int = Field(foreign_key="ticket_holder.ticket_holder_id")
    ticket_holder_guest_id: Optional[int] = Field(foreign_key="ticket_holder_guest.ticket_holder_guest_id")
    used: bool = False
    ticket_type_id: int = Field(foreign_key="ticket_type.ticket_type_id")
    ticket_holder: TicketHolder = Relationship(back_populates="tickets")
    ticket_holder_guest: TicketHolderGuest = Relationship(back_populates="tickets")

class TicketHolderType(SQLModel, table=True):
    __tablename__ = 'ticket_holder_type'
    ticket_holder_id: int = Field(default=None, primary_key=True)
    ticket_holder_type: str

class TicketType(SQLModel, table=True):
    __tablename__ = 'ticket_type'
    ticket_type_id: int = Field(default=None, primary_key=True)
    ticket_type_name: str
