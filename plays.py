# backend/plays.py
from fastapi import APIRouter, Request, HTTPException, Depends
from datetime import datetime
from auth.jwt_utils import verificar_token
from db import get_db
import json

cur.execute("""
    SELECT COUNT(*) FROM plays
    WHERE ip = ? AND created_at >= datetime('now', '-1 minute')
""", (request.client.host,))

if cur.fetchone()[0] >= 5:
    raise HTTPException(429, "Muitas requisições. Aguarde.")

router = APIRouter(prefix="/play", tags=["Play"])

@router.post("")
async def play(
    request: Request,
    user_id: int = Depends(verificar_token)
):
    payload = await request.json()
    round_id = payload.get("round_id")
    numbers = payload.get("numbers")
    device_fp = payload.get("device_fp")
    region = payload.get("region")

    if not round_id or not numbers:
        raise HTTPException(400, "round_id e numbers são obrigatórios")

    conn = get_db()
    cur = conn.cursor()

    # busca usuário REAL pelo JWT
    cur.execute("""
        SELECT email, credits, premium, livro_liberado
        FROM acessos
        WHERE id = ?
    """, (user_id,))
    row = cur.fetchone()

    if not row:
        raise HTTPException(403, "Usuário não encontrado")

    email, credits, premium, livro = row
    premium = bool(premium)
    livro = bool(livro)

    if not livro:
        raise HTTPException(403, "Livro não liberado")

    if premium and credits <= 0:
        cur.execute("UPDATE acessos SET premium = 0 WHERE id = ?", (user_id,))
        conn.commit()
        raise HTTPException(403, "Créditos esgotados")

    per_round_limit = 2 if premium else 1
    cur.execute("""
        SELECT COUNT(*) FROM plays
        WHERE email = ? AND round_id = ?
    """, (email, round_id))

    if cur.fetchone()[0] >= per_round_limit:
        raise HTTPException(403, "Limite por rodada atingido")

    cur.execute("""
        INSERT INTO plays
        (email, round_id, numbers, device_fingerprint, ip, region, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        email,
        round_id,
        json.dumps(numbers),
        device_fp,
        request.client.host,
        region,
        datetime.utcnow()
    ))

    if premium:
        cur.execute("UPDATE acessos SET credits = credits - 1 WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()

    return {
        "ok": True,
        "remaining_credits": max(0, credits - (1 if premium else 0))
    }
