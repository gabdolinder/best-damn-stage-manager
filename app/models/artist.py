from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import List, Optional
from sqlmodel import Relationship

class Artist(SQLModel, table=True):
    artist_id: int = Field(default=None, primary_key=True)
    ticket_holder_id: int = Field(foreign_key="ticket_holder.ticket_holder_id")
    artist_name: str
    comment: Optional[str] = Field(default="", max_length=10000)
    pr_text: Optional[str] = Field(default="", max_length=10000)
    riders: List["Rider"] = Relationship(back_populates="artist")
    pictures: List["Picture"] = Relationship(back_populates="artist")

class Rider(SQLModel, table=True):
    file_id: int = Field(default=None, primary_key=True)
    filename: str
    file_path: str
    artist_id: int = Field(foreign_key="artist.artist_id")
    artist: Artist = Relationship(back_populates="riders")

class Picture(SQLModel, table=True):
    file_id: int = Field(default=None, primary_key=True)
    filename: str
    file_path: str
    artist_id: int = Field(foreign_key="artist.artist_id")
    artist: Artist = Relationship(back_populates="pictures")

class Volounteer(SQLModel, table=True):
    volounteer_id: int = Field(default=None, primary_key=True)
    volounteer_name: str

class ArtistAct(SQLModel, table=True):
    __tablename__ = 'artist_act'
    artist_act_id: int = Field(default=None, primary_key=True)
    artist_id: int = Field(foreign_key="artist.artist_id")
    act_id: int = Field(foreign_key="act.act_id")

class ArtistLodge(SQLModel, table=True):
    __tablename__ = 'artist_lodge'
    artist_lodge_id: int = Field(default=None, primary_key=True)
    artist_id: int = Field(foreign_key="artist.artist_id")
    lodge_id: int = Field(foreign_key="lodge.lodge_id")

class ArtistVolounteer(SQLModel, table=True):
    __tablename__ = 'artist_volounteer'
    artist_volounteer_id: int = Field(default=None, primary_key=True)
    artist_id: int = Field(foreign_key="artist.artist_id")
    volounteer_id: int = Field(foreign_key="volounteer.volounteer_id")

class ArtistTransport(SQLModel, table=True):
    __tablename__ = 'artist_transport'
    artist_transport_id: int = Field(default=None, primary_key=True)
    artist_id: int = Field(foreign_key="artist.artist_id")
    transport_id: int = Field(foreign_key="transport_schedule.transport_id")
