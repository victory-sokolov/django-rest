
analyze: ## Run prospektor for static analysis
	poetry run prospector --profile prospector djangoblog

migrate: ## Run migrations
	DJANGO_ENV=local poetry run python manage.py migrate

make-migrations: migrate ## Create and run migrations
	DJANGO_ENV=local poetry run python manage.py makemigrations

dev: ## Run dev server
	DJANGO_ENV=local poetry run python manage.py runsslserver 0.0.0.0:8000

worker: ## Run celery worker
	DJANGO_ENV=local poetry run celery -A djangoblog worker -l info
	# watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A djangoblog worker -l info

start: ## Start project with uvicorn
	DJANGO_ENV=local uvicorn djangoblog.asgi:application --port 8081 --reload

prod:
	DJANGO_ENV=production gunicorn djangoblog:asgi:application -w 4 -k uvicorn.workers.UvicornWorker --log-file -

showoutdated: ## Show outdated Poetry packages
	poetry show --outdated -T

loadtest: ## Load test app
	loadtest -n 300 -k  http://localhost:8081/post/

mypy:
	DJANGO_ENV=local poetry run mypy --config-file pyproject.toml djangoblog --cache-fine-grained

security-check:
	DJANGO_ENV=production poetry run python manage.py check --deploy

tests: ## Run tests with coverage
	DJANGO_ENV=test poetry run coverage run --parallel-mode --concurrency=multiprocessing manage.py test --parallel -v 2
	DJANGO_ENV=test poetry run coverage combine
	DJANGO_ENV=test poetry run coverage report
	DJANGO_ENV=test poetry run coverage html

test: ## Run single test
	DJANGO_ENV=test poetry run python manage.py test

build-local: load-fixtures migrate
	DJANGO_ENV=local poetry install --no-root

load-fixtures: ## Load local and test fixtures
	DJANGO_ENV=local poetry run python manage.py loaddata djangoblog/fixtures/*.yaml

flush-db: ## Reset local DB
	DJANGO_ENV=local poetry run python manage.py flush

create-superuser: ## Create a new superuser
	DJANGO_ENV=local poetry run python manage.py create_superuser \
		--user=Admin \
		--password=superPassword12 \
		--email=admin@gmail.com

upgrade-deps:
	poetry up --latest

install:
	DJANGO_ENV=local poetry install --no-root

docker-build:
	docker-compose up --build -d --remove-orphans

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help
