from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import Article
from app.schemas.schemas import ArticleCreate, ArticleOut
from typing import List

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", response_model=List[ArticleOut])
def liste_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()


@router.get("/{id}", response_model=ArticleOut)
def get_article(id: int, db: Session = Depends(get_db)):
    a = db.query(Article).filter(Article.id == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Article introuvable")
    return a


@router.post("/", response_model=ArticleOut, status_code=201)
def creer_article(data: ArticleCreate, db: Session = Depends(get_db)):
    a = Article(**data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@router.put("/{id}/stock", response_model=ArticleOut)
def maj_stock(id: int, quantite: int, db: Session = Depends(get_db)):
    a = db.query(Article).filter(Article.id == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Article introuvable")
    a.stock += quantite
    db.commit()
    db.refresh(a)
    return a
