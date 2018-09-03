
clean:
	find . -name '__pycache__' -exec rm -fr {} +

test:
	pytest

coverage-application: 
	pytest -x --cov=authark/application tests/application/ \
	--cov-report term-missing

coverage-infrastructure: 
	pytest -x --cov=authark/infrastructure tests/infrastructure/ \
	--cov-report term-missing	

