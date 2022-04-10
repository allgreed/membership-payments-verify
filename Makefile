SOURCES := main.py plaintext_accounting_parser.py
TEST_SOURCES := test_plaintext_accounting_parser.py
INPUTS := $(SOURCES)

# Porcelain
# ###############
.PHONY: env-up env-down env-recreate container run build lint test watch

watch: ## watch for changes and run app
	ls $(INPUTS) | entr -c make --no-print-directory run

watch-test: ## watch for changes and run tests
	ls $(INPUTS) $(TEST_SOURCES) | entr -c make --no-print-directory test

run: setup ## run the app
	python main.py

build: setup ## create artifact
	@echo "Not implemented"; false

lint: setup ## run static analysis
	@echo "Not implemented"; false

test: setup $(SOURCES) $(TEST_SOURCES) ## run all tests
	pytest

container: build ## create container
	@echo "Not implemented"; false

# Plumbing
# ###############
.PHONY: setup gitclean gitclean-with-libs

setup:
gitclean:
	@# will remove everything in .gitignore expect for blocks starting with dep* or lib* comment

	diff --new-line-format="" --unchanged-line-format="" <(grep -v '^#' .gitignore | grep '\S' | sort) <(awk '/^# *(dep|lib)/,/^$/' testowy | head -n -1 | tail -n +2 | sort) | xargs rm -rf

gitclean-with-libs:
	diff --new-line-format="" --unchanged-line-format="" <(grep -v '^#' .gitignore | grep '\S' | sort) | xargs rm -rf

# Utilities
# ###############
.PHONY: help todo clean really_clean init
init: ## one time setup
	direnv allow .

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

clean: gitclean ## remove artifacts

really_clean: gitclean-with-libs ## remove EVERYTHING

help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help
