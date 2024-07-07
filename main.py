from fastapi import FastAPI
import uvicorn
from routers import ticket_holders, ticket_holder_guests, issued_tickets, ticket_types, ticket_holder_types
from database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ticket Management API"}


app.include_router(ticket_holders.router, prefix="/ticket_holders", tags=["ticket_holders"])
app.include_router(ticket_holder_guests.router, prefix="/ticket_holder_guests", tags=["ticket_holder_guests"])
app.include_router(issued_tickets.router, prefix="/issued_tickets", tags=["issued_tickets"])
app.include_router(ticket_types.router, prefix="/ticket_types", tags=["ticket_types"])
app.include_router(ticket_holder_types.router, prefix="/ticket_holder_types", tags=["ticket_holder_types"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
