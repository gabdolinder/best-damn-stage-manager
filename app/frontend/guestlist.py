from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from .dependencies import templates

guest_list = [
    {"id": 11, "guest_to_artist_id": 1, "ticket_holder_guest_name": "Erik Johansson",},
    {"id": 12, "guest_to_artist_id": 3, "ticket_holder_guest_name": "Oliver Nilsson",},
    {"id": 13, "guest_to_artist_id": 3, "ticket_holder_guest_name": "Fredrik Augustsson",}
]

artist_list = [
    {"id": 1, "ticket_holder_name": "Anders Andersson", 'related_act':'Artistjanne',},
    {"id": 2, "ticket_holder_name": "Johan Olsson", 'related_act':'Artistjanne',},
    {"id": 3, "ticket_holder_name": "Rickard Svensson", 'related_act': 'Greger',}
]

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def render_guest_list(request: Request):
    context = {'request': request, 'guest_list': guest_list, 'artist_list': artist_list}
    return templates.TemplateResponse("guestlist.html", context)

@router.get("/{guest_id}", response_class=HTMLResponse)
def get_guest(guest_id: int, request: Request):
    for item in guest_list:
        if item['id'] == guest_id:
            guest = item

    for artist in artist_list:
        if artist['id'] == guest['guest_to_artist_id']:
            related_artist = artist

    context = {'request': request, 'related_artist': related_artist, 'guest':guest}
    return templates.TemplateResponse("guest-detail.html", context)
