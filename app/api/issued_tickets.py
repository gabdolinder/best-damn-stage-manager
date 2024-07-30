from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import create_issued_ticket, get_issued_ticket
from schemas import IssuedTicketCreate, IssuedTicketBase
from database import get_db

router = APIRouter()

@router.post("/", response_model=IssuedTicketBase)
def create_new_issued_ticket(issued_ticket: IssuedTicketCreate, db: Session = Depends(get_db)):
    return create_issued_ticket(db=db, issued_ticket=issued_ticket)

@router.get("/", response_model=list[IssuedTicketBase])
def read_issued_tickets(db: Session = Depends(get_db)):
    issued_tickets = get_issued_ticket(db)
    return issued_tickets
