from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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

#functions for ticket_type
def create_ticket_type(db: Session, ticket_type: TicketTypeCreate):
    db_create_ticket_type = TicketType(ticket_type_name=ticket_type.ticket_type_name)
    db.add(db_create_ticket_type)
    db.commit()
    db.refresh(db_create_ticket_type)
    return db_create_ticket_type

def get_ticket_type(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TicketType).offset(skip).limit(limit).all()

def insert_ticket_type_data(db: Session):
    initial_ticket_types = [
        {"ticket_type_name": "veckoband"},
        {"ticket_type_name": "dagband onsdag"},
        {"ticket_type_name": "dagband torsdag"},
        {"ticket_type_name": "dagband fredag"},
        {"ticket_type_name": "dagband lördag"},
        {"ticket_type_name": "artistband onsdag"},
        {"ticket_type_name": "artistband torsdag"},
        {"ticket_type_name": "artistband fredag"},
        {"ticket_type_name": "artistband lördag"},
    ]
    
    for ticket_type_data in initial_ticket_types:
        ticket_type = TicketTypeCreate(**ticket_type_data)
        try:
            create_ticket_type(db, ticket_type)
        except IntegrityError:
            db.rollback()  # Rollback if a duplicate entry causes an IntegrityError
