.PHONY: install test run clean docker-build docker-run

install:
	poetry install

test:
	poetry run pytest tests/ -v

coverage:
	poetry run pytest --cov=app --cov-report=html

lint:
	poetry run ruff check app/
	poetry run mypy app/ --ignore-missing-imports

run:
	poetry run python -m app.main

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache
	rm -rf logs/*.log
	find . -type d -name "__pycache__" -exec rm -rf {} +

docker-build:
	docker build -t sentinel-api:latest .

docker-run:
	docker-compose up -d

docker-logs:
	docker-compose logs -f

docker-stop:
	docker-compose down
