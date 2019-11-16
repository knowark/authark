
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache
	rm -f .coverage
	rm -rf .mypy_cache

test:
	pytest

COVFILE ?= .coverage
PWD = $(shell pwd)
PROJECT = authark

coverage-application:
	mypy $(PROJECT)/application
	export COVERAGE_FILE=$(COVFILE); pytest -x \
	--cov=$(PWD)/$(PROJECT)/application $(PWD)/tests/application/ \
	--cov-report term-missing \
	--cov-report xml:$(COVFILE).xml -s -vv \
	-o cache_dir=/tmp/pytest/cache

coverage-infrastructure:
	mypy $(PROJECT)/infrastructure
	export COVERAGE_FILE=$(COVFILE); pytest -x \
	--cov=$(PWD)/$(PROJECT)/infrastructure $(PWD)/tests/infrastructure/ \
	--cov-report term-missing \
	--cov-report xml:$(COVFILE).xml -s -vv \
	-o cache_dir=/tmp/pytest/cache

coverage: 
	mypy $(PROJECT)
	export COVERAGE_FILE=$(COVFILE); pytest -x \
	--cov=$(PWD)/$(PROJECT) $(PWD)/tests/ \
	--cov-report term-missing \
	--cov-report xml:$(COVFILE).xml -s -vv \
	-o cache_dir=/tmp/pytest/cache

update:
	pip-review --auto
	pip freeze > requirements.txt

serve:
	python -m $(PROJECT) serve

terminal:
	python -m $(PROJECT) terminal

PART ?= patch

version:
	bump2version $(PART) $(PROJECT)/__init__.py --tag --commit
