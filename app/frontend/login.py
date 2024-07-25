from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from .dependencies import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def login(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("login.html", context)
