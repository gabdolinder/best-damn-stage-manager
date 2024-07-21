from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class TicketHolder(Base):
    __tablename__ = 'ticket_holder'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    persnum = Column(String, index=True)
    ticket_holder_type_id = Column(Integer, ForeignKey('ticket_holder_type.id'))

class TicketHolderGuest(Base):
    __tablename__ = 'ticket_holder_guest'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    persnum = Column(String, index=True)
    guest_to_artist_id = Column(Integer, ForeignKey('ticket_holder.id'))

class IssuedTicket(Base):
    __tablename__ = 'issued_ticket'
    id = Column(Integer, primary_key=True, index=True)
    ticket_holder_id = Column(Integer, ForeignKey('ticket_holder.id'))
    ticket_holder_guest_id = Column(Integer, ForeignKey('ticket_holder_guest.id'))
    status = Column(Boolean, default=True)
    ticket_type_id = Column(Integer, ForeignKey('ticket_type.id'))

class TicketType(Base):
    __tablename__ = 'ticket_type'
    id = Column(Integer, primary_key=True, index=True)
    ticket_type = Column(String, index=True)

class TicketHolderType(Base):
    __tablename__ = 'ticket_holder_type'
    id = Column(Integer, primary_key=True, index=True)
    ticket_holder_type = Column(String, index=True)
