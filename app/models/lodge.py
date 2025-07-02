from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class LodgeSchedule(SQLModel, table=True):
    __tablename__ = 'lodge_schedule'
    lodge_schedule_id: int = Field(default=None, primary_key=True)
    lodge_id: int = Field(foreign_key="lodge.lodge_id")
    start_time: datetime
    end_time: datetime
    comment: Optional[str] = Field(default="", max_length=10000)

class Lodge(SQLModel, table=True):
    lodge_id: int = Field(default=None, primary_key=True)
    lodge_name: str
    lodge_size: str
    comment: Optional[str] = Field(default="", max_length=10000)
