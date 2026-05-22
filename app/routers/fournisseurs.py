from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import Fournisseur
from app.schemas.schemas import FournisseurCreate, FournisseurOut
from typing import List

router = APIRouter(prefix="/fournisseurs", tags=["Fournisseurs"])


@router.get("/", response_model=List[FournisseurOut])
def liste_fournisseurs(db: Session = Depends(get_db)):
    return db.query(Fournisseur).all()


@router.get("/{id}", response_model=FournisseurOut)
def get_fournisseur(id: int, db: Session = Depends(get_db)):
    f = db.query(Fournisseur).filter(Fournisseur.id == id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Fournisseur introuvable")
    return f


@router.post("/", response_model=FournisseurOut, status_code=201)
def creer_fournisseur(data: FournisseurCreate, db: Session = Depends(get_db)):
    f = Fournisseur(**data.model_dump())
    db.add(f)
    db.commit()
    db.refresh(f)
    return f


@router.delete("/{id}", status_code=204)
def supprimer_fournisseur(id: int, db: Session = Depends(get_db)):
    f = db.query(Fournisseur).filter(Fournisseur.id == id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Fournisseur introuvable")
    db.delete(f)
    db.commit()
