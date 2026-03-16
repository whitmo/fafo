.PHONY: all install-deps run-demo clean help

VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

all: run-demo

## Environment Setup
install-deps: $(VENV_DIR) ## Initialize venv and install Python dependencies
	@echo "Installing Python dependencies..."
	$(PIP) install -r requirements.txt

$(VENV_DIR):
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip

## Demo Execution
run-demo: $(VENV_DIR) ## Run the Chroma agent integration demo
	@echo "Running the Chroma agent integration demo..."
	$(PYTHON) src/main_demo.py

## Cleanup
clean: ## Clean up virtual environment, ChromaDB data, and other demo artifacts
	@echo "Cleaning up demo environment..."
	rm -rf $(VENV_DIR)
	rm -rf .chroma_db # Default directory for persistent ChromaDB
	rm -rf data/*.pdf # Remove any downloaded PDFs
	rm -rf wal # Remove Litestream WAL directory if created

help: ## Display this help message
	@echo "Usage: make <command>"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s
", $$1, $$2}'