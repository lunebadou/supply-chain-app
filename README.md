# Supply Chain - Module Achat

API FastAPI pour la gestion des achats : fournisseurs, articles, bons de commande et facturation.

## Stack
- Python 3.11 + FastAPI
- PostgreSQL
- Docker + Docker Compose
- Prometheus metrics exposées sur `/metrics`

## Lancer en local

```bash
# Copier le fichier d'env
cp .env.example .env

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'app
uvicorn app.main:app --reload --port 8001
```

## Lancer avec Docker

```bash
# Recette (port 8001) + Prod (port 8000)
docker-compose up -d --build
```

## Endpoints principaux

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | /health | Santé de l'app |
| GET/POST | /fournisseurs | Gestion fournisseurs |
| GET/POST | /articles | Gestion articles |
| POST | /commandes | Créer un bon de commande |
| PUT | /commandes/{id}/valider | Valider une commande |
| PUT | /commandes/{id}/reception | Réceptionner une commande |
| POST | /commandes/{id}/facturer | Générer une facture |
| GET | /metrics | Métriques Prometheus |
| GET | /docs | Swagger UI |

## Workflow Achat

```
Créer commande → Valider → Réceptionner → Facturer
```

## Environnements

- **Recette** : port `8001`
- **Prod** : port `8000`

test test
hhuhuujiujiiijij
njnjjnjjjjjjkjjkjkj,kk
k,kk,k,k,kj,kj