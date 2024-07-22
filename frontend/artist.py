from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from .dependencies import templates

artist_list = [
    {"id": 1, "name": "Anders Andersson", 'pers_num': '102030-4050', 'related_act':'Artistjanne',},
    {"id": 2, "name": "Johan Olsson", 'pers_num': '112233-4455', 'related_act':'Artistjanne',},
    {"id": 3, "name": "Rickard Svensson", 'pers_num': '122334-4550', 'related_act': 'Greger',}
]

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def render_artist_list(request: Request):
    context = {'request': request, 'artist_list': artist_list}
    return templates.TemplateResponse("artist.html", context)

@router.get("/{artist_id}", response_class=HTMLResponse)
def get_artist(artist_id: int, request: Request):

    for item in artist_list:
        if item['id'] == artist_id:
            artist = item

    context = {'request': request, 'artist': artist}
    return templates.TemplateResponse("artist-detail.html", context)