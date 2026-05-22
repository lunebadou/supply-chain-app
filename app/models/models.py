from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.db import Base


class StatutCommande(str, enum.Enum):
    EN_ATTENTE = "en_attente"
    VALIDEE = "validee"
    RECUE = "recue"
    FACTUREE = "facturee"
    PAYEE = "payee"
    ANNULEE = "annulee"


class Fournisseur(Base):
    __tablename__ = "fournisseurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telephone = Column(String)
    adresse = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    commandes = relationship("BonCommande", back_populates="fournisseur")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, nullable=False)
    designation = Column(String, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lignes = relationship("LigneCommande", back_populates="article")


class BonCommande(Base):
    __tablename__ = "bons_commande"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, nullable=False)
    fournisseur_id = Column(Integer, ForeignKey("fournisseurs.id"))
    statut = Column(Enum(StatutCommande), default=StatutCommande.EN_ATTENTE)
    montant_total = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    fournisseur = relationship("Fournisseur", back_populates="commandes")
    lignes = relationship("LigneCommande", back_populates="commande")
    facture = relationship("Facture", back_populates="commande", uselist=False)


class LigneCommande(Base):
    __tablename__ = "lignes_commande"

    id = Column(Integer, primary_key=True, index=True)
    commande_id = Column(Integer, ForeignKey("bons_commande.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    montant = Column(Float, nullable=False)

    commande = relationship("BonCommande", back_populates="lignes")
    article = relationship("Article", back_populates="lignes")


class Facture(Base):
    __tablename__ = "factures"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, nullable=False)
    commande_id = Column(Integer, ForeignKey("bons_commande.id"))
    montant = Column(Float, nullable=False)
    statut = Column(String, default="en_attente")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    commande = relationship("BonCommande", back_populates="facture")
