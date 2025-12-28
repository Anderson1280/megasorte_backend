import hmac, hashlib, json, os
from fastapi import Request, HTTPException

KIWIFY_SECRET = os.getenv("KIWIFY_SECRET")

async def verify_signature(request: Request):
    body = await request.body()
    signature = request.headers.get("x-kiwify-signature","")
    mac = hmac.new(KIWIFY_SECRET.encode(), body, hashlib.sha256).hexdigest()
    # dependendo do formato, talvez Kiwify envie base64; ajuste com base no painel
    if not hmac.compare_digest(mac, signature):
        raise HTTPException(status_code=401, detail="Signature invalid")
    return json.loads(body)
