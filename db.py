from fastapi import APIRouter

router = APIRouter()

@router.get("/vendas")
def listar_vendas():
    conn = get_db()
    # Se o seu get_db retornar uma conexão direta:
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
