from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True, index=True)
    cidade = Column(String)
    estado = Column(String, default="GO")
    certificada_iso14000 = Column(Boolean, default=False)

    registros_impacto = relationship(
        "RegistroImpacto", back_populates="empresa")


class RegistroImpacto(Base):
    __tablename__ = "registros_impacto"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    data_registro = Column(DateTime, default=datetime.utcnow)

    # Consumos
    consumo_agua_litros = Column(Float, default=0.0)
    consumo_energia_kwh = Column(Float, default=0.0)

    # Resíduos
    residuos_solidos_kg = Column(Float, default=0.0)
    residuos_perigosos_kg = Column(Float, default=0.0)

    # Ações tomadas
    acoes_mitigacao = Column(String, default="")

    empresa = relationship("Empresa", back_populates="registros_impacto")
