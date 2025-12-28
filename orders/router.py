from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user

router = APIRouter()

# Simulação de pedidos/livros
pedidos = []

@router.post("/comprar")
def comprar_livro(usuario: str, livro: str, user_id: int = Depends(get_current_user)):
    pedido = {"usuario": usuario, "livro": livro}
    pedidos.append(pedido)
    return {"mensagem": "Livro comprado com sucesso!", "pedido": pedido}

@router.get("/listar")
def listar_pedidos(user_id: int = Depends(get_current_user)):
    return {"pedidos": pedidos}
