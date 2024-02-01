install_hooks:
	poetry run pre-commit install

black:
	poetry run black .

ruff:
	poetry run ruff .

mypy:
	poetry run mypy .
