.DEFAULT_GOAL := help
PYTHON ?= python3
PYTHONPATH := src

.PHONY: help build verify serve new-post clean-build

help:
	@echo "Targets:"
	@echo "  make build                     Build public site into build/_site/"
	@echo "  make verify                    Build public + fixture previews and run all tests"
	@echo "  make serve                     Preview build/_site/ at http://localhost:8000"
	@echo "  make new-post SLUG=...         Scaffold a new Feed Markdown post"
	@echo "  make clean-build               Remove ephemeral build/ and cache directories"

build:
	@PYTHONPATH=$(PYTHONPATH) "$(PYTHON)" -m web_engine.app.cli --out-dir build/_site

verify:
	@PYTHONPATH=$(PYTHONPATH) "$(PYTHON)" -m web_engine.app.cli --out-dir build/_site --verify-fixtures
	@PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) "$(PYTHON)" -m unittest discover -s test -p "test_*.py" -v

serve: build
	@echo "Serving http://localhost:8000 (Ctrl+C to stop)"
	@"$(PYTHON)" -m http.server 8000 --directory build/_site

new-post:
	@test -n "$(SLUG)" || (echo "Usage: make new-post SLUG=my-topic [KIND=note]" && exit 1)
	@PYTHONPATH=$(PYTHONPATH) "$(PYTHON)" -m web_engine.app.cli --new-post "$(SLUG)" --kind "$(or $(KIND),note)"

clean-build:
	@rm -rf build .pytest_cache .mypy_cache .ruff_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +
