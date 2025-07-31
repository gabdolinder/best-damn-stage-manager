from sqlmodel import select
from sqlalchemy.orm import Session
from models.ticket import TicketHolder, TicketHolderGuest, TicketType, TicketHolderType, IssuedTicket
from models.artist import Artist
from typing import Optional



#Ticket holder
def create_ticket_holder(db: Session, ticket_holder_name: str, ticket_holder_type: str):
    """Create a TicketHolder. If type is 'artist', also create an Artist entry."""

    ticket_holder_type_obj = get_single_ticket_holder_type(db, ticket_holder_type)
    if not ticket_holder_type_obj:
        raise ValueError(f"Invalid ticket_holder_type: {ticket_holder_type}")

    # Create the TicketHolder
    new_ticket_holder = TicketHolder(
        ticket_holder_name=ticket_holder_name,
        ticket_holder_type_id=ticket_holder_type_obj.ticket_holder_id
    )
    db.add(new_ticket_holder)
    db.commit()
    db.refresh(new_ticket_holder)

    # If type is 'artist', create an Artist entry
    if ticket_holder_type.lower() == "artist":
        new_artist = Artist(
            ticket_holder_id=new_ticket_holder.ticket_holder_id,
            artist_name=ticket_holder_name
        )
        db.add(new_artist)
        db.commit()
        db.refresh(new_artist)

    return new_ticket_holder

def get_ticket_holder(db: Session):
    """Fetch all ticket holders."""
    result = db.execute(select(TicketHolder))
    return result.scalars().all()


#Ticket holder guest
def get_ticket_holder_by_name(db: Session, ticket_holder_name: str):
    """Fetch the TicketHolder object based on the ticket_holder_name."""
    result = db.execute(
        select(TicketHolder).where(TicketHolder.ticket_holder_name == ticket_holder_name)
    )
    return result.scalar_one_or_none()

def create_ticket_holder_guest(db: Session, ticket_holder_name: str, ticket_holder_guest_name: str):
    """Create a TicketHolderGuest for a given ticket holder."""
    
    # Get the 'Gäst' ticket_holder_type using the helper function
    guest_type = get_single_ticket_holder_type(db, 'gäst')
    if not guest_type:
        raise ValueError("Ticket holder type 'Gäst' not found.")
    
    # Fetch the ticket_holder by ticket_holder_name
    ticket_holder = get_ticket_holder_by_name(db, ticket_holder_name)
    
    if ticket_holder is None:
        raise ValueError(f"Ticket holder with name {ticket_holder_name} not found.")
    
    # Ensure that we now have a valid ticket_holder with ticket_holder_id
    if not hasattr(ticket_holder, 'ticket_holder_id'):
        raise ValueError(f"Invalid ticket holder object: {ticket_holder}")
    
    # Create the TicketHolderGuest
    new_guest = TicketHolderGuest(
        ticket_holder_guest_name=ticket_holder_guest_name,
        guest_to_id=ticket_holder.ticket_holder_id,  # Match with the ticket_holder_id
        ticket_holder_type_id=guest_type.ticket_holder_id
    )
    
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)

    return new_guest


def get_ticket_holder_guests(db: Session):
    """Fetch all ticket holder guests."""
    result = db.execute(select(TicketHolderGuest))
    return result.scalars().all()

#Ticket Type
def create_ticket_type(db: Session, ticket_type_name: str):
    """Creates a new ticket type if it doesn't already exist."""
    existing_ticket_type = db.execute(select(TicketType).filter(TicketType.ticket_type_name == ticket_type_name)).scalar_one_or_none()

    # If it doesn't exist, add the new ticket type
    if not existing_ticket_type:
        new_ticket_type = TicketType(ticket_type_name=ticket_type_name)
        db.add(new_ticket_type)
        db.commit()
        db.refresh(new_ticket_type)
        return new_ticket_type
    return None

def insert_ticket_types(db: Session):
    ticket_types = [
        "veckoband",
        "dagband onsdag",
        "dagband torsdag",
        "dagband fredag",
        "dagband lördag",
        "artistband onsdag",
        "artistband torsdag",
        "artistband fredag",
        "artistband lördag",
    ]

    new_ticket_types = []
    for ticket_type_name in ticket_types:
        created_ticket = create_ticket_type(db, ticket_type_name)
        if created_ticket:
            new_ticket_types.append(created_ticket)

    return new_ticket_types


def get_ticket_type(db: Session):
    result = db.execute(select(TicketType))
    return result.scalars().all() 

#Ticket Holder Type
def create_ticket_holder_type(db: Session, ticket_holder_type: str):
    """Creates a new ticket holder type if it doesn't already exist."""
    existing_ticket_holder_type = db.execute(select(TicketHolderType).filter(TicketHolderType.ticket_holder_type == ticket_holder_type)).scalar_one_or_none()

    # If it doesn't exist, add the new ticket type
    if not existing_ticket_holder_type:
        new_ticket_holder_type = TicketHolderType(ticket_holder_type=ticket_holder_type)
        db.add(new_ticket_holder_type)
        db.commit()
        db.refresh(new_ticket_holder_type)
        return new_ticket_holder_type
    return None

def insert_ticket_holder_types(db: Session):
    ticket_holder_types = [
        "artist",
        "gäst",
        "crew",
        "utställare",
    ]

    new_ticket_holder_types = []
    for ticket_holder_type_name in ticket_holder_types:
        created_ticket_holder_type = create_ticket_holder_type(db, ticket_holder_type_name)
        if created_ticket_holder_type:
            new_ticket_holder_types.append(created_ticket_holder_type)

    return new_ticket_holder_types


def get_ticket_holder_type(db: Session):
    result = db.execute(select(TicketHolderType))
    return result.scalars().all() 

def get_single_ticket_holder_type(db: Session, ticket_holder_type: str):
    """Fetch the TicketHolderType object based on the type name."""
    result = db.execute(
        select(TicketHolderType).where(TicketHolderType.ticket_holder_type == ticket_holder_type)
    )
    return result.scalar_one_or_none()

#Issued ticket
def get_ticket_holder_guest_by_name(db: Session, name: str) -> Optional[TicketHolderGuest]:
    """Fetch a ticket holder guest by name (optional)."""
    return db.execute(select(TicketHolderGuest).where(TicketHolderGuest.name == name)).scalars().first()

def get_ticket_type_by_name(db: Session, ticket_type_name: str):
    """Fetch the ticket type by name."""
    return db.execute(select(TicketType).where(TicketType.ticket_type_name == ticket_type_name)).scalars().first()


def create_issued_ticket(
    db: Session,
    ticket_holder_id: int,
    ticket_type_id: int,
    ticket_holder_guest_id: Optional[int] = None
) -> IssuedTicket:
    """Create a new issued ticket entry."""
    new_ticket = IssuedTicket(
        ticket_holder_id=ticket_holder_id,
        ticket_holder_guest_id=ticket_holder_guest_id,
        ticket_type_id=ticket_type_id,
        used=False  # Default is unused
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

def get_all_issued_tickets(db: Session) -> list[IssuedTicket]:
    """Retrieve all issued tickets."""
    return db.execute(select(IssuedTicket)).scalars().all()
