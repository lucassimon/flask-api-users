GIT_CURRENT_BRANCH := ${shell git symbolic-ref --short HEAD}

.PHONY: help clean test clean-build isort run

.DEFAULT: help

help:
	@echo "make clean"
	@echo "       prepare development environment, use only once"
	@echo "make clean-build"
	@echo "       Clear all build directories"
	@echo "make isort"
	@echo "       run isort command cli in development features"
	@echo "make lint"
	@echo "       run lint"
	@echo "make test"
	@echo "       run tests"
	@echo "make run"
	@echo "       run the web application"

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . | grep -E "__pycache__|.pyc|.DS_Store$$" | xargs rm -rf

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

setup:
	@echo "---- Installing Python dependencies ----"
	@pip install -r requirements/prod.txt --upgrade

setup_dev:
	@echo "---- Installing Python dependencies ----"
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

run: test
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
