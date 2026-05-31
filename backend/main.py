from backend.database import engine, SessionLocal
from backend import models
from backend import schemas

from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session

from typing import List
from sqlalchemy import func
from fastapi import HTTPException

from fastapi import Query
from sqlalchemy import or_
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app=FastAPI()
app.mount(

    "/static",

    StaticFiles(

        directory="../frontend/static"

    ),

    name="static"

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)
Base.metadata.create_all(bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")

def dashboard():

    return FileResponse(

        "../frontend/templates/index.html"

    )

@app.get("/create")

def create_page():

    return FileResponse(

        "../frontend/templates/create_ticket.html"

    )


@app.get("/ticket")

def ticket_page():

    return FileResponse(

        "../frontend/templates/ticket.html"

    )


@app.get("/")
def home():
    return {"message":"CRM Running"}

@app.post("/tickets")

def create_ticket(
    ticket:TicketCreate,
    db:Session=Depends(get_db)

):
    last_ticket = db.query(Ticket).order_by(
    Ticket.id.desc()
).first()

    if last_ticket:
        next_number = last_ticket.id + 1

    else:

        next_number = 1
    generated_ticket_id = f"TKT-{next_number:03d}"


    new_ticket=Ticket(

        ticket_id=generated_ticket_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description

    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {

        "ticket_id":new_ticket.ticket_id,
        "status":"created"

    }





@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)

def get_tickets(

    status:str=None,
    search:str=None,
    db:Session=Depends(get_db)

):

    query=db.query(Ticket)
    if status:

        query=query.filter(

        func.lower(
            Ticket.status
        ) == status.lower()

    )

    if search:

        query=query.filter(

        or_(

            Ticket.customer_name.ilike(f"%{search}%"),
            Ticket.customer_email.ilike(f"%{search}%"),
            Ticket.ticket_id.ilike(f"%{search}%"),
            Ticket.description.ilike(f"%{search}%")
        )
    )

    return query.all()




@app.get(

    "/tickets/{ticket_id}",

    response_model=TicketDetail

)

def get_ticket(

    ticket_id:str,
    db:Session=Depends(get_db)

):

    ticket=db.query(Ticket).filter(

        Ticket.ticket_id==ticket_id

    ).first()

    if not ticket:

        raise HTTPException(

            status_code=404,
            detail="Ticket Not Found"

        )

    return ticket



@app.put(
    "/tickets/{ticket_id}"
)

def update_ticket(

    ticket_id:str,

    data:TicketUpdate,

    db:Session=Depends(get_db)

):

    ticket=db.query(
        Ticket
    ).filter(

        Ticket.ticket_id==ticket_id

    ).first()

    if not ticket:

        raise HTTPException(

            status_code=404,

            detail="Ticket Not Found"

        )

    ticket.status=data.status

    new_note=Note(

        ticket_id=ticket_id,

        note_text=data.notes

    )

    db.add(new_note)

    db.commit()

    return {

        "success":True

    }