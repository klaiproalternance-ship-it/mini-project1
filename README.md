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
