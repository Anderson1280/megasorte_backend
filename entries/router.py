from fastapi import APIRouter

router = APIRouter(
    prefix="/entries",
    tags=["Entries"]
)

@router.get("/")
def list_entries():
    return {
        "status": "ok",
        "message": "Entries router carregado com sucesso"
    }