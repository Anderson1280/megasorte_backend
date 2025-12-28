# backend/webhook.py
from fastapi import APIRouter, Request, HTTPException
import hmac, hashlib, os, logging

router = APIRouter()
log = logging.getLogger("uvicorn.error")

KIWIFY_SECRET = os.getenv("KIWIFY_SECRET", "MEGA_SORTE_2025_SECRET")  # definir em env no Render

def verify_signature(payload_bytes: bytes, signature_header: str) -> bool:
    # Kiwify pode enviar assinatura HMAC (ajuste se diferente)
    mac = hmac.new(KIWIFY_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature_header)

@router.post("/webhook/kiwify")
async def kiwify_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("x-kiwify-signature", "")
    try:
        if not verify_signature(body, signature):
            raise HTTPException(status_code=401, detail="Signature invalid")

        event = await request.json()
        # EX: event = { "event": "PURCHASE_APPROVED", "data": { ... } }
        evt = event.get("event")
        data = event.get("data", {})
        if evt == "PURCHASE_APPROVED":
            # lógica: localizar usuário por email e adicionar créditos / ativar download
            buyer_email = data.get("buyer", {}).get("email")
            # chamar função interna para creditar, gravar transação etc.
            # ex: add_credits_to_user(email=buyer_email, credits=10, reason="Kiwify purchase")
            log.info(f"Compra aprovada para {buyer_email}")
            return {"status":"ok","message":"Acesso Premium liberado"}
        return {"status":"ok","message":"event ignored"}
    except Exception as e:
        log.exception("Erro processando webhook")
        raise HTTPException(status_code=500, detail=str(e))
