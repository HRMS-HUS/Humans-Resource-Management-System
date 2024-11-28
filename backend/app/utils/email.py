import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from typing import List

load_dotenv()

config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

async def send_mail(subject: str, recipient: List[str], message: str):
    message = MessageSchema(
        subject = subject,
        recipients = recipient,
        body = message,
        subtype = "html"
    )
    fm = FastMail(config)
    await fm.send_message(message)