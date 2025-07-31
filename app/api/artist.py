from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.artist import Artist
from crud.artist import create_artist, get_artist

router = APIRouter()

@router.post("/artists/", response_model=Artist)
def add_artist(artist_name: str, comment: str = "", pr_text: str = "", db: Session = Depends(get_db)):
    """
    API endpoint to create an artist along with a ticket holder.
    """
    return create_artist(db, artist_name, comment, pr_text)

@router.get("/artists/")
def list_artists(db: Session = Depends(get_db)):
    artists = get_artist(db)
    return {"artists": [a.artist_name for a in artists]}