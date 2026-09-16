PYTHON ?= python3

VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
VENV_STAMP := $(VENV)/.installed

.DEFAULT_GOAL := check

.PHONY: help venv install check lint validate readme readme-check clean

help: ## Show this help
	@grep -hE '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*## /\t/' | expand -t 16

venv: $(VENV_STAMP) ## Create the virtualenv and install the development dependencies
install: $(VENV_STAMP) ## Alias for venv

check: lint validate readme-check ## Run all checks

lint: $(VENV_STAMP) ## Lint the YAML files
	$(VENV_PYTHON) -m yamllint --strict .

validate: $(VENV_STAMP) ## Validate the blueprints
	$(VENV_PYTHON) scripts/blueprints.py validate

readme: $(VENV_STAMP) ## Regenerate the blueprint list in README.md
	$(VENV_PYTHON) scripts/blueprints.py readme

readme-check: $(VENV_STAMP) ## Fail if the blueprint list in README.md is out of date
	$(VENV_PYTHON) scripts/blueprints.py readme --check

clean: ## Remove the virtualenv
	rm -rf $(VENV)

$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)

$(VENV_STAMP): requirements-dev.txt | $(VENV_PYTHON)
	$(VENV_PYTHON) -m pip install --quiet --disable-pip-version-check -r requirements-dev.txt
	@touch $@
