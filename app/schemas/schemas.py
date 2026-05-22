from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.models import StatutCommande


# ── Fournisseur ──────────────────────────────────────
class FournisseurCreate(BaseModel):
    nom: str
    email: str
    telephone: Optional[str] = None
    adresse: Optional[str] = None

class FournisseurOut(FournisseurCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ── Article ──────────────────────────────────────────
class ArticleCreate(BaseModel):
    reference: str
    designation: str
    prix_unitaire: float
    stock: int = 0

class ArticleOut(ArticleCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ── Ligne Commande ───────────────────────────────────
class LigneCommandeCreate(BaseModel):
    article_id: int
    quantite: int
    prix_unitaire: float

class LigneCommandeOut(LigneCommandeCreate):
    id: int
    montant: float
    class Config:
        from_attributes = True


# ── Bon de Commande ──────────────────────────────────
class BonCommandeCreate(BaseModel):
    fournisseur_id: int
    lignes: List[LigneCommandeCreate]

class BonCommandeOut(BaseModel):
    id: int
    numero: str
    fournisseur_id: int
    statut: StatutCommande
    montant_total: float
    created_at: datetime
    lignes: List[LigneCommandeOut] = []
    class Config:
        from_attributes = True


# ── Facture ──────────────────────────────────────────
class FactureOut(BaseModel):
    id: int
    numero: str
    commande_id: int
    montant: float
    statut: str
    created_at: datetime
    class Config:
        from_attributes = True
