### INÍCIO - backend/admin.py
from fastapi import APIRouter
from db import get_db # Correto para o Render

router = APIRouter()

@router.get("/vendas")
def listar_vendas():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, email, produto, transaction_id, status, data FROM vendas ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return {"vendas": [dict(r) for r in rows]}

@router.get("/acessos")
def listar_acessos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, email, credits, livro_liberado, premium FROM acessos ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return {"acessos": [dict(r) for r in rows]}

@router.get("/stats/regions")
def stats_regions():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT region, COUNT(*) as total FROM plays WHERE region IS NOT NULL GROUP BY region ORDER BY total DESC")
    rows = cur.fetchall()
    conn.close()
    return [{"region": r[0], "total": r[1]} for r in rows]
### FIM
