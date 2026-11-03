from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
from database import SessionLocal

router = APIRouter(
    prefix="/registros",
    tags=["registros"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.RegistroImpacto)
def create_registro(registro: schemas.RegistroImpactoCreate, db: Session = Depends(get_db)):
    db_empresa = crud.get_empresa(db, empresa_id=registro.empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return crud.create_registro_impacto(db=db, registro=registro)


@router.get("/", response_model=List[schemas.RegistroImpacto])
def read_registros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    registros = crud.get_registros(db, skip=skip, limit=limit)
    return registros


@router.get("/empresa/{empresa_id}", response_model=List[schemas.RegistroImpacto])
def read_registros_por_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return crud.get_registros_by_empresa(db, empresa_id=empresa_id)
