pytest:
	docker compose up -d
	docker compose exec pytest-example pytest -vvs -n auto


mypy:
	docker compose up -d
	docker compose exec pytest-example mypy src/  --ignore-missing-imports
	docker compose exec pytest-example mypy tests/ --ignore-missing-imports


test:
	make pytest
	make mypy
