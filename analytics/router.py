from fastapi import APIRouter
from analytics.generator import generate_balanced_game

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/generate")
def get_game(region: str = None):
    # Simulação de sorteios históricos para o gerador
    mock_history = [
        [1, 10, 20, 30, 40, 50],
        [5, 15, 25, 35, 45, 55]
    ]
    jogo = generate_balanced_game(mock_history, region=region)
    return jogo
