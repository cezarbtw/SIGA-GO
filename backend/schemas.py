from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ==========================
# Schemas para Empresa
# ==========================


class EmpresaBase(BaseModel):
    nome: str = Field(..., description="Nome da organização")
    cnpj: str = Field(..., description="CNPJ da empresa")
    cidade: str = Field(..., description="Cidade da empresa em Goiás")
    estado: str = Field("GO", description="Estado (padrão GO)")
    certificada_iso14000: bool = False


class EmpresaCreate(EmpresaBase):
    pass


class Empresa(EmpresaBase):
    id: int

    class Config:
        from_attributes = True

# ==========================
# Schemas para RegistroImpacto
# ==========================


class RegistroImpactoBase(BaseModel):
    consumo_agua_litros: float = Field(0.0, ge=0)
    consumo_energia_kwh: float = Field(0.0, ge=0)
    residuos_solidos_kg: float = Field(0.0, ge=0)
    residuos_perigosos_kg: float = Field(0.0, ge=0)
    acoes_mitigacao: Optional[str] = None


class RegistroImpactoCreate(RegistroImpactoBase):
    empresa_id: int


class RegistroImpacto(RegistroImpactoBase):
    id: int
    empresa_id: int
    data_registro: datetime

    class Config:
        from_attributes = True
