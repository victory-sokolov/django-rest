
analyze: ## Run prospektor for static analysis
	poetry run prospector --profile prospector djangoblog

migrate: ## Run migrations
	poetry run python manage.py migrate

make-migrations: migrate ## Create and run migrations
	poetry run python manage.py makemigrations

dev: ## Run dev server
	poetry run python manage.py runsslserver 0.0.0.0:8000

worker: ## Run celery worker
	poetry run celery -A djangoblog worker -l info
	# watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A djangoblog worker -l info

start: ## Start project with uvicorn
	uvicorn djangoblog.asgi:application --port 8081 --reload

prod:
	gunicorn djangoblog:asgi:application -w 4 -k uvicorn.workers.UvicornWorker --log-file -

showoutdated: ## Show outdated Poetry packages
	poetry show --outdated

loadtest: ## Load test app
	loadtest -n 300 -k  http://localhost:8081/post/

tests: ## Run tests with coverage
	poetry run coverage run manage.py test -v 2
	poetry run coverage report
	poetry run coverage html

test: ## Run single test
	poetry run python manage.py test

build-local: load-fixtures migrate
	poetry install

load-fixtures: ## Load local and test fixtures
	poetry run python manage.py loaddata djangoblog/fixtures/*.yaml

flush-db: ## Reset local DB
	poetry run python manage.py flush

create-superuser: ## Create a new superuser
	poetry run python manage.py create_superuser \
		--user=Admin \
		--password=superPassword12 \
		--email=admin@gmail.com

upgrade-deps:
	poetry up --latest

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help
