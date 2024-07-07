from sqlalchemy.orm import Session
from models import TicketHolder, TicketHolderGuest, IssuedTicket, TicketType, TicketHolderType
from schemas import TicketHolderCreate, TicketHolderGuestCreate, IssuedTicketCreate, TicketTypeCreate, TicketHolderTypeCreate

#functions for issued_tickets
def create_issued_ticket(db: Session, issued_ticket: IssuedTicketCreate):
    db_issued_ticket = IssuedTicket(**issued_ticket.dict())
    db.add(db_issued_ticket)
    db.commit()
    db.refresh(db_issued_ticket)
    return db_issued_ticket

def get_issued_ticket(db: Session, skip: int = 0, limit: int = 10):
    return db.query(IssuedTicket).offset(skip).limit(limit).all()

#functions for ticket_holder_guests
def create_ticket_holder_guest(db: Session, ticket_holder_guest: TicketHolderGuestCreate):
    db_ticket_holder_guest = TicketHolderGuest(**ticket_holder_guest.dict())
    db.add(db_ticket_holder_guest)
    db.commit()
    db.refresh(db_ticket_holder_guest)
    return db_ticket_holder_guest

def get_ticket_holder_guest(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TicketHolderGuest).offset(skip).limit(limit).all()

#functions for ticket_holder_types
def create_ticket_holder_type(db: Session, ticket_holder_type: TicketHolderTypeCreate):
    db_ticket_holder_type = TicketHolderType(**ticket_holder_type.dict())
    db.add(db_ticket_holder_type)
    db.commit()
    db.refresh(db_ticket_holder_type)
    return db_ticket_holder_type

def get_ticket_holder_type(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TicketHolderType).offset(skip).limit(limit).all()

#functions for ticket_holders
def create_ticket_holder(db: Session, ticket_holder: TicketHolderCreate):
    db_ticket_holder = TicketHolder(**ticket_holder.dict())
    db.add(db_ticket_holder)
    db.commit()
    db.refresh(db_ticket_holder)
    return db_ticket_holder

def get_ticket_holder(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TicketHolder).offset(skip).limit(limit).all()

# functions for ticket_types
def create_ticket_type(db: Session, ticket_type: TicketTypeCreate):
    db_ticket_type = TicketType(**ticket_type.dict())
    db.add(db_ticket_type)
    db.commit()
    db.refresh(db_ticket_type)
    return db_ticket_type

def get_ticket_type(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TicketType).offset(skip).limit(limit).all()
