# 📊 DevOps Monitoring Dashboard (Mini-Project)

Bienvenue dans le projet **DevOps Monitor**, une application de surveillance système complète comprenant une **API FastAPI** et un **Dashboard interactif Streamlit**.

## 🎯 Objectifs
Ce projet permet de surveiller en temps réel des serveurs (CPU, Mémoire, Disque) via une interface moderne et de gérer un parc de serveurs supervisés. Il est entièrement conteneurisé avec **Docker** pour un déploiement facile et reproductible sur n'importe quel environnement.

## 🗂️ Structure du Projet

```text
devops-monitor/
├── api/                 # Backend FastAPI (métriques, serveurs, websockets)
├── dashboard/           # Frontend Streamlit (visualisation en temps réel)
├── tests/               # Tests automatisés (Pytest)
├── docker-compose.yml   # Configuration multi-conteneurs Docker
├── Makefile             # Commandes d'automatisation (Make)
└── requirements.txt     # Dépendances Python
```

## ⚡ Démarrage Rapide (Quick Start)

Vous venez de cloner le projet ? Voici comment le lancer en **1 minute chrono**.

**Prérequis** : Vous devez avoir [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et lancé sur votre ordinateur.

1. Ouvrez un terminal dans le dossier du projet (`devops-monitor`).
2. Tapez la commande suivante :
   ```bash
   docker compose up --build -d
   ```
3. Et c'est tout ! 🎉 Accédez maintenant à :
   - **Dashboard** : [http://localhost:8501](http://localhost:8501)
   - **API Backend** : [http://localhost:8000/docs](http://localhost:8000/docs)

Pour tout éteindre quand vous avez terminé, tapez `docker compose down`.

---

## ⚙️ Prérequis Détaillés

- **Docker** & **Docker Compose** (Obligatoire pour le lancement simple)
- **Python 3.11+** (Optionnel, uniquement pour le développement local sans Docker)
- **Make** (Optionnel, pour utiliser les raccourcis du Makefile)

## 🚀 Utilisation Avancée (Makefile)

Si vous avez l'outil `make` installé sur votre ordinateur (Linux/Mac), vous pouvez utiliser les raccourcis configurés :

- `make up` : Lance le projet (équivalent de `docker compose up --build -d`)
- `make down` : Arrête le projet et supprime les conteneurs
- `make logs` : Affiche les logs en temps réel
- `make clean` : Nettoie les fichiers temporaires locaux

*(Alternative) Lancement local de développement sans Docker :*
```bash
make install
make dev
```

## 🧪 Tests & Qualité

Ce projet inclut des tests unitaires configurés avec **Pytest** et une vérification de la couverture de code.

Pour exécuter les tests :
```bash
make test
```

Pour vérifier le formatage du code (Linting) :
```bash
make lint
```

## 🐳 Déploiement Production (Docker)

Le projet est préconfiguré pour être déployé via Docker Compose, que ce soit en local ou sur un serveur (VPS).

Assurez-vous d'avoir Docker installé et lancez simplement :

```bash
docker compose up --build -d
```

L'API et le Dashboard vont communiquer via le réseau interne de Docker. C'est la méthode recommandée pour faire tourner le projet !

## 🧹 Nettoyage du dépôt

Pour nettoyer les fichiers temporaires locaux (cache, pycache) :
```bash
make clean
```
