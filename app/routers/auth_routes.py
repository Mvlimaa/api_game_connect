from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.utils.password_handler import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.schemas.auth_schemas import UserCreate, Token, UserOut, LoginIn
from app.services.password_reset_service import send_reset_email, reset_password as service_reset
from pydantic import BaseModel, EmailStr

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email já cadastrado')
    user = User(name=user_in.name, email=user_in.email, password_hash=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id=str(user.id), name=user.name, email=user.email)

@router.post('/login', response_model=Token)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciais inválidas')
    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    frontend_url: str | None = None

@router.post('/forgot-password')
async def forgot_password(req: ForgotPasswordRequest):
    ok = await send_reset_email(req.email, frontend_url=req.frontend_url)
    if not ok:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return {'message': 'E-mail de redefinição enviado com sucesso.'}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post('/reset-password')
def reset_password_route(req: ResetPasswordRequest):
    ok = service_reset(req.token, req.new_password)
    if not ok:
        raise HTTPException(status_code=400, detail='Token inválido ou expirado.')
    return {'message': 'Senha redefinida com sucesso.'}
