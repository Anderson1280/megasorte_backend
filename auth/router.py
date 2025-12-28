# backend/auth/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db import get_db
from models import User
from schemas import LoginIn, TokenOut
from auth.jwt_utils import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not pwd_context.verify(data.senha, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
