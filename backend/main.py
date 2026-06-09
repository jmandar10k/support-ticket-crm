
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
from backend.gmail_service import get_gmail_service
from backend.email_cleaner import clean_email_body
from backend.auth import (
hash_password,
verify_password,
create_access_token
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import FileResponse,RedirectResponse
from fastapi.security import HTTPBearer
from fastapi import Security
from backend.auth import verify_token

from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError

from backend.database import (
    engine,
    SessionLocal
)

from backend.models import (
    Base,
    Ticket,
    Note,StatusHistory,User
)

from backend.schemas import (
    TicketCreate,
    TicketResponse,
    TicketDetail,
    TicketUpdate,
    ChatRequest,
    ChatResponse,UserSignup,UserResponse,LoginRequest
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
security=HTTPBearer()


def get_current_user(

credentials=

Security(

security

)

):

    token=credentials.credentials


    email=verify_token(

        token

    )


    if not email:

        raise HTTPException(

            status_code=401,

            detail=

            "Invalid Token"

        )


    return email

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



@app.get(

"/"

)

def root():

    return RedirectResponse(

        "/login-page"

    )



@app.get("/create")
def create_page():
    return FileResponse(
        TEMPLATE_DIR / "create_ticket.html"
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

   current_user:

    str=

    Depends(

    get_current_user

    ),

    db:Session=

    Depends(

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

    current_user:str= Depends( get_current_user ), 
    db:Session= Depends( get_db ) ):



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

    "/tickets/{ticket_id}"

)


def get_ticket(

ticket_id:str,

current_user:str=

Depends(

get_current_user

),

db:Session=

Depends(

get_db

)

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


    history=db.query(

        StatusHistory

    ).filter(

        StatusHistory.ticket_id==ticket_id

    ).order_by(

        StatusHistory.changed_at

    ).all()


    return {

        "ticket_id":

        ticket.ticket_id,

        "customer_name":

        ticket.customer_name,

        "customer_email":

        ticket.customer_email,

        "subject":

        ticket.subject,

        "description":

        ticket.description,

        "status":

        ticket.status,


        "notes":[

            {

                "note_text":

                n.note_text,

                "created_at":

                n.created_at

            }

            for n in ticket.notes

        ],


        "history":[

            {

                "old_status":

                h.old_status,

                "new_status":

                h.new_status,

                "changed_at":

                h.changed_at

            }

            for h in history

        ]

    }





@app.put(

    "/tickets/{ticket_id}"

)


def update_ticket(

ticket_id:str,

data:TicketUpdate,

current_user:str=

Depends(

get_current_user

),

db:Session=

Depends(

get_db

)

):


    ticket=db.query(

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


    old_status=ticket.status


    ticket.status=data.status


    if old_status != data.status:

        history=StatusHistory(

            ticket_id=

            ticket_id,

            old_status=

            old_status,

            new_status=

            data.status

        )

        db.add(

            history

        )


    if data.notes:

        note=Note(

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

        "success":True

    }



@app.post(

"/chat",

response_model=ChatResponse

)

def chat(

data:ChatRequest,

current_user:str=

Depends(

get_current_user

),

db:Session=

Depends(

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





@app.post(

"/sync-emails"

)


def sync_emails(

current_user:str=

Depends(

get_current_user

),

db:Session=

Depends(

get_db

)

):


    service=get_gmail_service()


    results=service.users().messages().list(

        userId="me",

        maxResults=10

    ).execute()


    messages=results.get(

        "messages",

        []

    )


    created=0

    skipped=0

    processed=0


    for msg in messages:


        processed += 1


        message=service.users().messages().get(

            userId="me",

            id=msg["id"]

        ).execute()


        headers=message["payload"].get(

            "headers",

            []

        )


        subject=""

        sender=""


        for h in headers:

            if h["name"]=="Subject":

                subject=h["value"]

            elif h["name"]=="From":

                sender=h["value"]


        customer_name=sender.split("<")[0].strip()


        customer_email=sender.split("<")[-1].replace(

            ">",

            ""

        )



        description=""

        payload=message["payload"]

        import base64


        if "parts" in payload:


            for part in payload["parts"]:


                if (

                    part.get(

                        "mimeType"

                    )

                    ==

                    "text/plain"

                ):


                    data= part["body"].get(

                        "data"

                    )


                    if data:


                        raw_text=base64.urlsafe_b64decode(

                            data

                        ).decode(

                            "utf-8",

                            errors="ignore"

                        )


                        description=clean_email_body(

                            raw_text

                        )


                        break


        else:


            data=payload.get(

                "body",

                {}

            ).get(

                "data"

            )


            if data:


                raw_text=base64.urlsafe_b64decode(

                    data

                ).decode(

                    "utf-8",

                    errors="ignore"

                )


                description=clean_email_body(

                    raw_text

                )



        existing=db.query(

            Ticket

        ).filter(

            Ticket.subject==subject,

            Ticket.customer_email==customer_email

        ).first()


        if existing:

            skipped += 1

            continue


        last_ticket = db.query(

            Ticket

        ).order_by(

            Ticket.id.desc()

        ).first()


        next_number = (

            last_ticket.id + 1

            if last_ticket

            else 1

        )


        generated_ticket_id = (

            f"TKT-{next_number:03d}"

        )


        new_ticket = Ticket(

            ticket_id=

            generated_ticket_id,

            customer_name=

            customer_name,

            customer_email=

            customer_email,

            subject=

            subject,

            description=

            description,

            status="Open"

        )


        db.add(

            new_ticket

        )


        db.flush()


        created += 1


    db.commit()


    return {

        "tickets_created":

        created,

        "skipped":

        skipped,

        "processed":

        processed

    }



@app.post(

"/signup",

response_model=

UserResponse

)

def signup(

data:UserSignup,

db:Session=

Depends(

get_db

)

):

    user= User(

        name=

        data.name,

        email=

        data.email,

        hashed_password=

        hash_password(

            data.password

        )

    )


    try:

        db.add(

            user

        )

        db.commit()

        db.refresh(

            user

        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(

            status_code=400,

            detail=

            "Email Already Exists"

        )


    return user




@app.post(

"/login"

)

def login(

data:LoginRequest,

db:Session=

Depends(

get_db

)

):

    user=db.query(

        User

    ).filter(

        User.email

        ==

        data.email

    ).first()


    if (

        not user

        or

        not verify_password(

            data.password,

            user.hashed_password

        )

    ):

        raise HTTPException(

            status_code=401,

            detail=

            "Invalid Credentials"

        )


    token=create_access_token(

        {

            "sub":

            user.email

        }

    )


    return {

        "access_token":

        token,

        "token_type":

        "bearer",

        "name":

        user.name

    }


@app.get(

"/login-page"

)

def login_page():

    return FileResponse(

         "frontend/templates/login.html"
    )


@app.get(

"/signup-page"

)

def signup_page():

    return FileResponse(

        TEMPLATE_DIR

        / "signup.html"

    )



@app.get("/dashboard")
def dashboard():
    return FileResponse(
        TEMPLATE_DIR / "index.html"
    )
