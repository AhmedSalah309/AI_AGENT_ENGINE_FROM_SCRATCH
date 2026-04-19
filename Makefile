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

# ==========================================
# 8-  CODE QUALITY
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
# 9- CLEANUP
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
	