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
	@echo "make clone-dotenv"
	@echo "       Creates .env file base on .env-example"
	@echo "       Used by setup_dev command"
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
	find . | grep -E "__pycache__|.pytest_cache|.pyc|.DS_Store$$" | xargs rm -rf

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clone-dotenv:
	@echo "---- Clone dotenv ----"
	@cp .env-example .env
	@echo "---- Finish clone ----"

coverage: test
	@echo "---- Create coverage ----"
	@coverage-badge > static/coverage.svg

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint: clean
	pylint

test:
	@pytest -s --verbose --disable-warnings --cov=apps --color=yes tests/

dev: lint test
	python run.py

release:
	@echo "creating a new release ${v}"
	@echo "version = '${v}'" > `pwd`/__version__.py
	@git add `pwd`/__version__.py
	@git add `pwd`/static/coverage.svg
	@git commit -m '${v}'
	@git tag ${v}
	@git push origin ${v}
	@git push --set-upstream origin "${GIT_CURRENT_BRANCH}"
	@git push origin
