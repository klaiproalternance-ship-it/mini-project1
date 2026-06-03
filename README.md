# DevOps Monitoring Dashboard MVP

Ce projet est un tableau de bord de surveillance DevOps opérationnel comprenant un backend FastAPI et un frontend interactif Streamlit.

## Structure du Projet

```
devops-monitor/
├── api/
│   ├── __init__.py
│   ├── main.py          # Point d'entrée de FastAPI (lifespan, routes)
│   ├── models.py        # Modèles Pydantic + Dataclass Server
│   ├── auth.py          # Dépendance pour la clé API
│   ├── metrics.py       # Helper psutil pour collecter les métriques système
│   └── poller.py        # Logique de vérification de santé en arrière-plan
├── dashboard/
│   └── app.py           # Frontend Streamlit
├── tests/
│   ├── test_metrics.py
│   └── test_routes.py
├── requirements.txt
└── README.md
```

## Installation

1. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Démarrez l'API FastAPI (sur le port 8000 par défaut) :
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

2. Dans un autre terminal, lancez le Dashboard Streamlit :
   ```bash
   streamlit run dashboard/app.py
   ```

3. Ouvrez votre navigateur et accédez à l'adresse suivante :
   `http://localhost:8501`

## Exécution des Tests

Pour exécuter la suite de tests unitaires et d'intégration :
```bash
pytest tests/ -v
```
