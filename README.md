# 📊 DevOps Monitoring Dashboard (Mini-Project)

Bienvenue dans le projet **DevOps Monitor**, une application de surveillance système complète comprenant une **API FastAPI** et un **Dashboard interactif Streamlit**.

## 🎯 Objectifs
Ce projet permet de surveiller en temps réel des serveurs (CPU, Mémoire, Disque) via une interface moderne et de gérer un parc de serveurs supervisés. Il est conçu pour être facilement déployable en local ou sur le cloud (Azure).

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

## ⚙️ Prérequis

- **Docker** & **Docker Compose** (recommandé pour le lancement local)
- **Python 3.11+** (pour le développement local sans Docker)
- **Make** (pour utiliser les commandes automatisées du Makefile)
- **Azure CLI** (pour le déploiement sur Azure)

## 🚀 Installation & Lancement Local

La manière la plus simple d'exécuter le projet est d'utiliser **Docker** et le `Makefile`.

1. **Cloner le projet et se rendre dans le dossier** :
   ```bash
   cd devops-monitor
   ```

2. **Démarrer l'application avec Docker Compose** :
   ```bash
   make up
   ```
   *L'API sera disponible sur `http://localhost:8000` (Swagger sur `/docs`)*
   *Le Dashboard sera disponible sur `http://localhost:8501`*

3. **Arrêter l'application** :
   ```bash
   make down
   ```

*(Alternative) Lancement local sans Docker :*
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

## ☁️ Déploiement sur Azure

Le projet est préconfiguré pour être déployé sur **Azure Container Apps** (API) et **Azure Web Apps** (Dashboard).

Assurez-vous d'être connecté à Azure (`az login`) et d'avoir défini vos variables dans le Makefile, puis exécutez :

```bash
# Déployer l'API sur Azure Container Apps
make deploy-api

# Déployer le Dashboard sur Azure Web App
make deploy-dash
```

## 🧹 Nettoyage du dépôt

Pour nettoyer les fichiers temporaires locaux (cache, pycache) :
```bash
make clean
```
