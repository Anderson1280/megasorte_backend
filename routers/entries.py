# Arquivo: backend/entries.py - Módulo de Rotas e Modelos para Jogos de Usuário

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from pydantic import BaseModel
from typing import List
import json

from .db import Base, get_db

# ==================== MODELO DO BANCO ====================
class Entry(Base):
    """Modelo para as apostas de usuários (Jogadas com geolocalização)."""
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    numbers = Column(String, nullable=False)  # JSON string: "[1,2,3,4,5,6]"
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, default="Brasil")
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== SCHEMAS PYDANTIC ====================
class EntryCreate(BaseModel):
    numbers: List[int]
    city: str
    state: str
    country: str = "Brasil"
    lat: float
    lon: float


class EntryResponse(BaseModel):
    id: int
    numbers: List[int]
    city: str | None
    state: str | None
    country: str
    lat: float | None
    lon: float | None
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== FASTAPI ROUTER ====================
router = APIRouter(prefix="/api/entries", tags=["Entries"])


@router.post("/save", response_model=dict)
async def save_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    """
    Salva uma nova aposta de usuário no banco de dados.
    """
    try:
        numbers_json = json.dumps(entry.numbers)

        new_entry = Entry(
            numbers=numbers_json,
            city=entry.city,
            state=entry.state,
            country=entry.country,
            lat=entry.lat,
            lon=entry.lon
        )

        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return {
            "status": "success",
            "message": "Aposta salva com sucesso!",
            "id": new_entry.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar: {str(e)}")


@router.get("", response_model=List[EntryResponse])
async def get_all_entries(db: Session = Depends(get_db)):
    """
    Retorna todas as apostas salvas com geolocalização
    """
    try:
        entries = db.query(Entry).order_by(Entry.created_at.desc()).all()

        # Converter entries para response format (decodificar JSON)
        result = []
        for entry in entries:
            result.append(EntryResponse(
                id=entry.id,
                numbers=json.loads(entry.numbers),
                city=entry.city,
                state=entry.state,
                country=entry.country,
                lat=entry.lat,
                lon=entry.lon,
                created_at=entry.created_at
            ))

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar apostas: {str(e)}")