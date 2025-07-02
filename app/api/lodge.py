from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud.lodge import create_lodge, get_lodges
from models.lodge import Lodge

router = APIRouter()

@router.post("/lodges/", response_model=Lodge)
def add_lodge(lodge_name: str, lodge_size: str, comment: str = "", db: Session = Depends(get_db)):
    """Create a new lodge."""
    return create_lodge(db, lodge_name=lodge_name,lodge_size=lodge_size, comment=comment)

@router.get("/lodges/", response_model=list[Lodge])
def list_lodges(db: Session = Depends(get_db)):
    """Retrieve all lodges."""
    return get_lodges(db)
