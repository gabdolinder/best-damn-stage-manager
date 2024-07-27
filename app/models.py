from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class TicketHolder(Base):
    __tablename__ = 'ticket_holder'
    ticket_holder_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_name = Column(String)
    #pers_num = Column(String)
    related_act = Column(String)
    __table_args__ = (
        UniqueConstraint('ticket_holder_name', 'related_act', name='unikey_ticket_holder_name_related_act'),
    )
    #ticket_holder_type_id = Column(Integer, ForeignKey('ticket_holder_type.id'))

class TicketHolderGuest(Base):
    __tablename__ = 'ticket_holder_guest'
    ticket_holder_guest_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_guest_name = Column(String)
    artist_related_act= Column(String)
    #pers_num = Column(String)
    guest_to_artist_id = Column(Integer, ForeignKey('ticket_holder.ticket_holder_id'))

class IssuedTicket(Base):
    __tablename__ = 'issued_ticket'
    ticket_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_id = Column(Integer, ForeignKey('ticket_holder.ticket_holder_id'))
    ticket_holder_guest_id = Column(Integer, ForeignKey('ticket_holder_guest.ticket_holder_guest_id'))
    used = Column(Boolean, default=True)
    ticket_type_id = Column(Integer, ForeignKey('ticket_type.ticket_type_id'))

class TicketHolderType(Base):
    __tablename__ = 'ticket_holder_type'
    ticket_holder_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_type = Column(String)

class TicketType(Base):
    __tablename__ = 'ticket_type'
    ticket_type_id = Column(Integer, primary_key=True, index=True )
    ticket_type_name = Column(String, unique=True)
