# backend/routes/book.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import os

# Ajuste: importe aqui sua dependência de autenticação existente
# Exemplo: from auth import get_current_user
# Ele deve retornar o usuário (objeto) ou lançar 401 se não estiver logado.
try:
    from auth import get_current_user
except Exception:
    # fallback: criar stub que permite uso sem auth (apenas para dev)
    def get_current_user():
        raise HTTPException(status_code=401, detail="configure get_current_user in routes/book.py")

router = APIRouter()

# Caminhos reais dos PDFs no backend
# Você informou que tem 'books' e/ou 'files' em backend; ajuste conforme necessário.
BOOK_DIR = os.path.join(os.path.dirname(__file__), "..", "book")
BOOK_INTRO = os.path.normpath(os.path.join(BOOK_DIR, "book_intro_15_pages.pdf"))  # coloque o PDF aqui
BOOK_FULL = os.path.normpath(os.path.join(BOOK_DIR, "Mente_Leve_Vida_Plena.pdf"))  # PDF completo aqui

# UTIL helpers: validações / marcação de compra
# TODO: implementar usando seu DB/models. Aqui deixei uma versão simples que você substitui
def user_has_book_paid(user) -> bool:
    """
    TODO: substituir por consulta ao seu DB (models.py).
    Exemplo com SQLAlchemy:
      return user.book_paid
    """
    if hasattr(user, "book_paid"):
        return bool(user.book_paid)
    # fallback: false
    return False

def mark_user_book_paid(user):
    """
    TODO: implementar a atualização no DB para marcar que o user comprou o livro.
    Exemplo: user.book_paid = True; db.session.commit()
    """
    # se o objeto tiver atributo, altere em memória (temporário)
    if hasattr(user, "book_paid"):
        try:
            user.book_paid = True
        except Exception:
            pass
    return True

# Rota pública para baixar a amostra (15 páginas)
@router.get("/livro/intro", response_class=FileResponse)
def get_livro_intro():
    if not os.path.exists(BOOK_INTRO):
        raise HTTPException(status_code=404, detail="Amostra não encontrada no servidor.")
    # entrega como anexo (nome amigável)
    return FileResponse(BOOK_INTRO, filename="MenteLeveVidaPlena-INTRO.pdf", media_type="application/pdf")

# Rota para iniciar compra PIX (gera um payment_id e um qr_code simulado)
@router.post("/livro/start-payment")
def start_payment(user = Depends(get_current_user)):
    """
    Retorna um payment_id (simulado) e um payload com QR code/texto do PIX.
    No seu fluxo real: gere um pagamento no provedor PIX e salve no DB.
    """
    # EXEMPLO SIMPLIFICADO: gere um payment_id único (timestamp)
    import time, uuid
    payment_id = str(uuid.uuid4())
    qr_text = f"pix://pagamento/{payment_id}?valor=19.90&fav={getattr(user,'id', 'anon')}"
    # Salve no DB: payment_id -> pending (TODO). Aqui retornamos ao frontend e esperamos confirmação
    return {"payment_id": payment_id, "qr": qr_text, "message": "PIX gerado (simulado). Envie comprovante ou confirme via /livro/confirm-payment"}

# Rota para confirmar pagamento (chamada pelo admin ou webhook)
@router.post("/livro/confirm-payment/{payment_id}")
def confirm_payment(payment_id: str, user = Depends(get_current_user)):
    """
    Em produção: webhook do processador/conta bancária confirmaria automaticamente.
    Aqui, marcamos o usuário como 'paid' para permitir download.
    """
    # TODO: validar payment_id no DB (se estiver usando)
    ok = mark_user_book_paid(user)
    if not ok:
        raise HTTPException(status_code=500, detail="Erro ao marcar pagamento.")
    return JSONResponse(status_code=200, content={"status":"ok", "detail":"Pagamento confirmado. Livro liberado."})

# Endpoint para baixar o livro completo — apenas usuários com pagamento confirmado
@router.get("/livro/download", response_class=FileResponse)
def download_full_book(user = Depends(get_current_user)):
    if not user_has_book_paid(user):
        raise HTTPException(status_code=403, detail="Livro não liberado. Compre primeiro.")
    if not os.path.exists(BOOK_FULL):
        raise HTTPException(status_code=404, detail="Livro completo não encontrado no servidor.")
    return FileResponse(BOOK_FULL, filename="MenteLeveVidaPlena-FULL.pdf", media_type="application/pdf")
