
from pathlib import Path
from typing import List
import re

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
    TicketUpdate,
    ChatRequest,
    ChatResponse
)

from groq import Groq

import os
from dotenv import load_dotenv

load_dotenv(
override=True
)

print(
os.getenv(
"GROQ_API_KEY"
))

app = FastAPI()
client = Groq(
api_key=
os.getenv(

"GROQ_API_KEY"
)
)


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


@app.post(

"/chat",

response_model=ChatResponse

)

def chat(

data:ChatRequest,

db:Session=Depends(

get_db

)

):

    question = data.question.lower()


    tickets = db.query(

        Ticket

    ).order_by(

        Ticket.created_at.desc()

    ).limit(

        50

    ).all()


    context = ""


    for t in tickets:

        context += f"""

Ticket ID:

{t.ticket_id}

Customer Name:

{t.customer_name}

Customer Email:

{t.customer_email}

Subject:

{t.subject}

Status:

{t.status}

Description:

{t.description}

Created At:

{t.created_at}

-----------------------------

"""


    response = client.chat.completions.create(

        model=

        "openai/gpt-oss-120b",

        messages=[

            {

                "role":"system",

                "content": """

You are an AI assistant for customer support CRM.


Rules:

1. ONLY answer using provided ticket data.

2. Never invent information.

3. If user asks counts, calculate using provided ticket data.

4. If user asks customer names, provide them.

5. If user asks summaries, summarize.

6. If user asks open tickets, analyze ticket statuses.

7. Format answers cleanly.

8. Use bullets where useful.

9. Avoid excessive punctuation.

10. Never create markdown tables.

11. If user asks for ticket details, format like:

Ticket ID: XXX

Customer: XXX

Subject: XXX

Status: XXX

Description: XXX


12. If answer cannot be found in ticket data say:

"I could not find that information in available tickets."

13. Keep answers concise and readable.

"""

            },

            {

                "role":"user",

                "content":

f"""

User Question:

{question}


Available Ticket Data:

{context}

"""

            }

        ]

    )


    return {

        "answer":

        response.choices[0]

        .message.content

    }

