#!/bin/bash
set -e
echo "--- Syncing Environment ---"
uv sync --all-extras
echo "--- Compliance Check (No-NoQA) ---"
bash scripts/check_compliance.sh
echo "--- Linting (Ruff) ---"
uv run ruff check . --fix
echo "--- Typing (Mypy) ---"
uv run mypy . --strict
echo "--- Architectural Ratchet (Zero-Any) ---"
uv run pytest tests/test_architecture.py
echo "--- Unit Tests ---"
uv run pytest --cov=src --cov-report=term-missing
