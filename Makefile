build:
	poetry build

package-install:
	pip install --user dist/*.whl

test:
	poetry run pytest

