from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Act(SQLModel, table=True):
    act_id: int = Field(default=None, primary_key=True)
    act_name: str
    stage_id: int = Field(foreign_key="stage.stage_id")
    start_time: datetime
    end_time: datetime
    comment: Optional[str] = Field(default="", max_length=10000)

class Stage(SQLModel, table=True):
    stage_id: int = Field(default=None, primary_key=True)
    stage_name: str
    