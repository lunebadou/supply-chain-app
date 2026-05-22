from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from app.database.db import engine
from app.models.models import Base
from app.routers import fournisseurs, articles, commandes, web
import os

# Création des tables
Base.metadata.create_all(bind=engine)

ENV = os.getenv("ENV", "recette")

app = FastAPI(
    title="Supply Chain - Module Achat",
    description="API de gestion des achats (Bons de commande, Fournisseurs, Articles, Factures)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Fichiers statiques (CSS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Métriques Prometheus
Instrumentator().instrument(app).expose(app)

# Routers
app.include_router(web.router)
app.include_router(fournisseurs.router)
app.include_router(articles.router)
app.include_router(commandes.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "app": "Supply Chain - Module Achat",
        "env": ENV,
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "env": ENV}