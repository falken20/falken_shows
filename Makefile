# ============================================================
# Live Memories – Makefile
# ============================================================
.DEFAULT_GOAL := help
.PHONY: help install dev test test-backend test-frontend test-e2e \
        lint format typecheck migrate seed build docker-up docker-down clean

BACKEND_DIR  := backend
FRONTEND_DIR := frontend
PYTHON       := python3
UV           := uv

# ── Help ──────────────────────────────────────────────────────
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Install ───────────────────────────────────────────────────
install: install-backend install-frontend ## Install all dependencies

install-backend: ## Install Python dependencies
	cd $(BACKEND_DIR) && $(UV) sync --all-extras

install-frontend: ## Install Node dependencies
	cd $(FRONTEND_DIR) && npm ci

# ── Development servers ───────────────────────────────────────
dev: ## Start backend + frontend concurrently (requires tmux or run in separate terminals)
	$(MAKE) -j2 dev-backend dev-frontend

dev-backend: ## Start backend dev server
	cd $(BACKEND_DIR) && $(UV) run uvicorn app.main:app --reload \
	  --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend dev server
	cd $(FRONTEND_DIR) && npm run dev

# ── Tests ─────────────────────────────────────────────────────
test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests with coverage
	cd $(BACKEND_DIR) && $(UV) run pytest --cov=app --cov-report=term-missing \
	  --cov-report=html:htmlcov --cov-fail-under=80 -v

test-frontend: ## Run frontend unit/integration tests
	cd $(FRONTEND_DIR) && npm run test:run

test-e2e: ## Run Playwright end-to-end tests
	cd $(FRONTEND_DIR) && npm run test:e2e

# ── Lint ──────────────────────────────────────────────────────
lint: lint-backend lint-frontend ## Run all linters

lint-backend: ## Run Ruff linter on backend
	cd $(BACKEND_DIR) && $(UV) run ruff check app tests

lint-frontend: ## Run ESLint on frontend
	cd $(FRONTEND_DIR) && npm run lint

# ── Format ────────────────────────────────────────────────────
format: format-backend format-frontend ## Format all code

format-backend: ## Format Python code with Ruff
	cd $(BACKEND_DIR) && $(UV) run ruff format app tests && \
	  $(UV) run ruff check --fix app tests

format-frontend: ## Format frontend code with Prettier
	cd $(FRONTEND_DIR) && npm run format

# ── Type checking ─────────────────────────────────────────────
typecheck: typecheck-backend typecheck-frontend ## Run all type checks

typecheck-backend: ## Run Mypy on backend
	cd $(BACKEND_DIR) && $(UV) run mypy app

typecheck-frontend: ## Run TypeScript type check on frontend
	cd $(FRONTEND_DIR) && npm run typecheck

# ── Database migrations ───────────────────────────────────────
migrate: ## Apply all pending Alembic migrations
	cd $(BACKEND_DIR) && $(UV) run alembic upgrade head

migrate-create: ## Create a new Alembic migration (usage: make migrate-create MSG="description")
	cd $(BACKEND_DIR) && $(UV) run alembic revision --autogenerate -m "$(MSG)"

migrate-downgrade: ## Downgrade one migration step
	cd $(BACKEND_DIR) && $(UV) run alembic downgrade -1

migrate-history: ## Show migration history
	cd $(BACKEND_DIR) && $(UV) run alembic history --verbose

# ── Seed ──────────────────────────────────────────────────────
seed: ## Load demo data into the database
	cd $(BACKEND_DIR) && $(UV) run python -m scripts.seed

# ── Build ─────────────────────────────────────────────────────
build: build-frontend build-backend ## Build all artefacts

build-frontend: ## Build frontend production bundle
	cd $(FRONTEND_DIR) && npm run build

build-backend: ## Build backend Docker image
	docker build -t live-memories-backend:latest $(BACKEND_DIR)

# ── Docker ────────────────────────────────────────────────────
docker-up: ## Start all services with Docker Compose (SQLite profile)
	docker compose up --build -d

docker-up-pg: ## Start all services with Docker Compose + PostgreSQL
	docker compose --profile postgres up --build -d

docker-down: ## Stop all Docker Compose services
	docker compose down

docker-logs: ## Tail logs from Docker Compose
	docker compose logs -f

# ── Clean ─────────────────────────────────────────────────────
clean: ## Remove build artefacts, caches and temporary files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf $(FRONTEND_DIR)/dist $(FRONTEND_DIR)/coverage $(FRONTEND_DIR)/playwright-report 2>/dev/null || true
	@echo "Clean done."

# ── Pre-commit ────────────────────────────────────────────────
pre-commit-install: ## Install pre-commit hooks
	pre-commit install --hook-type pre-commit --hook-type commit-msg

pre-commit-run: ## Run pre-commit on all files
	pre-commit run --all-files
