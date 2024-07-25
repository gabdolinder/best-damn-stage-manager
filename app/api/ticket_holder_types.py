from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import create_ticket_holder_type, get_ticket_holder_type
from schemas import TicketHolderTypeCreate, TicketHolderTypeBase
from database import get_db

router = APIRouter()

@router.post("/", response_model=TicketHolderTypeBase)
def create_new_ticket_holder_type(ticket_holder_type: TicketHolderTypeCreate, db: Session = Depends(get_db)):
    return create_ticket_holder_type(db=db, ticket_holder_type=ticket_holder_type)

@router.get("/", response_model=list[TicketHolderTypeBase])
def read_ticket_holder_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ticket_holder_types = get_ticket_holder_type(db, skip=skip, limit=limit)
    return ticket_holder_types
