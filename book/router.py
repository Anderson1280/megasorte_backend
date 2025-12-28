from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db import get_db
from models import User
from auth.jwt_utils import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not pwd_context.verify(senha, user.hashed_password):
        raise HTTPException(401, "Credenciais inválidas")

    token = criar_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
