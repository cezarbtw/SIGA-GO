import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import models
from database import engine
from routers import empresas, registros

# Criação das tabelas do banco de dados (SQLite)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIGA-GO API",
    description="Sistema de Informação de Gestão Ambiental - Goiás (ISO 14000)",
    version="1.0.0"
)

# Configuração de CORS permissiva para permitir requisições de file:/// e navegadores locais
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos roteadores da API
app.include_router(empresas.router)
app.include_router(registros.router)

# Rota de health check da API
@app.get("/api/health")
def api_health():
    return {"status": "online", "mensagem": "SIGA-GO API operacional"}

# Monta o frontend diretamente na raiz da aplicação (SPA)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
