from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from models import TicketHolder, TicketType, IssuedTicket, TicketHolderGuest
from database import get_db
import csv
from pydantic import BaseModel
from io import StringIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class CSVData(BaseModel):
    csv_data: str

# Insert ticket
@router.post("/", status_code=status.HTTP_201_CREATED)
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        csv_data = file.file.read().decode("utf-8")
        logger.info("CSV file read successfully")
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error reading file: {str(e)}")

    process_csv_data(csv_data, db)
    return {"Message": "Data inserted"}


def process_csv_data(csv_data: str, db: Session):
    csv_reader = csv.DictReader(StringIO(csv_data))

    for row in csv_reader:
        # Check that ticket_type is correct
        ticket_type = db.query(TicketType).filter(TicketType.ticket_type_name == row['ticket_type_name']).first()
        if not ticket_type:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ticket type {row['ticket_type_name']} does not exist")

        # Check that ticket_holder is correct
        ticket_holder = db.query(TicketHolder).filter(
            TicketHolder.ticket_holder_name == row['ticket_holder_name'],
            TicketHolder.related_act == row['related_act']).first()
        if not ticket_holder:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ticket holder {row['ticket_holder_name']} with act {row['related_act']} does not exist")
        
        # Check if a ticket holder with the same name, correlated artist and act already exists
        ticket_holder_guest = db.query(TicketHolderGuest).filter(
            TicketHolderGuest.ticket_holder_guest_name == row['ticket_holder_guest_name'],
            TicketHolderGuest.artist_related_act == row['related_act'],
            TicketHolderGuest.guest_to_artist_id == ticket_holder.ticket_holder_id).first()

        # Create or get the ticket holder guest
        if not ticket_holder_guest:
            ticket_holder_guest = TicketHolderGuest(
                ticket_holder_guest_name=row['ticket_holder_guest_name'],
                guest_to_artist_id=ticket_holder.ticket_holder_id,
                artist_related_act=row['related_act'] 
            )
            db.add(ticket_holder_guest)
            db.commit()
            db.refresh(ticket_holder_guest)
        
        used_value = row.get('used', 'false').strip().lower() in ('true', '1', 'yes')
        
        # Create the issued ticket
        issued_ticket = IssuedTicket(
            ticket_holder_id=ticket_holder.ticket_holder_id,
            ticket_holder_guest_id=ticket_holder_guest.ticket_holder_guest_id,
            used=used_value,
            ticket_type_id=ticket_type.ticket_type_id
        )
        db.add(issued_ticket)
        db.commit()
        db.refresh(issued_ticket)



# Delete ticket and associated guest
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    # Retrieve the ticket to be deleted
    issued_ticket = db.query(IssuedTicket).filter(IssuedTicket.ticket_id == ticket_id).first()
    
    # If the ticket does not exist, raise an HTTP 404 exception
    if not issued_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    # Retrieve the associated ticket_holder_guest
    ticket_holder_guest_id = issued_ticket.ticket_holder_guest_id

    # Delete the ticket
    db.delete(issued_ticket)
    db.commit()

    # Check if the ticket_holder_guest is associated with any other tickets
    other_tickets = db.query(IssuedTicket).filter(IssuedTicket.ticket_holder_guest_id == ticket_holder_guest_id).all()

    if not other_tickets:
        # Retrieve the ticket_holder_guest
        ticket_holder_guest = db.query(TicketHolderGuest).filter(TicketHolderGuest.ticket_holder_guest_id == ticket_holder_guest_id).first()
        
        # Delete the ticket_holder_guest
        db.delete(ticket_holder_guest)
        db.commit()

    return {"Message": "Ticket and associated guest deleted"}