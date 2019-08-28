
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache
	rm -f .coverage
	rm -rf .mypy_cache

test:
	pytest

COVFILE ?= .coverage
PWD = $(shell pwd)

coverage-application:
	mypy authark/application
	export COVERAGE_FILE=$(PWD)/$(COVFILE); pytest -x \
	--cov=$(PWD)/authark/application $(PWD)/tests/application/ \
	--cov-report term-missing \
	--cov-report xml:$(PWD)/$(COVFILE).xml -s -vv \
	-o cache_dir=/tmp/pytest/cache

coverage-infrastructure:
	mypy authark/infrastructure
	export COVERAGE_FILE=$(PWD)/$(COVFILE); pytest -x \
	--cov=$(PWD)/authark/infrastructure $(PWD)/tests/infrastructure/ \
	--cov-report term-missing \
	--cov-report xml:$(PWD)/$(COVFILE).xml -s -vv \
	-o cache_dir=/tmp/pytest/cache

coverage: 
	mypy authark
	export COVERAGE_FILE=$(PWD)/$(COVFILE); pytest -x \
	--cov=$(PWD)/authark $(PWD)/tests/ \
	--cov-report term-missing \
	--cov-report xml:$(PWD)/$(COVFILE).xml -s -vv \
	-o cache_dir=/tmp/pytest/cache

update:
	pip-review --auto
	pip freeze > requirements.txt

serve:
	python -m authark serve

terminal:
	python -m authark terminal

PART ?= patch

version:
	bump2version $(PART) authark/__init__.py --tag --commit
