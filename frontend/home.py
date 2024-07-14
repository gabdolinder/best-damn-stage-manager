from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from .dependencies import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def render_home(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("home.html", context)
