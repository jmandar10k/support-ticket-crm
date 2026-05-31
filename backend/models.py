from sqlalchemy import Column,String,Integer,DateTime
from backend.database import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Ticket(Base):

    __tablename__="tickets"

    id=Column(Integer,primary_key=True,index=True)

    ticket_id=Column(String,unique=True)

    customer_name=Column(String)

    customer_email=Column(String)

    subject=Column(String)

    description=Column(String)

    status=Column(String,default="Open")

    created_at=Column(
        DateTime,
        default=datetime.utcnow
    )
    notes=relationship(
        "Note",
        backref="ticket"
    )
    



class Note(Base):

    __tablename__="notes"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    ticket_id=Column(
        String,
        ForeignKey(
            "tickets.ticket_id"
        )
    )

    note_text=Column(String)

    created_at=Column(
        DateTime,
        default=datetime.utcnow
    )