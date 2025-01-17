import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from typing import List
from ..configs.email import config

async def send_mail(subject: str, recipient: List[str], message: str):
    message = MessageSchema(
        subject = subject,
        recipients = recipient,
        body = message,
        subtype = "html"
    )
    fm = FastMail(config)
    await fm.send_message(message)