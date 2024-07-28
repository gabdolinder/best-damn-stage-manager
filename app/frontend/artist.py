from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from .dependencies import templates
from database import get_db
from sqlalchemy.orm import Session
from models import TicketHolder
from crud import get_ticket_holder, get_specific_ticket_holder, get_specific_ticket_holder_guests, get_artist_issued_tickets, get_ticket_type

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

    ticket_types = get_ticket_type(db)

    context = {'request': request, 
               'artist': artist, 
               'artist_guests': artist_guests, 
               'artist_tickets': artist_tickets,
               'ticket_types': ticket_types}
    return templates.TemplateResponse("artist-detail.html", context)