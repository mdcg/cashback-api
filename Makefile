.PHONY: install run lint format security

install:
	@pip install -r requirements.txt

deps:
	@docker-compose up -d db rabbitmq

mock-servers:
	@docker-compose up -d mock_api mock_consumer

run:
	@python -m cashback.api.run

lint:
	@flake8 --ignore=W605,E203 cashback
	@black -l 79 --check --exclude env .

format:
	@black -l 79 --exclude env .

security:
	@echo "Running Bandit..."
	@bandit -r cashback
