from app.db.session import SessionLocal
from app.models.user import User
from app.utils.jwt_handler import create_access_token, decode_token
from app.utils.password_handler import hash_password
from app.services.mail_service import send_email
from datetime import timedelta

RESET_TOKEN_EXPIRE_MINUTES = 15

async def send_reset_email(email: str, frontend_url: str | None = None):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        token = create_access_token(subject=str(user.email), expires_minutes=RESET_TOKEN_EXPIRE_MINUTES)
        link = f"{frontend_url or 'https://seusite.com'}/reset-password?token={token}"
        body = f"Olá {user.name},\n\nClique no link para redefinir sua senha:\n{link}\n\nSe você não solicitou, ignore este e-mail." 
        await send_email("Redefinição de senha", [email], body)
        return True
    finally:
        db.close()

def reset_password(token: str, new_password: str):
    db = SessionLocal()
    try:
        payload = decode_token(token)
        email = payload.get('sub')
        if not email:
            return False
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        user.password_hash = hash_password(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return True
    except Exception:
        return False
    finally:
        db.close()
