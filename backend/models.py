
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base



class Ticket(Base):

    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True,
        index=True

    )


    ticket_id = Column(
        String(20),
        unique=True,
        nullable=False

    )


    customer_name = Column(
        String(100),
        nullable=False

    )


    customer_email = Column(
        String(150),
        nullable=False

    )


    subject = Column(
        String(200),
        nullable=False

    )


    description = Column(
        Text

    )


    status = Column(
        String(30),
        default="Open"

    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow

    )


    notes = relationship(
        "Note",
        backref="ticket",
        cascade="all, delete"

    )




class Note(Base):

    __tablename__ = "notes"

    id = Column(
        Integer,
        primary_key=True,
        index=True

    )

    ticket_id = Column(
        String(20),
        ForeignKey(
            "tickets.ticket_id"
        )

    )
    note_text = Column(
        Text
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow

    )



class StatusHistory(Base):

    __tablename__="status_history"


    id=Column(

        Integer,

        primary_key=True,

        index=True

    )


    ticket_id=Column(

        String(20),

        ForeignKey(

            "tickets.ticket_id"

        )

    )


    old_status=Column(

        String(50)

    )


    new_status=Column(

        String(50)

    )


    changed_at=Column(

        DateTime,

        default=datetime.utcnow

    )




class User(Base):

    __tablename__="users"


    id=Column(

        Integer,

        primary_key=True,

        index=True

    )


    name=Column(

        String(100)

    )


    email=Column(

        String(120),

        unique=True,

        index=True

    )


    hashed_password=Column(

        String(255)

    )


    role=Column(

        String(50),

        default="agent"

    )


    created_at=Column(

        DateTime,

        default=datetime.utcnow

    )
