from sqlmodel import select
from sqlalchemy.orm import Session
from models.stage import Stage

def create_stage(db: Session, stage_name: str):
    """Creates a new stage if it doesn't already exist."""
    existing_stage = db.execute(select(Stage).filter(Stage.stage_name == stage_name)).scalar_one_or_none()

    # If it doesn't exist, add the new stage
    if not existing_stage:
        new_stage = Stage(stage_name=stage_name)
        db.add(new_stage)
        db.commit()
        db.refresh(new_stage)
        return new_stage
    return None

def insert_stage(db: Session):
    stages = [
        "kinky scen",
        "stora scen",
        "regnbågen",
    ]

    # Insert each stage using the generic create_stage function
    new_stage_name = []
    for stage_name in stages:
        created_stage = create_stage(db, stage_name)
        if created_stage:
            new_stage_name.append(created_stage)

    return new_stage_name


def get_stage(db: Session):
    result = db.execute(select(Stage))
    return result.scalars().all()  # Fetch all stages
