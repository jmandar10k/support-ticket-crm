
from pathlib import Path
from typing import List

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from backend.database import (
    engine,
    SessionLocal
)

from backend.models import (
    Base,
    Ticket,
    Note
)

from backend.schemas import (

    TicketCreate,

    TicketResponse,

    TicketDetail,

    TicketUpdate

)


app = FastAPI()


BASE_DIR = Path(
    __file__
).resolve().parent.parent


STATIC_DIR = (

    BASE_DIR

    / "frontend"

    / "static"

)

TEMPLATE_DIR = (

    BASE_DIR

    / "frontend"

    / "templates"

)


app.mount(

    "/static",

    StaticFiles(

        directory=str(
            STATIC_DIR
        )

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


Base.metadata.create_all(
    bind=engine
)



def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()



@app.get("/")

def dashboard():

    return FileResponse(

        TEMPLATE_DIR

        / "index.html"

    )



@app.get("/create")

def create_page():

    return FileResponse(

        TEMPLATE_DIR

        / "create_ticket.html"

    )



@app.get("/ticket")

def ticket_page():

    return FileResponse(

        TEMPLATE_DIR

        / "ticket.html"

    )



@app.post("/tickets")

def create_ticket(

    ticket: TicketCreate,

    db: Session = Depends(
        get_db
    )

):

    last_ticket = db.query(
        Ticket
    ).order_by(

        Ticket.id.desc()

    ).first()


    if last_ticket:

        next_number = (

            last_ticket.id

            + 1

        )

    else:

        next_number = 1


    generated_ticket_id = (

        f"TKT-{next_number:03d}"

    )


    new_ticket = Ticket(

        ticket_id=generated_ticket_id,

        customer_name=
        ticket.customer_name,

        customer_email=
        ticket.customer_email,

        subject=
        ticket.subject,

        description=
        ticket.description

    )


    db.add(
        new_ticket
    )

    db.commit()

    db.refresh(
        new_ticket
    )


    return {

        "ticket_id":

        new_ticket.ticket_id,

        "status":

        "created"

    }



@app.get(

    "/tickets",

    response_model=

    List[TicketResponse]

)

def get_tickets(

    status: str = None,

    search: str = None,

    db: Session = Depends(
        get_db
    )

):

    query = db.query(
        Ticket
    )


    if status:

        query = query.filter(

            func.lower(

                Ticket.status

            )

            ==

            status.lower()

        )


    if search:

        query = query.filter(

            or_(

                Ticket.customer_name.ilike(

                    f"%{search}%"

                ),

                Ticket.customer_email.ilike(

                    f"%{search}%"

                ),

                Ticket.ticket_id.ilike(

                    f"%{search}%"

                ),

                Ticket.description.ilike(

                    f"%{search}%"

                )

            )

        )


    return query.all()



@app.get(

    "/tickets/{ticket_id}",

    response_model=

    TicketDetail

)

def get_ticket(

    ticket_id: str,

    db: Session = Depends(
        get_db
    )

):

    ticket = db.query(
        Ticket
    ).filter(

        Ticket.ticket_id

        ==

        ticket_id

    ).first()


    if not ticket:

        raise HTTPException(

            status_code=404,

            detail=

            "Ticket Not Found"

        )


    return ticket



@app.put(

    "/tickets/{ticket_id}"

)

def update_ticket(

    ticket_id: str,

    data: TicketUpdate,

    db: Session = Depends(
        get_db
    )

):

    ticket = db.query(
        Ticket
    ).filter(

        Ticket.ticket_id

        ==

        ticket_id

    ).first()


    if not ticket:

        raise HTTPException(

            status_code=404,

            detail=

            "Ticket Not Found"

        )


    ticket.status = data.status


    if data.notes:

        note = Note(

            ticket_id=
            ticket_id,

            note_text=
            data.notes

        )

        db.add(
            note
        )


    db.commit()


    return {

        "success": True

    }
