
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache .mypy_cache ./schema/.mypy_cache .coverage

test:
	pytest

PROJECT = authark
COVFILE ?= .coverage
TESTS ?= tests/

mypy:
	mypy $(PROJECT)

mypy-application:
	mypy $(PROJECT)/application

coverage-application:
	export COVERAGE_FILE=$(COVFILE); \
	pytest --cov-branch --cov=$(PROJECT)/application tests/application/ \
	--cov-report term-missing -x -s -W ignore::DeprecationWarning \
	-o cache_dir=/tmp/$(PROJECT)/cache

coverage:
	export COVERAGE_FILE=$(COVFILE); pytest --testmon --cov-branch \
	--cov=$(PROJECT) $(TESTS) --cov-report term-missing -x -s \
	-vv -o cache_dir=/tmp/$(PROJECT)/cache

update-requirements:
	pip-review --auto
	pip freeze > requirements.txt

serve:
	python -m $(PROJECT) serve

console:
	export echo $$(cat /etc/opt/authark/authark.env | xargs) && \
	python -m $(PROJECT) console

push:
	git push origin HEAD && git push --tags

PART ?= patch

version:
	bump2version $(PART) $(PROJECT)/__init__.py --tag --commit

uninstall-all:
	pip freeze | xargs pip uninstall -y

install-all:
	pip install -r requirements.txt

upgrade-all:
	pip-review --local --auto

update:
	git clean -xdf
	git reset --hard
	git checkout master
	git pull --depth=1
	git checkout `git describe --tags`

deploy:
	ansible-playbook -c local -i localhost, setup/deploy.yml

local:
	./setup/local.sh

gitmessage:
	touch .gitmessage
	echo "\n# commit message\n.gitmessage" >> .gitignore
	git config commit.template .gitmessage

activate:
	echo "set -a; source /etc/opt/authark/authark.env; set +a"
