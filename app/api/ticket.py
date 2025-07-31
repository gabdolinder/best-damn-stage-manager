from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from database import get_db
from crud.ticket import create_ticket_type, get_ticket_type, create_ticket_holder_type, get_ticket_holder_type, create_ticket_holder, get_ticket_holder, create_ticket_holder_guest, get_ticket_holder_guests, create_issued_ticket, get_all_issued_tickets, get_ticket_holder_by_name, get_ticket_holder_guest_by_name, get_ticket_type_by_name
from models.ticket import TicketType, TicketHolderType, TicketHolder, TicketHolderGuest, IssuedTicket
from typing import Optional


router = APIRouter()

#Ticket Holder
@router.post("/ticket_holders/", response_model=TicketHolder)
def create_ticket_holder_endpoint(ticket_holder_name: str, ticket_holder_type: str, db: Session = Depends(get_db)):
    """
    API endpoint to create a TicketHolder.
    If ticket_holder_type is 'artist', also creates an entry in the Artist table.
    """
    try:
        new_ticket_holder = create_ticket_holder(db, ticket_holder_name, ticket_holder_type)
        return new_ticket_holder
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ticket_holders/")
def list_ticket_holders(db: Session = Depends(get_db)):
    ticket_holders = get_ticket_holder(db)
    return {"ticket_holders": [th.ticket_holder_name for th in ticket_holders]}

#Ticket holder guest
@router.post("/ticket_holder_guests/", response_model=TicketHolderGuest)
def create_ticket_holder_guest_endpoint(
    ticket_holder_name: str, ticket_holder_guest_name: str, db: Session = Depends(get_db)
):
    """API endpoint to create a new ticket holder guest."""
    try:
        new_guest = create_ticket_holder_guest(db, ticket_holder_name, ticket_holder_guest_name)
        return new_guest
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ticket_holder_guests/")
def list_ticket_holder_guests(db: Session = Depends(get_db)):
    ticket_holder_guests = get_ticket_holder_guests(db)
    return {"ticket_holders": [thg.ticket_holder_guest_name for thg in ticket_holder_guests]}


#Ticket types
@router.post("/ticket-types/", response_model=TicketType)
def add_ticket_type(ticket_type_name: str, db: Session = Depends(get_db)):
    """Create a new ticket type if it doesn't already exist."""
    new_ticket_type = create_ticket_type(db, ticket_type_name=ticket_type_name)
    if new_ticket_type:
        return new_ticket_type
    return {"message": "Ticket type already exists."}

@router.get("/ticket-types/")
def list_ticket_types(db: Session = Depends(get_db)):
    ticket_types = get_ticket_type(db)
    return {"ticket_types": [tt.ticket_type_name for tt in ticket_types]}

#Ticket holder type
@router.post("/ticket-holder-types/", response_model=TicketHolderType)
def add_ticket_holder_type(ticket_holder_type: str, db: Session = Depends(get_db)):
    """Create a new ticket holder type if it doesn't already exist."""
    new_ticket_type = create_ticket_holder_type(db, ticket_holder_type=ticket_holder_type)
    if new_ticket_type:
        return new_ticket_type
    return {"message": "Ticket type already exists."}

@router.get("/ticket-holder-types/")
def list_ticket_holder_types(db: Session = Depends(get_db)):
    ticket_holder_types = get_ticket_holder_type(db)
    return {"ticket_holder_types": [tht.ticket_holder_type for tht in ticket_holder_types]}

#Issued ticket
@router.post("/tickets/", response_model=IssuedTicket)
def issue_ticket(
    ticket_holder_name: str,
    ticket_type_name: str,
    ticket_holder_guest_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Issue a new ticket after validating inputs."""
    
    # Validate ticket holder
    ticket_holder = get_ticket_holder_by_name(db, ticket_holder_name)
    if not ticket_holder:
        raise HTTPException(status_code=404, detail=f"Ticket holder '{ticket_holder_name}' not found")
    
    # Validate ticket holder guest (if provided)
    ticket_holder_guest = None
    if ticket_holder_guest_name:
        ticket_holder_guest = get_ticket_holder_guest_by_name(db, ticket_holder_guest_name)
        if not ticket_holder_guest:
            raise HTTPException(status_code=404, detail=f"Guest '{ticket_holder_guest_name}' not found")
    
    # Validate ticket type
    ticket_type = get_ticket_type_by_name(db, ticket_type_name)
    if not ticket_type:
        raise HTTPException(status_code=404, detail=f"Ticket type '{ticket_type_name}' not found")

    # Issue the ticket
    return create_issued_ticket(
        db=db,
        ticket_holder_id=ticket_holder.ticket_holder_id,
        ticket_type_id=ticket_type.ticket_type_id,
        ticket_holder_guest_id=ticket_holder_guest.ticket_holder_guest_id if ticket_holder_guest else None
    )

@router.get("/tickets/", response_model=list[IssuedTicket])
def fetch_issued_tickets(db: Session = Depends(get_db)):
    """Retrieve all issued tickets."""
    return get_all_issued_tickets(db)