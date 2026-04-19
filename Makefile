# ==========================================
# AI Agent Engine From Scratch
# ==========================================

# --- Variables ---
VENV        = .venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip
RUFF        = $(VENV)/bin/ruff
BLACK       = $(VENV)/bin/black
MYPY        = $(VENV)/bin/mypy
PYTEST      = $(VENV)/bin/pytest
DEV_PORT    = 8002
PROD_PORT   = 8001

.PHONY: help setup install run-dev run check-ollama check-env \
        test format lint type-check check clean \
        docker-up docker-down docker-build docker-rebuild docker-logs docker-logs-worker \
        monitor-up check-worker migrate-create migrate-up

# ==========================================
# HELP
# ==========================================
help: ## Show this help message
	@echo ""
	@echo "AI Agent Engine From Scratch - Makefile Commands"
	@echo ""
	@echo "Usage: make <command>"
	@echo ""
	@echo "SETUP & INSTALLATION:"
	@echo "  make setup          → Create venv + install dependencies"
	@echo "  make install        → Install dependencies only (if venv exists)"
	@echo ""
	@echo "RUNNING LOCALLY:"
	@echo "  make run-dev        → Run dev server (port $(DEV_PORT)) (Flask + Gunicorn)"
	@echo "  make run            → Run production server (Gunicorn)"
	@echo ""
	@echo "QUALITY & TESTING:"
	@echo "  make format         → Format code (Ruff)"
	@echo "  make lint           → Check linting errors (Ruff)"
	@echo "  make type-check     → Run static type checking (Mypy)"
	@echo "  make test           → Run all tests with coverage"
	@echo "  make check          → Full quality check (format + lint + test)"
	@echo ""
	@echo "CLEANUP:"
	@echo "  make clean          → Remove venv and caches"
	@echo ""
	@echo "DOCKER:"
	@echo "  make docker-up      → Start all services (Nginx, Web, Worker, Redis, Prometheus, Grafana)"
	@echo "  make docker-down    → Stop all services"
	@echo "  make docker-build   → Build Docker images"
	@echo "  make docker-rebuild → Rebuild images and restart"
	@echo "  make docker-logs    → View web app logs"
	@echo "  make docker-logs-worker → View worker logs"
	@echo ""
	@echo "MONITORING:"
	@echo "  make monitor-up     → Start Prometheus + Grafana"
	@echo ""
	@echo "DATABASE:"
	@echo "  make migrate-create → Create new Alembic migration"
	@echo "  make migrate-up     → Apply database migrations"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ==========================================
# SETUP & INSTALLATION
# ==========================================
setup: ## Create virtual environment and install all dependencies
	@echo "Creating virtual environment in $(VENV)..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "Setup complete! Activate with: source $(VENV)/bin/activate"
	@echo "   Then run: make run-dev"

install: ## Install/update dependencies in existing venv
	$(PIP) install -r requirements.txt

# ==========================================
# PRE-FLIGHT CHECKS
# ==========================================
check-ollama: ## Verify Ollama is running and model is available
	@echo "Checking Ollama..."
	@curl -sf http://localhost:11434 > /dev/null 2>&1 \
		&& echo "Ollama is running" \
		|| (echo "Ollama is NOT running. Start it with: ollama serve" && exit 1)
	@echo "Checking gemma:2b model..."
	@ollama list 2>/dev/null | grep -q "gemma:2b" \
		&& echo "gemma:2b model is available" \
		|| (echo "gemma:2b not found. Pull it with: ollama pull gemma:2b" && exit 1)

check-env: ## Verify .env file exists with required settings
	@echo "Checking .env file..."
	@test -f .env \
		&& echo ".env file found" \
		|| (echo ".env file missing. Copy from: cp .env.example .env" && exit 1)
	@grep -q "OLLAMA_BASE_URL" .env \
		&& echo "OLLAMA_BASE_URL is set" \
		|| (echo "OLLAMA_BASE_URL missing in .env" && exit 1)

check-venv: ## Verify virtual environment exists
	@test -d $(VENV) \
		&& echo "Virtual environment found" \
		|| (echo "No venv found. Run: make setup" && exit 1)

preflight: check-env check-venv check-ollama ## Run all pre-flight checks
	@echo ""
	@echo "All checks passed! Ready to run."

# ==========================================
# LOCAL DEVELOPMENT
# ==========================================
run-dev: check-env check-ollama ## Start Flask dev server with hot-reload (port 8002)
	@echo "Starting Flask dev server on http://localhost:$(DEV_PORT) ..."
	PYTHONPATH=src FLASK_APP=src.agent_engine.api.main:app FLASK_DEBUG=1 \
		python3 -m flask run --port=$(DEV_PORT)

run: check-venv ## Start Flask via venv (port 8001)
	@echo "Starting Flask server on http://0.0.0.0:$(PROD_PORT) ..."
	FLASK_APP=src.agent_engine.api.main:app FLASK_DEBUG=1 \
		$(PYTHON) -m flask run --host=0.0.0.0 --port=$(PROD_PORT)

# ==========================================
# DATABASE MIGRATIONS
# ==========================================
migrate-create: ## Auto-generate a new Alembic migration
	python3 -m alembic revision --autogenerate -m "auto-migration"

migrate-up: ## Apply all pending migrations
	python3 -m alembic upgrade head

# ==========================================
# DOCKER (Production / Staging)
# ==========================================
docker-build: ## Build Docker images
	docker compose build

docker-up: ## Start all containers (build if needed)
	docker compose up -d --build
	@echo ""
	@echo "✅ Containers are up!"
	@echo "   App:        http://localhost:8001"
	@echo "   Prometheus: http://localhost:9091"
	@echo "   Grafana:    http://localhost:3001"

docker-down: ## Stop and remove all containers
	docker compose down

docker-rebuild: ## Full rebuild with clean-up
	docker compose down --remove-orphans
	docker compose build --no-cache
	docker compose up -d
	@echo "✅ Full rebuild complete!"

docker-logs: ## View live logs from web service
	docker compose logs -f web

docker-logs-worker: ## View live logs from the Celery worker
	docker compose logs -f worker

# ==========================================
# MONITORING
# ==========================================
monitor-up: ## Start Prometheus, Grafana, and Nginx
	docker compose up -d prometheus grafana nginx

check-worker: ## Check Celery worker status
	docker compose logs -f worker

# ==========================================
# CODE QUALITY
# ==========================================
format: ## Auto-format code using ruff
	@echo "Running ruff formatter..."
	$(RUFF) format .
	$(RUFF) check . --fix

lint: ## Check for linting errors (no auto-fix)
	@echo "Running ruff linter..."
	$(RUFF) check .
	$(RUFF) format --check .

type-check: ## Run static type checking with mypy
	@echo "Running mypy type checker..."
	$(MYPY) src/

test: ## Run all tests with coverage report
	$(PYTEST) tests/ -s --cov=src --cov-report=term-missing

check: format type-check test ## Full quality check: Format → Type Check → Test
	@echo ""
	@echo "All checks passed! Ready for commit/push."

# ==========================================
# CLEANUP
# ==========================================
clean: ## Remove venv, caches, and temporary files
	@echo "Cleaning up..."
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete."
