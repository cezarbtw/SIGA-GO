from sqlalchemy.orm import Session
import models
import schemas

# Empresas


def get_empresa(db: Session, empresa_id: int):
    return db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()


def get_empresa_by_cnpj(db: Session, cnpj: str):
    return db.query(models.Empresa).filter(models.Empresa.cnpj == cnpj).first()


def get_empresas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Empresa).offset(skip).limit(limit).all()


def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

# Registros de Impacto


def get_registros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RegistroImpacto).offset(skip).limit(limit).all()


def get_registros_by_empresa(db: Session, empresa_id: int):
    return db.query(models.RegistroImpacto).filter(models.RegistroImpacto.empresa_id == empresa_id).all()


def create_registro_impacto(db: Session, registro: schemas.RegistroImpactoCreate):
    db_registro = models.RegistroImpacto(**registro.model_dump())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro
