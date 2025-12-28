from fastapi import FastAPI
from db import engine, Base
import logging

# Configuração de logs para monitoramento no Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MegaSorte API",
    description="Backend para integração com Kiwify e gerenciamento de acessos",
    version="0.1.0"
)

# CRIAÇÃO AUTOMÁTICA DE TABELAS
# O SQLAlchemy criará as tabelas 'vendas', 'acessos', etc., se elas não existirem
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas do banco de dados verificadas/criadas com sucesso.")
except Exception as e:
    logger.error(f"Erro ao criar tabelas: {e}")

# ROTA DE SAÚDE (Para testar se o site está no ar)
@app.get("/")
def home():
    return {"status": "online", "message": "MegaSorte API rodando com sucesso"}

# IMPORTAÇÃO DOS ROTEADORES (Com tratamento de erro individual)

# 1. Webhook (Kiwify)
try:
    from webhook import router as webhook_router
    app.include_router(webhook_router, prefix="/api", tags=["Webhook"])
    logger.info("Módulo Webhook carregado.")
except Exception as e:
    logger.warning(f"AVISO: Webhook não carregado: {e}")

# 2. Admin (Listagem de Vendas/Acessos)
try:
    from admin import router as admin_router
    app.include_router(admin_router, prefix="/api", tags=["Admin"])
    logger.info("Módulo Admin carregado.")
except Exception as e:
    logger.warning(f"AVISO: Admin não carregado: {e}")

# 3. Plays (Lógica de Jogos/Tokens)
try:
    from plays import router as plays_router
    app.include_router(plays_router, prefix="/api", tags=["Plays"])
    logger.info("Módulo Plays carregado.")
except Exception as e:
    logger.warning(f"AVISO: Plays não carregado: {e}")

# 4. Entries (Entradas de Dados)
try:
    from entries.router import router as entries_router
    app.include_router(entries_router, prefix="/api", tags=["Entries"])
    logger.info("Módulo Entries carregado.")
except Exception as e:
    logger.warning(f"AVISO: Entries não carregado: {e}")

# 5. Analytics (Gráficos e Mapas)
try:
    from analytics.router import router as analytics_router
    app.include_router(analytics_router, prefix="/api", tags=["Analytics"])
    logger.info("Módulo Analytics carregado.")
except Exception as e:
    logger.warning(f"AVISO: Analytics não carregado: {e}")
