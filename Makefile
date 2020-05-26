
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache .mypy_cache ./schema/.mypy_cache .coverage

test:
	pytest

PROJECT = authark
COVFILE ?= .coverage
TESTS ?= tests/

coverage-application:
	export COVERAGE_FILE=$(COVFILE); pytest --cov-branch \
	--cov=$(PROJECT)/application tests/application/ --cov-report \
	term-missing -x -s -W ignore::DeprecationWarning \
	-o cache_dir=/tmp/authark/cache

coverage-infrastructure:
	export COVERAGE_FILE=$(COVFILE); pytest --cov-branch \
	--cov=$(PROJECT)/infrastructure tests/infrastructure/ --cov-report \
	term-missing -x -s -W ignore::DeprecationWarning \
	-o cache_dir=/tmp/authark/cache

coverage:
	mypy authark && export COVERAGE_FILE=$(COVFILE); pytest --cov-branch \
	--cov=$(PROJECT) $(TESTS) --cov-report term-missing -x -s \
	-vv -W ignore::DeprecationWarning -o cache_dir=/tmp/authark/cache

update:
	pip-review --auto
	pip freeze > requirements.txt

serve:
	python -m $(PROJECT) serve

console:
	python -m $(PROJECT) console

PART ?= patch

version:
	bump2version $(PART) $(PROJECT)/__init__.py --tag --commit

uninstall-all:
	pip freeze | xargs pip uninstall -y

install-all:
	pip install -r requirements.txt

upgrade-all:
	pip-review --local --auto
