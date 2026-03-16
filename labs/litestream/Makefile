.PHONY: all install-deps run-demo demo clean help

all: demo

## Environment Setup
install-deps: ## Install Litestream and gum dependencies on macOS
	@echo "Installing dependencies for macOS..."
	@if command -v brew &> /dev/null; then 
		brew install litestream gum; 
	else 
		echo "Homebrew not found. Please install Homebrew (https://brew.sh/) first."; 
		exit 1; 
	fi

## Demo Execution
demo: ## Run interactive demo with showoff
	../showoff/bin/showoff ./steps ./workspace

run-demo: ## Run the original non-interactive demo script
	./sqlite-litestream-recovery-demo.sh

## Cleanup
clean: ## Clean up demo artifacts
	@echo "Cleaning up demo environment..."
	rm -rf workspace labs/litestream_demo_env

## Help
help: ## Display this help message
	@echo "Usage: make <command>"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
