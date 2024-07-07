from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import create_ticket_holder_guest, get_ticket_holder_guest
from schemas import TicketHolderGuestCreate, TicketHolderGuestBase
from database import get_db

router = APIRouter()

@router.post("/", response_model=TicketHolderGuestBase)
def create_new_ticket_holder_guest(ticket_holder_guest: TicketHolderGuestCreate, db: Session = Depends(get_db)):
    return create_ticket_holder_guest(db=db, ticket_holder_guest=ticket_holder_guest)

@router.get("/", response_model=list[TicketHolderGuestBase])
def read_ticket_holder_guests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ticket_holder_guests = get_ticket_holder_guest(db, skip=skip, limit=limit)
    return ticket_holder_guests