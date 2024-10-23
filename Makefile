GIT_COMMIT_HASH := $(shell git rev-parse HEAD)
EXCLUDED_DIRS = infra/k8s/haproxy
ENV := $(or ${DJANGO_ENV}, local)
PORT := $(or ${PORT}, 8080)

migrate: ## Run migrations
	DJANGO_ENV=$(ENV) uv run python manage.py migrate --no-input

make-migrations: migrate ## Create and run migrations
	DJANGO_ENV=$(ENV) uv run python manage.py makemigrations

dev: ## Run dev server
	# DJANGO_ENV=local uv run python manage.py runserver_plus --cert-file certs/cert.pem --key-file certs/certkey.pem
	DJANGO_ENV=$(ENV) uv run python manage.py runserver 0.0.0.0:$(PORT)

prod:
	DJANGO_ENV=$(ENV) gunicorn djangoblog.wsgi:application --config gunicorn.py --bind 0.0.0.0:$(PORT)

worker: ## Run celery worker
	DJANGO_ENV=$(ENV) uv run watchmedo auto-restart \
		--directory=./djangoblog \
		--pattern="**/tasks/*.py" \
		--recursive -- \
		uv run celery -A djangoblog worker -l info
	# DJANGO_ENV=local uv run celery -A djangoblog worker -l info

start: ## Start project with uvicorn
	DJANGO_ENV=$(ENV) uvicorn djangoblog.asgi:application --port 8081 --reload

flower: ## Run Flower Celery monitoring system
	DJANGO_ENV=local uv run celery -A djangoblog.celery.app flower

collectstatic:
	DJANGO_ENV=$(ENV) uv run python manage.py collectstatic --noinput -i silk/*
	DJANGO_ENV=$(ENV) uv run python manage.py compress --force


loadtest: ## Load test app
	loadtest -n 300 -k  http://localhost:8081/post/

mypy:
	DJANGO_ENV=$(ENV) uv run mypy --config-file pyproject.toml djangoblog --cache-fine-grained

run-checks:
	DJANGO_ENV=$(ENV) uv run python manage.py check --deploy
	DJANGO_ENV=$(ENV) uv run python manage.py check

test: ## Run tests with coverage
	DJANGO_ENV=test uv run coverage run --parallel-mode --concurrency=multiprocessing manage.py test --parallel -v 2 --failfast
	DJANGO_ENV=test uv run coverage combine
	DJANGO_ENV=test uv run coverage report
	DJANGO_ENV=test uv run coverage html

build-local: load-fixtures migrate
	DJANGO_ENV=local uv install --no-root

load-fixtures: ## Load local and test fixtures
	DJANGO_ENV=$(ENV) uv run python manage.py loaddata djangoblog/fixtures/*.yaml

flush-db: ## Reset local DB
	DJANGO_ENV=local uv run python manage.py flush

create-superuser: ## Create a new superuser
	DJANGO_ENV=$(ENV) uv run python manage.py create_superuser \
		--user=admin \
		--password=superPassword12 \
		--email=admin@gmail.com

create-posts: ## Generate random posts
	DJANGO_ENV=$(ENV) uv run python manage.py create_posts --count 100

print-settings:
	DJANGO_ENV=$(ENV) uv run python manage.py print_settings

install-dev:
	DJANGO_ENV=local python uv sync --no-install-project --extra dev --frozen

# Infra commands

docker-build:
	docker-compose up --build -d --remove-orphans

compose-up: ## Docker compose up with watch
	docker compose up --watch

docker-local:
	​docker compose -f docker-compose.yml -f docker-compose.local.yml up -d

push-image:
	docker buildx build -t victorysokolov/django-blog:$(GIT_COMMIT_HASH) --push --platform linux/amd64,linux/arm64 .

deploy: push-image
	# Modify image tag
	sed -i "s/victorysokolov\/django-blog:[^ ]*/victorysokolov\/django-blog:${GIT_COMMIT_HASH}/g" infra/k8s/django/app-deployment.yaml
	sed -i "s/victorysokolov\/django-blog:[^ ]*/victorysokolov\/django-blog:${GIT_COMMIT_HASH}/g" infra/k8s/celery/celery-worker-pod.yaml
	sed -i "s/victorysokolov\/django-blog:[^ ]*/victorysokolov\/django-blog:${GIT_COMMIT_HASH}/g" infra/k8s/debugpy/app-debug-service.yaml
	sed -i "s/victorysokolov\/django-blog:[^ ]*/victorysokolov\/django-blog:${GIT_COMMIT_HASH}/g" infra/k8s/jobs/staticfiles-job.yaml
	kubectl apply -f infra/k8s --recursive
	# find infra/k8s -type f -name "*.yaml" | grep -v -E "$$(echo $$EXCLUDED_DIRS | sed 's/ /|/g')" | xargs -I {} kubectl apply -f {}
	kubectl get pods

terraform-apply:
	cd infra/terraform && terraform -chdir=infra/terraform/providers/gcloud apply --parallelism=20 -auto-approve

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help
