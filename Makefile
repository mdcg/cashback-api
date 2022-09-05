.PHONY: install run lint format security

install:
	@pip install -r requirements.txt

start-deps:
	@docker-compose up -d db rabbitmq

start-mock-servers:
	@docker-compose up -d mock_api mock_consumer

start-api:
	@docker-compose up api

run:
	@python -m cashback.api.run

lint:
	@flake8 --ignore=W605,E203 cashback
	@black -l 79 --check --exclude env .

format:
	@black -l 79 --exclude env .

tests:
	@python -m unittest

security:
	@bandit -r cashback
