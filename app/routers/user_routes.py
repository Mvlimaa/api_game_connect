from fastapi import APIRouter, Depends
from app.utils.jwt_handler import get_current_user
from app.schemas.user_schemas import UserProfile

router = APIRouter()

@router.get('/me', response_model=UserProfile)
def me(current_user=Depends(get_current_user)):
    return UserProfile(username=current_user.name, email=current_user.email, steam_id=current_user.steam_id)
