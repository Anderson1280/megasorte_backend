from fastapi import APIRouter
from analytics.generator import generate_balanced_game

# Define o roteador. O prefixo aqui se soma ao do app.py
router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/generate")
def get_game(region: str = None):
    """
    Rota para gerar jogos baseados em estatísticas.
    Exemplo: /api/analytics/generate?region=SP
    """
    # Simulamos um histórico para o gerador funcionar imediatamente
    mock_history = [
        [1, 10, 20, 30, 40, 50],
        [5, 15, 25, 35, 45, 55],
        [2, 12, 22, 32, 42, 52]
    ]
    
    try:
        jogo = generate_balanced_game(mock_history, region=region)
        return jogo
    except Exception as e:
        return {"error": f"Falha ao gerar jogo: {str(e)}"}
