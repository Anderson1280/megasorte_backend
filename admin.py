from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_db

router = APIRouter()

@router.get("/vendas")
def listar_vendas(db: Session = Depends(get_db)):
    # Usamos db.execute(text(...)) porque o get_db fornece uma sessão do SQLAlchemy
    query = text("SELECT id, email, produto, transaction_id, status, data FROM vendas ORDER BY id DESC")
    result = db.execute(query)
    # Converte o resultado para dicionário
    vendas = [dict(row._mapping) for row in result]
    return {"vendas": vendas}

@router.get("/acessos")
def listar_acessos(db: Session = Depends(get_db)):
    query = text("SELECT id, email, credits, livro_liberado, premium FROM acessos ORDER BY id DESC")
    result = db.execute(query)
    acessos = [dict(row._mapping) for row in result]
    return {"acessos": acessos}

@router.get("/stats/regions")
def stats_regions(db: Session = Depends(get_db)):
    query = text("SELECT region, COUNT(*) as total FROM plays WHERE region IS NOT NULL GROUP BY region ORDER BY total DESC")
    result = db.execute(query)
    return [{"region": row[0], "total": row[1]} for row in result]
