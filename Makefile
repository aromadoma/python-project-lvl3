build:
	poetry build

install:
	poetry install

package-install:
	pip install --user dist/*.whl

test:
	poetry run pytest page_loader/ tests

lint:
	poetry run flake8 page_loader/

check:	lint test

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests
