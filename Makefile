

test:
	pytest

coverage-application: 
	pytest -x --cov=authark/application tests/application/

coverage-infrastructure: 
	pytest -x --cov=authark/infrastructure tests/infrastructure/
