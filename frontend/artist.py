from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from .dependencies import templates

guest_list = [
    {"id": 11, "guest_to_artist_id": 1, "pers_name": "Erik Johansson",},
    {"id": 12, "guest_to_artist_id": 1, "pers_name": "Oliver Nilsson",},
    {"id": 13, "guest_to_artist_id": 3, "pers_name": "Fredrik Augustsson",}
]

artist_list = [
    {"id": 1, "pers_name": "Anders Andersson", 'related_act':'Artistjanne',},
    {"id": 2, "pers_name": "Johan Olsson", 'related_act':'Artistjanne',},
    {"id": 3, "pers_name": "Rickard Svensson", 'related_act': 'Greger',}
]

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def render_artist_list(request: Request):
    context = {'request': request, 'artist_list': artist_list}
    return templates.TemplateResponse("artist.html", context)

@router.get("/{artist_id}", response_class=HTMLResponse)
def get_artist(artist_id: int, request: Request):

    # Find all data for artist with the given artist_id
    for item in artist_list:
        if item['id'] == artist_id:
            artist = item

    # Create an artist specific guest list for the given artist_id
    artist_guests = []
    for item in guest_list:
        if item['guest_to_artist_id'] == artist_id:
            artist_guests.append(item)

    context = {'request': request, 'artist': artist, 'artist_guests': artist_guests}
    return templates.TemplateResponse("artist-detail.html", context)