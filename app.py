from fastapi import FastAPI
from db import engine, Base
import logging

# Configuração básica de log para evitar o erro NameError
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MegaSorte API",
    version="0.1.0"
)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Routers
try:
    from webhook import router as webhook_router
    app.include_router(webhook_router, prefix="/api")
except Exception as e:
    logger.warning(f"webhook não carregado: {e}")

try:
    from plays import router as plays_router
    app.include_router(plays_router, prefix="/api")
except Exception as e:
    logger.warning(f"plays não carregado: {e}")

try:
    from admin import router as admin_router
    app.include_router(admin_router, prefix="/api")
except Exception as e:
    logger.warning(f"admin não carregado: {e}")

try:
    from entries.router import router as entries_router
    app.include_router(entries_router, prefix="/api")
except Exception as e:
    logger.warning(f"entries não carregado: {e}")

try:
    from analytics.router import router as analytics_router
    app.include_router(analytics_router, prefix="/api")
except Exception as e:
    logger.warning(f"analytics não carregado: {e}")