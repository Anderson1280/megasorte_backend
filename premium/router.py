from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/")
def area_premium(user_id: int = Depends(get_current_user)):
    return {"mensagem": f"Bem-vindo à área premium! Seu user_id: {user_id}"}

