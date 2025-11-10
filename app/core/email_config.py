from fastapi_mail import ConnectionConfig
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME or "",
    MAIL_PASSWORD = settings.MAIL_PASSWORD or "",
    MAIL_FROM = settings.MAIL_FROM or "",
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME = "API Steam Postagens",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
