# backend/auth_jwt.py
import os
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any

SECRET_KEY = os.getenv("JWT_SECRET", os.getenv("SECRET_KEY", "change_this_in_prod"))
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def gerar_token(user_id: int, exp_segundos: int = 3600) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=exp_segundos),
        "sub": str(user_id)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def verificar_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado!")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido!")
