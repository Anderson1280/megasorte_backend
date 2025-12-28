from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from auth.router import router as auth_router
from orders.router import router as orders_router
from premium.router import router as premium_router
from entries.router import router as entries_router
from analyzer.router import router as analyzer_router

app = FastAPI(
    title="Mega Sorte API",
    version="2.0.0",
    description="Backend completo MegaSorte"
)

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas públicas
@app.get("/")
async def root():
    return {"message": "MegaSorte backend online"}

@app.get("/health")
async def health():
    return {"status": "OK"}

# Incluir routers
app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(premium_router)
app.include_router(entries_router)
app.include_router(analyzer_router)

# Rodar localmente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
