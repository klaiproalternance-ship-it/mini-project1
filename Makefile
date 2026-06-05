.PHONY: install up down logs test lint dev clean deploy-api deploy-dash push-github

# Variables pour le déploiement Azure
AZURE_RG ?= devops-monitor-rg
AZURE_LOCATION ?= westeurope
API_APP_NAME ?= devops-api-app
DASH_APP_NAME ?= devops-dash-app
GITHUB_REPO ?= https://github.com/klaiproalternance-ship-it/mini-project1.git

install:
	pip install -r requirements.txt

up:
	docker compose up --build -d

down:
	docker compose down -v

logs:
	docker compose logs -f

test:
	python -m pytest tests/ -v --cov=api --cov-fail-under=70

lint:
	flake8 api/ dashboard/ tests/ || echo "Linting errors found, check output."

dev:
	@echo "Pour lancer localement sans Docker :"
	@echo "Terminal 1: uvicorn api.main:app --reload --port 8000"
	@echo "Terminal 2: streamlit run dashboard/app.py"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .coverage
	@echo "Nettoyage terminé."

deploy-api:
	@echo "Déploiement de l'API sur Azure Container Apps..."
	az containerapp up \
		--name $(API_APP_NAME) \
		--resource-group $(AZURE_RG) \
		--location $(AZURE_LOCATION) \
		--source ./api \
		--ingress external \
		--target-port 8000 \
		--env-vars API_KEY=super-secret-ops-key

deploy-dash:
	@echo "Déploiement du Dashboard sur Azure Web App..."
	az webapp up \
		--name $(DASH_APP_NAME) \
		--resource-group $(AZURE_RG) \
		--location $(AZURE_LOCATION) \
		--os-type Linux \
		--runtime "PYTHON:3.11" \
		--startup-file "python -m streamlit run dashboard/app.py --server.port 8000 --server.address 0.0.0.0"

push-github:
	@echo "Initialisation et push vers GitHub..."
	git init || true
	git branch -M main || true
	git add .
	git commit -m "feat: initialisation du mini-projet DevOps Monitor" || echo "Rien à commiter"
	git remote remove origin 2>/dev/null || true
	git remote add origin $(GITHUB_REPO)
	git push -u origin main --force
