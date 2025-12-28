from fastapi import FastAPI
from db import engine, Base
import logging

# Se você tiver um arquivo chamado models.py, descomente a linha abaixo:
# import models 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MegaSorte API", version="0.1.0")

# Este comando CRIA as tabelas no banco de dados automaticamente
Base.metadata.create_all(bind=engine)

# Inclusão dos Roteadores
try:
    from webhook import router as webhook_router
    app.include_router(webhook_router, prefix="/api")
except Exception as e:
    logger.warning(f"webhook não carregado: {e}")

try:
    from admin import router as admin_router
    app.include_router(admin_router, prefix="/api")
except Exception as e:
    logger.warning(f"admin não carregado: {e}")

# Adicione aqui os outros try/except para plays, entries e analytics se necessário
