GIT_CURRENT_BRANCH := ${shell git symbolic-ref --short HEAD}

.PHONY: help clean test clean-build isort run

.DEFAULT: help

help:
	@echo "make clean:"
	@echo "       Removes all pyc, pyo and __pycache__"
	@echo ""
	@echo "make clean-build:"
	@echo "       Clear all build directories"
	@echo ""
	@echo "make setup_dev"
	@echo "       Install dev dependencies and flake8 webhook"
	@echo "       Needs virtualenv activated and git initalized"
	@echo ""
	@echo "make clone-dotenv"
	@echo "       Creates .env file base on .env-example"
	@echo "       Used by setup_dev command"
	@echo ""
	@echo "make setup"
	@echo "       Install prod dependencies"
	@echo "       Needs virtualenv activated and git initalized"
	@echo ""
	@echo "make isort:"
	@echo "       Run isort command cli in development features"
	@echo ""
	@echo "make lint:"
	@echo "       Run lint"
	@echo ""
	@echo "make coverage:"
	@echo "       Run tests with coverage and generate a badge (svg)"
	@echo ""
	@echo "make test:"
	@echo "       Run tests with coverage, lint, and clean commands"
	@echo ""
	@echo "make dev:"
	@echo "       Run the dev web application, with tests and coverage"
	@echo ""
	@echo "make run:"
	@echo "       Run the web application without tests"
	@echo ""
	@echo "make release:"
	@echo "       Creates a new tag and set the version in this package"
	@echo "       Ex: make release v=1.0.0"
	@echo ""

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . | grep -E "__pycache__|.pyc|.DS_Store$$" | xargs rm -rf

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clone-dotenv:
	@echo "---- Clone dotenv ----"
	@cp .env-example .env
	@echo "---- Finish clone ----"

setup:
	@echo "---- Installing Python dependencies ----"
	@pip install -r requirements/prod.txt --upgrade

setup_dev: clone-dotenv
	@echo "---- Installing Python dev dependencies ----"
	@pip install -r requirements/dev.txt --upgrade
	@flake8 --install-hook git
	@git config --bool flake8.strict true

coverage:
	@echo "---- Running tests coverage ----"
	@pytest --cov=apps --color=yes tests/
	@coverage-badge > static/coverage.svg

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint: clean
	flake8

test: lint
	@pytest --verbose --cov=apps --color=yes tests/

dev: test
	python application.py

run:
	python application.py

release:

	@if [ "$(v)" == "" ]; then \
		echo "You need to specify the new release version. Ex: make release v=1.0.0" \
		exit 1; \
	fi

	@if ! make coverage; then \
		echo "Error" \
		exit 1; \
	fi

	@if ! make lint; then \
		echo "Error" \
		exit 1; \
	fi

	@echo "creating a new release ${v}"
	@echo "version = '${v}'" > `pwd`/__version__.py
	@git add `pwd`/__version__.py
	@git add `pwd`/static/coverage.svg
	@git commit -m '${v}'
	@git tag ${v}
	@git push origin ${v}
	@git push --set-upstream origin "${GIT_CURRENT_BRANCH}"
	@git push origin
