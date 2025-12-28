# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterIn(BaseModel):
    email: EmailStr
    senha: str

class LoginIn(BaseModel):
    email: EmailStr
    senha: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PremiumStatusOut(BaseModel):
    concurso_atual: Optional[int]
    total_jogos: int
    ja_jogou_no_concurso: bool
