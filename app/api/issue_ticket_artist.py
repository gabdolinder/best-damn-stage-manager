from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Query
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

# Insert single ticket
@router.post("/single_artist_ticket", status_code=status.HTTP_201_CREATED)
def upload_single_artist_ticket(
    ticket_holder_name: str = Query(..., description="Name of the artist"),
    related_act: str = Query(..., description="Related act of the artist"),
    ticket_type_name: str = Query(..., description="Type of ticket"),
    used: bool = Query(False, description="Indicates if the ticket is used"),
    db: Session = Depends(get_db)
):
    try:
        process_single_artist_ticket_data(ticket_holder_name, related_act, ticket_type_name, used, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error processing data: {str(e)}")

    return {"message": "Data inserted"}

# I would prefer to use the same function as for csv files but can't be bothered to rewrite it right now
def process_single_artist_ticket_data(ticket_holder_name: str, related_act: str, ticket_type_name: str, used: bool, db: Session):
    # Check that ticket_type is correct
    ticket_type = db.query(TicketType).filter(TicketType.ticket_type_name == ticket_type_name).first()
    if not ticket_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ticket type {ticket_type_name} does not exist")

    # Check if a ticket holder with the same name and act already exists
    ticket_holder = db.query(TicketHolder).filter(
        TicketHolder.ticket_holder_name == ticket_holder_name,
        TicketHolder.related_act == related_act
    ).first()

    if not ticket_holder:
        # Create the ticket holder if it does not exist
        ticket_holder = TicketHolder(
            ticket_holder_name=ticket_holder_name,
            related_act=related_act
        )
        db.add(ticket_holder)
        db.commit()
        db.refresh(ticket_holder)
    
    # Check if a ticket holder with the same name, act, and ticket type already exists
    existing_ticket = db.query(IssuedTicket).filter(
        IssuedTicket.ticket_holder_id == ticket_holder.ticket_holder_id,
        IssuedTicket.ticket_type_id == ticket_type.ticket_type_id
    ).first()

    if existing_ticket:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ticket for {ticket_holder_name} in act {related_act} with ticket {ticket_type_name} already exists")

    # Create the issued ticket
    issued_ticket = IssuedTicket(
        ticket_holder_id=ticket_holder.ticket_holder_id,
        used=used,
        ticket_type_id=ticket_type.ticket_type_id
    )
    db.add(issued_ticket)
    db.commit()
    db.refresh(issued_ticket)


# Insert csv ticket
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

        # Check if a ticket holder with the same name and act already exists
        ticket_holder = db.query(TicketHolder).filter(
            TicketHolder.ticket_holder_name == row['ticket_holder_name'],
            TicketHolder.related_act == row['related_act']
        ).first()

        if not ticket_holder:
            # Create the ticket holder if it does not exist
            ticket_holder = TicketHolder(
                ticket_holder_name=row['ticket_holder_name'],
                related_act=row['related_act']
            )
            db.add(ticket_holder)
            db.commit()
            db.refresh(ticket_holder)
        
        # Check if a ticket holder with the same name, act and ticket type already exists
        existing_ticket = db.query(IssuedTicket).filter(
            IssuedTicket.ticket_holder_id == ticket_holder.ticket_holder_id,
            IssuedTicket.ticket_type_id == ticket_type.ticket_type_id
        ).first()

        if existing_ticket:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ticket for {row['ticket_holder_name']} in act {row['related_act']} with ticket {row['ticket_type_name']} already exists")

        used_value = row.get('used', 'false').strip().lower() in ('true', '1', 'yes')
        
        # Create the issued ticket
        issued_ticket = IssuedTicket(
            ticket_holder_id=ticket_holder.ticket_holder_id,
            used=used_value,
            ticket_type_id=ticket_type.ticket_type_id
        )
        db.add(issued_ticket)
        db.commit()
        db.refresh(issued_ticket)



@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    # Retrieve the ticket to be deleted
    issued_ticket = db.query(IssuedTicket).filter(IssuedTicket.ticket_id == ticket_id).first()
    
    # If the ticket does not exist, raise an HTTP 404 exception
    if not issued_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    # Retrieve the associated ticket_holder
    ticket_holder_id = issued_ticket.ticket_holder_id

    # Delete the ticket
    db.delete(issued_ticket)
    db.commit()

    # Check if the ticket_holder is associated with any other tickets
    other_tickets = db.query(IssuedTicket).filter(IssuedTicket.ticket_holder_id == ticket_holder_id).all()

    if not other_tickets:
        # Retrieve the ticket_holder
        ticket_holder = db.query(TicketHolder).filter(TicketHolder.ticket_holder_id == ticket_holder_id).first()

        # Retrieve and delete associated ticket_holder_guest records
        ticket_holder_guests = db.query(TicketHolderGuest).filter(TicketHolderGuest.ticket_holder_guest_id == ticket_holder_id).all()
        for guest in ticket_holder_guests:
            db.delete(guest)
            db.commit()
        
        # Delete the ticket_holder
        if ticket_holder:
            db.delete(ticket_holder)
            db.commit()

    return {"Message": "Ticket, artist and associated guest deleted"}