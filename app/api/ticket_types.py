from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import create_ticket_type, get_ticket_type
from schemas import TicketTypeCreate, TicketTypeBase
from database import get_db

router = APIRouter()

@router.post("/", response_model=TicketTypeBase)
def create_new_ticket_type(ticket_type: TicketTypeCreate, db: Session = Depends(get_db)):
    return create_ticket_type(db=db, ticket_type=ticket_type)

@router.get("/", response_model=list[TicketTypeBase])
def read_ticket_types(db: Session = Depends(get_db)):
    ticket_types = get_ticket_type(db)
    return ticket_types
