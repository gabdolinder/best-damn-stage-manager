from sqlalchemy.orm import Session
from sqlmodel import select
from models.lodge import Lodge

def create_lodge(db: Session, lodge_name: str, lodge_size: str, comment: str = ""):
    """Creates a new lodge and adds it to the database."""
    new_lodge = Lodge(lodge_name=lodge_name,lodge_size=lodge_size, comment=comment)
    db.add(new_lodge)
    db.commit()
    db.refresh(new_lodge)
    return new_lodge

def get_lodges(db: Session):
    """Retrieves all lodges from the database."""
    result = db.execute(select(Lodge))
    return result.scalars().all()