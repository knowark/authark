
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache
	rm -f .coverage

test:
	pytest

COVFILE ?= .coverage

coverage-application:
	mypy authark
	export COVERAGE_FILE=$(COVFILE); pytest -x --cov=authark/application \
	tests/application/ --cov-report term-missing -s

coverage-infrastructure:
	mypy authark
	export COVERAGE_FILE=$(COVFILE); pytest -x --cov=authark/infrastructure \
	tests/infrastructure/ --cov-report term-missing -s

coverage: 
	mypy authark
	export COVERAGE_FILE=$(COVFILE); pytest -x --cov=authark tests/ \
	--cov-report term-missing -s

PART ?= patch

version:
	bump2version $(PART) authark/__init__.py --tag --commit
