from sqlalchemy.orm import Session
from sqlmodel import select
from models.artist import Artist
from models.ticket import TicketHolder, TicketHolderType

def create_artist(db: Session, artist_name: str, comment: str = "", pr_text: str = ""):
    """
    Creates an artist and a corresponding ticket holder with the type 'artist'.
    """
    # Fetch the 'artist' ticket_holder_type_id
    ticket_holder_type = db.execute(
        select(TicketHolderType).where(TicketHolderType.ticket_holder_type == "artist")
    ).scalar_one_or_none()

    if not ticket_holder_type:
        raise ValueError("TicketHolderType 'artist' does not exist. Please add it first.")

    # Create the TicketHolder
    new_ticket_holder = TicketHolder(
        ticket_holder_name=artist_name,
        ticket_holder_type_id=ticket_holder_type.ticket_holder_id
    )
    db.add(new_ticket_holder)
    db.commit()
    db.refresh(new_ticket_holder)

    # Create the Artist with reference to the new TicketHolder
    new_artist = Artist(
        ticket_holder_id=new_ticket_holder.ticket_holder_id,
        artist_name=artist_name,
        comment=comment,
        pr_text=pr_text
    )
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)

    return new_artist

def get_artist(db: Session):
    result = db.execute(select(Artist))
    return result.scalars().all()
