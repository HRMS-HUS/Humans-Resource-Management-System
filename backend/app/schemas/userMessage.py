from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    sender_id: Optional[str] = None
    receiver_id: str
    ext: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    text: Optional[str] = None

class MessageResponse(MessageBase):
    message_id: str

    class Config:
        orm_mode = True
