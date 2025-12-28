import sqlite3
from .db import get_db
from datetime import datetime

def check_premium_limits(email: str, round_id: int):
    conn = get_db()
    cur = conn.cursor()

    # localizar usuário
    cur.execute("SELECT premium, credits FROM acessos WHERE email = ?", (email,))
    row = cur.fetchone()

    premium = row[0] if row else 0
    credits = row[1] if row else 0

    # quantas jogadas fez nesta rodada
    cur.execute(
        "SELECT COUNT(*) FROM plays WHERE email = ? AND round_id = ?",
        (email, round_id)
    )
    count = cur.fetchone()[0]

    if premium:
        if credits <= 0:
            raise Exception("Você não tem mais créditos Premium. Volta ao modo Free.")
        if count >= 2:
            raise Exception("Limite Premium: 2 jogadas por rodada.")
        # consome 1 crédito por rodada
        cur.execute("UPDATE acessos SET credits = credits - 1 WHERE email = ?", (email,))
        conn.commit()
    else:
        if count >= 1:
            raise Exception("Limite Free: 1 jogada por rodada.")
