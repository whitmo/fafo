.PHONY: install-deps lint help

install-deps: ## Install gum dependency
	@if command -v brew &>/dev/null; then 
		brew install gum; 
	else 
		echo "Homebrew not found. See https://github.com/charmbracelet/gum#installation"; 
		exit 1; 
	fi

lint: ## Run shellcheck on all scripts
	shellcheck bin/showoff bin/_shell-init.sh

help: ## Display this help message
	@echo "Usage: make <command>"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s
", $$1, $$2}'
