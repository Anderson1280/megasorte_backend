from fastapi import FastAPI
from db import engine, Base

app = FastAPI(
    title="MegaSorte API",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)
# Routers
try:
    from webhook import router as webhook_router
    app.include_router(webhook_router, prefix="/api")
except Exception as e:
    log.warning(f"webhook não carregado: {e}")

try:
    from plays import router as plays_router
    app.include_router(plays_router, prefix="/api")
except Exception as e:
    log.warning(f"plays não carregado: {e}")

try:
    from admin import router as admin_router
    app.include_router(admin_router, prefix="/api")
except Exception as e:
    log.warning(f"admin não carregado: {e}")

try:
    from entries.router import router as entries_router
    app.include_router(entries_router, prefix="/api")
except Exception as e:
    log.warning(f"entries não carregado: {e}")

try:
    from analytics.router import router as analytics_router
    app.include_router(analytics_router, prefix="/api")
except Exception as e:
    log.warning(f"analytics não carregado: {e}")
