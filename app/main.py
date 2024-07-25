from fastapi import FastAPI, Depends
import uvicorn
from api import ticket_holders, ticket_holder_guests, issued_tickets, ticket_types, ticket_holder_types
from database import Base, engine, SessionLocal
from crud import insert_ticket_type_data
from contextlib import asynccontextmanager
from frontend import login, artist, guestlist, home


# Create tables
Base.metadata.create_all(bind=engine)

def on_startup():
    db = SessionLocal()
    try:
        insert_ticket_type_data(db)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup()
    yield


app = FastAPI(lifespan=lifespan)

# Frontend routes
app.include_router(home.router, tags=["home"])
app.include_router(login.router, prefix="/login", tags=["login"])
app.include_router(artist.router, prefix="/artist", tags=["artist"])
app.include_router(guestlist.router, prefix="/guestlist", tags=["guestlist"])

# API routes
app.include_router(ticket_holders.router, prefix="/ticket_holders", tags=["API/ticket_holders"])
app.include_router(ticket_holder_guests.router, prefix="/ticket_holder_guests", tags=["API/ticket_holder_guests"])
app.include_router(issued_tickets.router, prefix="/issued_tickets", tags=["API/issued_tickets"])
app.include_router(ticket_types.router, prefix="/ticket_types", tags=["API/ticket_types"])
app.include_router(ticket_holder_types.router, prefix="/ticket_holder_types", tags=["API/ticket_holder_types"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
