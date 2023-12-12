.PHONY: help install develop test

test: ## Run all tests
	@echo "+ $@"
	@python3 -m pytest --cov

develop: ## Install package in editable mode with pip
	@echo "+ $@"
	@python3 -m pip install -e .

install: ## Install packege with pip
	@echo "+ $@"
	@python3 -m pip install .

help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
