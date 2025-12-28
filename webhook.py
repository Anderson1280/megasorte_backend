### INÍCIO - backend/webhook.py
from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from db import get_db
import os

router = APIRouter()

@router.post("/webhook/kiwify")
async def kiwify_webhook(request: Request):
    # valida token enviado no header (configurado no painel Kiwify)
    secret = request.headers.get("x-kiwify-signature") or request.headers.get("X-Kiwify-Signature")
    expected = os.getenv("KIWIFY_SECRET")
    if expected and secret != expected:
        raise HTTPException(status_code=401, detail="Token inválido")

    data = await request.json()
    if data.get("event") != "PURCHASE_APPROVED":
        return {"ignored": True}

    info = data.get("data", {})
    email = info.get("buyer", {}).get("email")
    produto = info.get("product", {}).get("name")
    purchase = info.get("purchase", {})
    transaction = purchase.get("transaction") or purchase.get("id") or ""
    status = purchase.get("status") or "APPROVED"

    conn = get_db()
    cur = conn.cursor()
    # cria tabelas caso não existam
    cur.execute("""CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT, produto TEXT, transaction_id TEXT, status TEXT, data DATETIME
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS acessos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        credits INTEGER DEFAULT 10,
        livro_liberado INTEGER DEFAULT 0,
        premium INTEGER DEFAULT 0
    )""")
    # registra venda
    cur.execute("INSERT INTO vendas (email, produto, transaction_id, status, data) VALUES (?, ?, ?, ?, ?)",
                (email, produto, transaction, status, datetime.now()))
    # cria/atualiza acesso premium
    cur.execute("SELECT * FROM acessos WHERE email = ?", (email,))
    exists = cur.fetchone()
    if not exists:
        cur.execute("INSERT INTO acessos (email, credits, livro_liberado, premium) VALUES (?, ?, ?, ?)",
                    (email, 10, 1, 1))
    else:
        cur.execute("UPDATE acessos SET premium = 1, credits = 10, livro_liberado = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    return {"ok": True, "email": email}
### FIM
