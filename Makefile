.PHONY: install test lint format run docker-build

install:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest

lint:
	ruff check app tests

format:
	black app tests

run:
	uvicorn app.main:app --reload

docker-build:
	docker build -t cloud-cicd-pipeline .
