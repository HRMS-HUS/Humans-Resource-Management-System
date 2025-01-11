from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    sender_id: str
    receiver_id: str
    text: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    text: Optional[str] = None

class MessageResponse(MessageBase):
    message_id: str

    class Config:
        orm_mode = True
