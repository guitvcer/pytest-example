pytest:
	docker compose up -d
	docker compose exec pytest-example pytest -vvs -n auto


mypy:
	docker compose up -d
	docker compose exec pytest-example mypy src/  --ignore-missing-imports
	docker compose exec pytest-example mypy tests/ --ignore-missing-imports


ruff_check:
	docker compose up -d
	docker compose exec pytest-example ruff check src/ tests/


ruff_format:
	docker compose up -d
	docker compose exec pytest-example ruff format src/ tests/


test:
	make pytest
	make mypy
	make ruff_format
	make ruff_check
