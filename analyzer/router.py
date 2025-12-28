from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/analise")
def analise_mega():
    # Simulação de análise da MegaSena
    dezenas = random.sample(range(1, 61), 6)
    return {"analise": dezenas}
