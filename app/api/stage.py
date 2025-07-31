from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from database import get_db
from crud.stage import create_stage, get_stage
from models.stage import Stage

router = APIRouter()

@router.post("/stages/", response_model=Stage)
def add_stage(stage_name: str, db: Session = Depends(get_db)):
    """Create a new stage if it doesn't already exist."""
    new_stage = create_stage(db, stage_name=stage_name)
    if new_stage:
        return new_stage
    return {"message": "Stage already exists."}

@router.get("/stages/")
def list_stages(db: Session = Depends(get_db)):
    stages = get_stage(db)
    return {"stages": [s.stage_name for s in stages]}
