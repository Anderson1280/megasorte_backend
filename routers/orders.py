# backend/orders.py
import hmac
import hashlib
import json
from fastapi import APIRouter, Request, HTTPException
from db import get_db
from models import User

router = APIRouter()

# 🔥 Coloque aqui a sua chave secreta do Webhook da Kiwify
KIWIFY_SECRET = "SUA_CHAVE_SECRETA_AQUI"


def verify_signature(secret: str, payload: bytes, signature: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/webhook/kiwify")
async def kiwify_webhook(request: Request):
    raw_body = await request.body()

    signature = request.headers.get("X-Kiwify-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Signature missing")

    # 🔒 Validando assinatura
    if not verify_signature(KIWIFY_SECRET, raw_body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    data = await request.json()
    event_type = data.get("event")

    # Dados importantes
    email = data["data"]["customer_email"]
    status = data["data"]["status"]
    product_name = data["data"]["product_name"]

    db = next(get_db())

    # Localiza usuário pelo email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Caso o usuário ainda não exista, cria automaticamente
        user = User(email=email, hashed_password="", is_premium=False, credits=0)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Apenas confirmar pagamento aprovado
    if status == "approved":

        # 🟦 Se o produto comprado for o LIVRO PREMIUM
        if "Mente Leve, Vida Plena" in product_name:
            user.is_premium = True  # libera acesso ao livro

        # 🟩 Se o produto for créditos
        if "créditos" in product_name.lower():
            user.credits += 10  # exemplo: adiciona 10 créditos

        db.commit()

    return {"status": "success"}
