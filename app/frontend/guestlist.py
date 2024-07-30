from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from .dependencies import templates
from database import get_db
from sqlalchemy.orm import Session
from crud import (
    get_ticket_holder_guest,
    get_ticket_holder, 
    get_specific_guest,
    get_guest_issued_tickets,
    use_issued_ticket,
    return_issued_ticket,
)
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def render_guest_list(request: Request, db: Session = Depends(get_db)):

    # Find all guests and artists
    ticket_holder_guests = get_ticket_holder_guest(db)
    ticket_holders = get_ticket_holder(db)

    context = {'request': request, 
               'ticket_holder_guests': ticket_holder_guests,
               'ticket_holders': ticket_holders,}
    return templates.TemplateResponse("guestlist.html", context)

@router.get("/{guest_id}", response_class=HTMLResponse)
def get_guest(guest_id: int, request: Request, db: Session = Depends(get_db)):
    
    # Find the specific guest and it's issued tickets
    guest = get_specific_guest(db, guest_id)    
    guest_tickets = get_guest_issued_tickets(db, guest_id)

    context = {'request': request, 
               'guest': guest,
               'guest_tickets': guest_tickets,}
    return templates.TemplateResponse("guest-detail.html", context)

@router.get("/{guest_id}/use_ticket/{ticket_id}", response_class=HTMLResponse)
def use_guest_ticket(guest_id: int, ticket_id: int, request: Request, db: Session = Depends(get_db)):
    use_issued_ticket(db, ticket_id)

    url = '/guestlist/' + str(guest_id)
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@router.get("/{guest_id}/return_ticket/{ticket_id}", response_class=HTMLResponse)
def return_guest_ticket(guest_id: int, ticket_id: int, request: Request, db: Session = Depends(get_db)):
    return_issued_ticket(db, ticket_id)

    url = '/guestlist/' + str(guest_id)
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
