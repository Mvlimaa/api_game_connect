from app.utils.password_handler import hash_password, verify_password
from app.utils.jwt_handler import create_access_token, decode_token, get_current_user as _get_current_user_jwt

__all__ = ["hash_password", "verify_password", "create_access_token", "decode_token", "get_current_user", "get_current_user_from_token"]

def get_current_user_from_token(token: str):
    from fastapi import HTTPException, status
    from app.db.session import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        user = db.query(User).filter(User.id == sub).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
        return user
    finally:
        db.close()

get_current_user = _get_current_user_jwt
