from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import create_ticket_holder, get_ticket_holder
from schemas import TicketHolderCreate, TicketHolderBase
from database import get_db

router = APIRouter()

@router.post("/", response_model=TicketHolderBase)
def create_new_ticket_holder(ticket_holder: TicketHolderCreate, db: Session = Depends(get_db)):
    return create_ticket_holder(db=db, ticket_holder=ticket_holder)

@router.get("/", response_model=list[TicketHolderBase])
def read_ticket_holders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ticket_holders = get_ticket_holder(db, skip=skip, limit=limit)
    return ticket_holders
