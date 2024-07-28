from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from .dependencies import templates
from database import get_db
from sqlalchemy.orm import Session
from models import TicketHolder
from crud import get_ticket_holder, get_specific_ticket_holder, get_specific_ticket_holder_guests, get_artist_issued_tickets, get_ticket_type, use_issued_ticket, return_issued_ticket
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def render_artist_list(request: Request, db: Session = Depends(get_db)):

    ticket_holders = get_ticket_holder(db)

    context = {'request': request, 'ticket_holders': ticket_holders}
    return templates.TemplateResponse("artist.html", context)


@router.get("/{artist_id}", response_class=HTMLResponse)
def get_artist(artist_id: int, request: Request, db: Session = Depends(get_db)):

    # Find all data for artist with the given artist_id
    artist = get_specific_ticket_holder(db, artist_id)

    # Create an artist specific guest list for the given artist_id
    artist_guests = get_specific_ticket_holder_guests(db, artist_id)

    # Find all tickets for artist
    artist_tickets = get_artist_issued_tickets(db, artist_id)

    context = {'request': request, 
               'artist': artist, 
               'artist_guests': artist_guests, 
               'artist_tickets': artist_tickets,}
    return templates.TemplateResponse("artist-detail.html", context)

@router.get("/{artist_id}/use_ticket/{ticket_id}", response_class=HTMLResponse)
def use_artist_ticket(artist_id: int, ticket_id: int, request: Request, db: Session = Depends(get_db)):
    use_issued_ticket(db, ticket_id)

    url = '/artist/' + str(artist_id)
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@router.get("/{artist_id}/return_ticket/{ticket_id}", response_class=HTMLResponse)
def return_artist_ticket(artist_id: int, ticket_id: int, request: Request, db: Session = Depends(get_db)):
    return_issued_ticket(db, ticket_id)

    url = '/artist/' + str(artist_id)
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)