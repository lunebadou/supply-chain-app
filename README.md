### 2. README pour le dépôt `supply-chain-app`

```markdown
# Supply Chain - Module Achat

API FastAPI pour la gestion des achats : fournisseurs, articles, bons de commande et facturation.

## Stack

- Python 3.11 + FastAPI
- PostgreSQL
- Docker + Docker Compose

## Lancer en local

```bash
# Copier le fichier d'env
cp .env.example .env

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'app
uvicorn app.main:app --reload --port 8001
Lancer avec DockerBash# Recette (port 8001) + Prod (port 8000)
docker-compose up -d --build
Endpoints principauxMéthodeRouteDescriptionGET/healthSanté de l'appGET/POST/fournisseursGestion fournisseursGET/POST/articlesGestion articlesPOST/commandesCréer un bon de commandePUT/commandes/{id}/validerValider une commandePUT/commandes/{id}/receptionRéceptionner une commandePOST/commandes/{id}/facturerGénérer une factureGET/docsSwagger UIWorkflow AchatCréer commande → Valider → Réceptionner → Facturer
EnvironnementsRecette : port 8001Prod : port 8000