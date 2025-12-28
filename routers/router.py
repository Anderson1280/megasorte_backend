from fastapi import APIRouter, Depends
from auth.jwt_utils import verificar_token

router = APIRouter(prefix="/premium", tags=["Créditos Premium"])

@router.get("/")
def area_premium(user_id: int = Depends(verificar_token)):
    return {"mensagem": f"Bem-vindo à área premium! Seu user_id: {user_id}"}
