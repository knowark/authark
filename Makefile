
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache
	rm -f .coverage

test:
	pytest

coverage-application: 
	pytest -x --cov=authark/application tests/application/ \
	--cov-report term-missing -s

coverage-infrastructure: 
	pytest -x --cov=authark/infrastructure tests/infrastructure/ \
	--cov-report term-missing -s

coverage: 
	pytest -x --cov=authark tests/ --cov-report term-missing -s

PART ?= patch
A
version:
	bump2version $(PART) authark/__init__.py --tag --commit
