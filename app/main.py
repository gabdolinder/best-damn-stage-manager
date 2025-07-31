from fastapi import FastAPI
from database import init_db, get_db
from api import ticket, transport, stage, artist, lodge
from crud.ticket import insert_ticket_types, insert_ticket_holder_types
from crud.stage import insert_stage

app = FastAPI()

@app.on_event("startup")

def startup():
    init_db()
    db = get_db()  
    insert_ticket_types(db)
    insert_ticket_holder_types(db)
    insert_stage(db)
    db.close() 


app.include_router(artist.router, prefix="/artist", tags=["API/artist"])
app.include_router(lodge.router, prefix="/lodge", tags=["API/lodge"])
app.include_router(ticket.router, prefix="/ticket", tags=["API/ticket"])
app.include_router(transport.router, prefix="/transport", tags=["API/transport"])
app.include_router(stage.router, prefix="/stage", tags=["API/stage"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
