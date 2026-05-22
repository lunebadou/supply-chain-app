import os
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uuid

from app.database.db import get_db
from app.models.models import Fournisseur, Article, BonCommande, LigneCommande, StatutCommande

router = APIRouter(prefix="/ui", tags=["UI"])

templates = Jinja2Templates(directory="app/templates")

ENV = os.getenv("ENV", "recette")


def _ctx() -> dict:
    return {"env": ENV}


def _generer_numero(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


# ────── Accueil ──────
@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    counts = {
        "fournisseurs": db.query(Fournisseur).count(),
        "articles": db.query(Article).count(),
        "commandes": db.query(BonCommande).count(),
    }
    return templates.TemplateResponse(
        request, "home.html", {**_ctx(), "counts": counts}
    )


# ────── Fournisseurs ──────
@router.get("/fournisseurs")
def fournisseurs_page(request: Request, db: Session = Depends(get_db)):
    fournisseurs = db.query(Fournisseur).order_by(Fournisseur.id.desc()).all()
    return templates.TemplateResponse(
        request, "fournisseurs.html", {**_ctx(), "fournisseurs": fournisseurs}
    )


@router.post("/fournisseurs")
def fournisseurs_create(
    request: Request,
    nom: str = Form(...),
    email: str = Form(...),
    telephone: str = Form(""),
    adresse: str = Form(""),
    db: Session = Depends(get_db),
):
    fournisseur = Fournisseur(
        nom=nom,
        email=email,
        telephone=telephone or None,
        adresse=adresse or None,
    )
    db.add(fournisseur)
    db.commit()
    fournisseurs = db.query(Fournisseur).order_by(Fournisseur.id.desc()).all()
    return templates.TemplateResponse(
        request, "_fournisseurs_table.html", {**_ctx(), "fournisseurs": fournisseurs}
    )


# ────── Articles ──────
@router.get("/articles")
def articles_page(request: Request, db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.id.desc()).all()
    return templates.TemplateResponse(
        request, "articles.html", {**_ctx(), "articles": articles}
    )


@router.post("/articles")
def articles_create(
    request: Request,
    reference: str = Form(...),
    designation: str = Form(...),
    prix_unitaire: float = Form(...),
    stock: int = Form(0),
    db: Session = Depends(get_db),
):
    article = Article(
        reference=reference,
        designation=designation,
        prix_unitaire=prix_unitaire,
        stock=stock,
    )
    db.add(article)
    db.commit()
    articles = db.query(Article).order_by(Article.id.desc()).all()
    return templates.TemplateResponse(
        request, "_articles_table.html", {**_ctx(), "articles": articles}
    )


# ────── Commandes ──────
@router.get("/commandes")
def commandes_page(request: Request, db: Session = Depends(get_db)):
    commandes = db.query(BonCommande).order_by(BonCommande.id.desc()).all()
    fournisseurs = db.query(Fournisseur).order_by(Fournisseur.nom).all()
    articles = db.query(Article).order_by(Article.designation).all()
    return templates.TemplateResponse(
        request,
        "commandes.html",
        {
            **_ctx(),
            "commandes": commandes,
            "fournisseurs": fournisseurs,
            "articles": articles,
        },
    )


@router.post("/commandes")
def commandes_create(
    request: Request,
    fournisseur_id: int = Form(...),
    article_id: int = Form(...),
    quantite: int = Form(...),
    prix_unitaire: float = Form(...),
    db: Session = Depends(get_db),
):
    montant_total = quantite * prix_unitaire

    commande = BonCommande(
        numero=_generer_numero("BC"),
        fournisseur_id=fournisseur_id,
        montant_total=montant_total,
    )
    db.add(commande)
    db.flush()

    ligne = LigneCommande(
        commande_id=commande.id,
        article_id=article_id,
        quantite=quantite,
        prix_unitaire=prix_unitaire,
        montant=montant_total,
    )
    db.add(ligne)
    db.commit()

    commandes = db.query(BonCommande).order_by(BonCommande.id.desc()).all()
    return templates.TemplateResponse(
        request, "_commandes_table.html", {**_ctx(), "commandes": commandes}
    )