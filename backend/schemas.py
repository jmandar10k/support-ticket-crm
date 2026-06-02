from pydantic import BaseModel
from datetime import datetime

class TicketCreate(BaseModel):

    customer_name:str
    customer_email:str
    subject:str
    description:str




class TicketResponse(BaseModel):

    ticket_id:str
    customer_name:str
    subject:str
    status:str
    created_at:datetime


    class Config:

        from_attributes=True

class NoteResponse(BaseModel):

    note_text:str

    created_at:datetime

    class Config:

        from_attributes=True

class TicketDetail(BaseModel):

    ticket_id:str
    customer_name:str
    customer_email:str
    subject:str
    description:str
    status:str
    created_at:datetime
    notes:list[NoteResponse]=[]


    class Config:

        from_attributes=True


class TicketUpdate(BaseModel):

    status:str
    notes:str

class ChatRequest(BaseModel):
    question:str

class ChatResponse(BaseModel):
    answer:str