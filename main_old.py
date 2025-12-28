from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
from datetime import datetime

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de dados
class PlayEntry(BaseModel):
    numbers: List[int]
    city: str
    state: str
    country: str
    lat: float
    lon: float


# Endpoint para salvar jogada
@app.post("/save_entry")
async def save_entry(entry: PlayEntry):
    data = entry.dict()
    data['timestamp'] = datetime.now().isoformat()

    try:
        with open("jogadas.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

        print(f"✅ Jogada salva: {data}")
        return {"status": "success", "message": "Jogo salvo!"}

    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"status": "error", "message": str(e)}


# Endpoint para buscar jogadas
@app.get("/players_locations")
async def get_players():
    try:
        with open("jogadas.json", "r", encoding="utf-8") as f:
            jogadas = [json.loads(line) for line in f]
        return jogadas
    except FileNotFoundError:
        return []


@app.get("/")
async def root():
    return {"message": "Backend MegaSorte rodando! 🎲"}