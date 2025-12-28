from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_db

router = APIRouter()

@router.get("/vendas")
def listar_vendas(db: Session = Depends(get_db)):
    # O comando text() garante compatibilidade com o SQLAlchemy
    query = text("SELECT id, email, produto, transaction_id, status, data FROM vendas ORDER BY id DESC")
    try:
        result = db.execute(query)
        vendas = [dict(row._mapping) for row in result]
        return {"vendas": vendas}
    except Exception:
        return {"vendas": [], "message": "Tabela ainda não criada ou vazia"}

@router.get("/acessos")
def listar_acessos(db: Session = Depends(get_db)):
    query = text("SELECT id, email, credits, livro_liberado, premium FROM acessos ORDER BY id DESC")
    try:
        result = db.execute(query)
        acessos = [dict(row._mapping) for row in result]
        return {"acessos": acessos}
    except Exception:
        return {"acessos": [], "message": "Tabela ainda não criada ou vazia"}
