from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import BonCommande, LigneCommande, Facture, StatutCommande
from app.schemas.schemas import BonCommandeCreate, BonCommandeOut, FactureOut
from typing import List
import uuid

router = APIRouter(prefix="/commandes", tags=["Commandes"])


def generer_numero(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


@router.get("/", response_model=List[BonCommandeOut])
def liste_commandes(db: Session = Depends(get_db)):
    return db.query(BonCommande).all()


@router.get("/{id}", response_model=BonCommandeOut)
def get_commande(id: int, db: Session = Depends(get_db)):
    c = db.query(BonCommande).filter(BonCommande.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return c


@router.post("/", response_model=BonCommandeOut, status_code=201)
def creer_commande(data: BonCommandeCreate, db: Session = Depends(get_db)):
    montant_total = sum(l.quantite * l.prix_unitaire for l in data.lignes)

    commande = BonCommande(
        numero=generer_numero("BC"),
        fournisseur_id=data.fournisseur_id,
        montant_total=montant_total
    )
    db.add(commande)
    db.flush()

    for l in data.lignes:
        ligne = LigneCommande(
            commande_id=commande.id,
            article_id=l.article_id,
            quantite=l.quantite,
            prix_unitaire=l.prix_unitaire,
            montant=l.quantite * l.prix_unitaire
        )
        db.add(ligne)

    db.commit()
    db.refresh(commande)
    return commande


@router.put("/{id}/valider", response_model=BonCommandeOut)
def valider_commande(id: int, db: Session = Depends(get_db)):
    c = db.query(BonCommande).filter(BonCommande.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    c.statut = StatutCommande.VALIDEE
    db.commit()
    db.refresh(c)
    return c


@router.put("/{id}/reception", response_model=BonCommandeOut)
def reception_commande(id: int, db: Session = Depends(get_db)):
    c = db.query(BonCommande).filter(BonCommande.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    if c.statut != StatutCommande.VALIDEE:
        raise HTTPException(status_code=400, detail="La commande doit être validée avant réception")
    c.statut = StatutCommande.RECUE
    db.commit()
    db.refresh(c)
    return c


@router.post("/{id}/facturer", response_model=FactureOut)
def facturer_commande(id: int, db: Session = Depends(get_db)):
    c = db.query(BonCommande).filter(BonCommande.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    if c.statut != StatutCommande.RECUE:
        raise HTTPException(status_code=400, detail="La commande doit être reçue avant facturation")
    if c.facture:
        raise HTTPException(status_code=400, detail="Commande déjà facturée")

    facture = Facture(
        numero=generer_numero("FAC"),
        commande_id=c.id,
        montant=c.montant_total
    )
    db.add(facture)
    c.statut = StatutCommande.FACTUREE
    db.commit()
    db.refresh(facture)
    return facture


@router.put("/{id}/annuler", response_model=BonCommandeOut)
def annuler_commande(id: int, db: Session = Depends(get_db)):
    c = db.query(BonCommande).filter(BonCommande.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    if c.statut in [StatutCommande.FACTUREE, StatutCommande.PAYEE]:
        raise HTTPException(status_code=400, detail="Impossible d'annuler une commande facturée ou payée")
    c.statut = StatutCommande.ANNULEE
    db.commit()
    db.refresh(c)
    return c
