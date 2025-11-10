from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME = "API Steam Postagens",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(subject: str, recipients: list[str], body: str):
    message = MessageSchema(subject=subject, recipients=recipients, body=body, subtype="plain")
    fm = FastMail(conf)
    await fm.send_message(message)
