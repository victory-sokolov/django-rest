GIT_COMMIT_HASH := $(shell git rev-parse HEAD)
EXCLUDED_DIRS = infra/k8s/haproxy

migrate: ## Run migrations
	DJANGO_ENV=local poetry run python manage.py migrate

make-migrations: migrate ## Create and run migrations
	DJANGO_ENV=local poetry run python manage.py makemigrations

dev: ## Run dev server
	# DJANGO_ENV=local poetry run python manage.py runsslserver 0.0.0.0:8000
	DJANGO_ENV=local poetry run python manage.py runserver_plus --cert-file certs/cert.pem --key-file certs/certkey.pem

worker: ## Run celery worker
	DJANGO_ENV=local poetry run celery -A djangoblog worker -l info
	# DJANGO_ENV=poetry run watchmedo auto-restart --directory=./ --pattern="*.py" --recursive -- poetry run celery -A djangoblog worker -l info

start: ## Start project with uvicorn
	DJANGO_ENV=local uvicorn djangoblog.asgi:application --port 8081 --reload

flower: ## Run Flower Celery monitoring system
	DJANGO_ENV=local poetry run celery -A djangoblog.celery.app flower

collectstatic:
	DJANGO_ENV=local poetry run python manage.py collectstatic --noinput

prod:
	DJANGO_ENV=production gunicorn djangoblog.wsgi:application --config gunicorn.py --bind 0.0.0.0:"${PORT:-80}"

showoutdated: ## Show outdated Poetry packages
	poetry show --outdated -T

loadtest: ## Load test app
	loadtest -n 300 -k  http://localhost:8081/post/

mypy:
	DJANGO_ENV=local poetry run mypy --config-file pyproject.toml djangoblog --cache-fine-grained

security-check:
	DJANGO_ENV=production poetry run python manage.py check --deploy

test: ## Run tests with coverage
	DJANGO_ENV=test poetry run coverage run --parallel-mode --concurrency=multiprocessing manage.py test --parallel -v 2
	DJANGO_ENV=test poetry run coverage combine
	DJANGO_ENV=test poetry run coverage report
	DJANGO_ENV=test poetry run coverage html

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

install-dev:
	DJANGO_ENV=local poetry install --no-root

docker-build:
	docker-compose up --build -d --remove-orphans

docker-local:
	​docker-compose -f docker-compose.yml -f docker-compose.local.yml up

push-image:
	docker buildx build -t victorysokolov/django-blog:$(GIT_COMMIT_HASH) --push --platform linux/amd64,linux/arm64 .

deploy: push-image
	# Modify image tag
	sed -i "s/victorysokolov\/django-blog:[^ ]*/victorysokolov\/django-blog:${GIT_COMMIT_HASH}/g" infra/k8s/django/app-deployment.yaml
	sed -i "s/victorysokolov\/django-blog:[^ ]*/victorysokolov\/django-blog:${GIT_COMMIT_HASH}/g" infra/k8s/celery/celery-worker-pod.yaml
	sed -i "s/victorysokolov\/django-blog:[^ ]*/victorysokolov\/django-blog:${GIT_COMMIT_HASH}/g" infra/k8s/debugpy/app-debug-service.yaml
	# sed -i "s/victorysokolov\/django-blog:[^ ]*/victorysokolov\/django-blog:${GIT_COMMIT_HASH}/g" infra/k8s/staticfiles-job.yaml

	find infra/k8s -type f -name "*.yaml" | grep -v -E "$$(echo $$EXCLUDED_DIRS | sed 's/ /|/g')" | xargs -I {} kubectl apply -f {}
	kubectl get pods

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help
