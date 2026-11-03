from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Configuração de CORS para permitir que o Frontend (React/HTML) consuma a API
origins = [
    "http://localhost",
    "http://localhost:5173",  # Porta padrão do Vite
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desenvolvimento, permitindo de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(empresas.router)
app.include_router(registros.router)


@app.get("/")
def read_root():
    return {"mensagem": "Bem-vindo à API do SIGA-GO (Gestão Ambiental)"}
