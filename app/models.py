from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from database import Base

class TicketHolder(Base):
    __tablename__ = 'ticket_holder'
    ticket_holder_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_name = Column(String)
    ticket_holder_type_id = Column(Integer, ForeignKey('ticket_holder_type.id'))
    __table_args__ = (
        UniqueConstraint('ticket_holder_id', 'ticket_holder_name', name='unikey_ticket_holder_id_ticket_holder_name')
    )

class TicketHolderGuest(Base):
    __tablename__ = 'ticket_holder_guest'
    ticket_holder_guest_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_guest_name = Column(String)
    guest_to_id = Column(Integer, ForeignKey('ticket_holder.ticket_holder_id'))

class IssuedTicket(Base):
    __tablename__ = 'issued_ticket'
    ticket_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_id = Column(Integer, ForeignKey('ticket_holder.ticket_holder_id'))
    ticket_holder_guest_id = Column(Integer, ForeignKey('ticket_holder_guest.ticket_holder_guest_id'))
    used = Column(Boolean, default=True)
    ticket_type_id = Column(Integer, ForeignKey('ticket_type.ticket_type_id'))

class TicketHolderType(Base):
    __tablename__ = 'ticket_holder_type'
    ticket_holder_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_type = Column(String)

class TicketType(Base):
    __tablename__ = 'ticket_type'
    ticket_type_id = Column(Integer, primary_key=True, index=True )
    ticket_type_name = Column(String, unique=True)

class Artist(Base):
    __tablename__ = 'artist'
    artist_id = Column(Integer, primary_key=True, index=True)
    ticket_holder_id = Column(Integer, ForeignKey('ticket_holder.ticket_holder_id'))
    artist_name = Column(String)
    rider = relationship("Rider", back_populates="artist")
    picture = relationship("Picture", back_populates="artist")
    comment = Column(String)
    pr_text = Column(String)

class Rider(Base):
    __tablename__ = "rider"
    file_id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Store path to the uploaded file
    artist_id = Column(Integer, ForeignKey("artist.artist_id"))
    artist = relationship("Artist", back_populates="rider")

class Picture(Base):
    __tablename__ = "picture"
    file_id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Store path to the uploaded file
    artist_id = Column(Integer, ForeignKey("artist.artist_id"))
    artist = relationship("Artist", back_populates="picture")

class ArtistVolounteer(Base):
    __tablename__ = 'artist_volounteer'
    artist_id = Column(Integer, ForeignKey("artist.artist_id"))
    volounteer_id = Column(Integer, ForeignKey("volounteer.volounteer_id"))

class Volounteer(Base):
    __tablename__ = 'volounteer'
    volounteer_id = Column(Integer, primary_key=True, index=True)
    volounteer_name = Column(String)

class ArtistTransport(Base):
    __tablename__ = 'artist_transport'
    artist_id = Column(Integer, ForeignKey("artist.artist_id"))
    transport_id = Column(Integer, ForeignKey("transport.transport_id"))

class TransportSchedule(Base):
    __tablename__ = 'transport_schedule'
    transport_id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('car.car_id'))
    pickup_time = Column(DateTime(timezone=True))
    dropoff_time = Column(DateTime(timezone=True))
    location_from = Column(String)
    location_to = Column(String)
    number_guests = Column(Integer)
    comments = Column(String)
    booked = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)

class Car(Base):
    __tablename__ = 'car'
    car_id = Column(Integer, primary_key=True, index=True )
    car_type = Column(String)

class ArtistLodgeSchedule(Base):
    __tablename__ = 'artist_lodge_schedule'
    artist_id = Column(Integer, ForeignKey("artist.artist_id"))
    lodge_schedule_id = Column(Integer, ForeignKey("lodge_schedule.lodge_schedule_id"))

class LodgeSchedule(Base):
    __tablename__ = 'lodge_schedule'
    lodge_schedule_id = Column(Integer, primary_key=True, index=True)
    lodge_id = Column(Integer, ForeignKey("lodge.lodge_id"))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    comments = Column(String)

class Lodge(Base):
    __tablename__ = 'lodge'
    lodge_id = Column(Integer, primary_key=True, index=True )
    lodge_name = Column(String)
    lodge_size = Column(String)
    comments = Column(String)

class ArtistAct(Base):
    __tablename__ = 'artist_act'
    artist_id = Column(Integer, ForeignKey("artist.artist_id"))
    act_id = Column(Integer, ForeignKey("act.act_id"))

class Act(Base):
    __tablename__ = 'act'
    act_id = Column(Integer, primary_key=True, index=True)
    act_name = Column(String)
    stage_id = Column(Integer, ForeignKey("stage.stage_id"))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    comments = Column(String)

class Stage(Base):
    __tablename__ = 'stage'
    stage_id = Column(Integer, primary_key=True, index=True )
    stage_name = Column(String)
