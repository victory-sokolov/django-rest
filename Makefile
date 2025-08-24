GIT_COMMIT_HASH := $(shell git rev-parse HEAD)
EXCLUDED_DIRS = infra/k8s/haproxy
ENV := $(or ${DJANGO_ENV}, local)
PORT := $(or ${PORT}, 8080)
RUN_IN_DOCKER ?= false
UV_RUN ?= uv run

NPROCS := $(shell getconf _NPROCESSORS_ONLN)
FAIL_TEST_UNDER := 100


export DOCKER_BUILDKIT ?= 1

ifeq ($(RUN_IN_DOCKER), true)
	CMD := docker compose run --rm app
else:
	CMD :=
endif

shell: ## Django shell
	DJANGO_ENV=$(ENV) uv run python manage.py shell_plus

check-migrations: ## Check for unapplied migrations
	DJANGO_ENV=$(ENV) uv run python manage.py makemigrations --check

migrate: ## Run migrations
	DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py migrate --no-input
	# DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py migrate --database=read_replica

make-migrations: migrate ## Create and run migrations
	DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py makemigrations

dev: ## Run dev server
	# DJANGO_ENV=local uv run python manage.py runserver_plus --cert-file certs/cert.pem --key-file certs/certkey.pem
	echo "Using ${ENV} environment"
	DJANGO_ENV=$(ENV) uv run python manage.py runserver 0.0.0.0:$(PORT)

dev-async: ## Run dev server with uvicorn
	DJANGO_ENV=$(ENV) uv run uvicorn djangoblog.asgi:application

prod: ## Run production server with gunicorn
	DJANGO_ENV=$(ENV) $(UV_RUN) gunicorn djangoblog.wsgi:application --config gunicorn_config.py --bind 0.0.0.0:$(PORT)

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

collectstatic: ## Collect static files and compress them
	DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py collectstatic --noinput -i silk/*
	DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py compress --force

messages: ## Compile translation messages
	DJANGO_ENV=$(ENV) uv run python manage.py compilemessages

loadtest: ## Load test app
	uv run locust -f locustfile.py --users 50 --spawn-rate 1 --host http://localhost:80/post/

mypy: ## Run mypy type checks
	DJANGO_ENV=$(ENV) uv run mypy --config-file pyproject.toml djangoblog --cache-fine-grained

lint-html: ## Lint HTML files with djlint
	uv run djlint djangoblog --extension=html --lint

run-checks: ## Run all checks
	@$(CMD_PREFIX) sh -c ' \
		DJANGO_ENV=$(ENV) uv run python manage.py check --deploy; \
		DJANGO_ENV=$(ENV) uv run python manage.py check; \
	'

test: ## Run tests with coverage
	DJANGO_ENV=test uv run coverage run manage.py test --parallel -v 2
	DJANGO_ENV=test uv run coverage combine
	DJANGO_ENV=test uv run coverage report
	DJANGO_ENV=test uv run coverage html

test-single: ## Run a single test with coverage
	DJANGO_ENV=test uv run python manage.py test

build-local: load-fixtures migrate ## Build local environment
	DJANGO_ENV=local uv install --no-root

load-fixtures: ## Load local and test fixtures
	DJANGO_ENV=$(ENV) uv run python manage.py loaddata djangoblog/fixtures/*.yaml

flush-db: ## Reset local DB
	DJANGO_ENV=local uv run python manage.py flush

create-superuser: ## Create a new superuser
	DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py create_superuser \
		--user=admin \
		--password=superPassword12 \
		--email=admin@gmail.com

create-posts: ## Generate random posts
	DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py create_posts --count 100

print-settings: ## Print Django settings
	DJANGO_ENV=$(ENV) uv run python manage.py print_settings

install-dev: ## Install dev dependencies
	DJANGO_ENV=local uv sync --no-install-project --group dev --frozen

# Prepare project for local development
install: install-dev
	uv run pre-commit install

outdated: ## Check outdated packages
	uv tree --outdated --depth 1

# Infra commands
docker-build: ## Build docker image
	COMPOSE_BAKE=true docker-compose up --build --remove-orphans

compose-up: ## Docker compose up with watch
	docker compose up --watch

compose-down: ## Remove main docker containers and local containers
	docker compose -f docker-compose.yml -f docker-compose.local.yml down --remove-orphans -v

docker-local: ## Run local docker compose with metrics
	docker compose -f docker-compose.yml -f docker-compose.local.yml up

minikube-start: ## Start Minikube cluster
	minikube start --driver=docker --cpus=2 --memory=7g --disk-size=10g
	# Set-up secrets
	kubectl create secret generic app-secret --from-env-file=.env -n production

push-image: ## Push Docker image to registry
	docker buildx build -t victorysokolov/django-blog:$(GIT_COMMIT_HASH) --push --platform linux/amd64,linux/arm64 .

deploy: push-image ## Deploy application to Kubernetes
	# Modify image tag
	sed -i "s/tag:[[:space:]]*[^[:space:]]*/tag: ${GIT_COMMIT_HASH}/g" infra/k8s/values.yaml
	# Apply Helm chart
	helmfile --namespace production --file infra/k8s/helmfile.yaml apply

terraform-apply: ## Apply Terraform configuration
	cd infra/terraform && terraform -chdir=infra/terraform/providers/gcloud apply --parallelism=20 -auto-approve

kube-secrets: ## Create secrets for kubernetes from .env file
	kubectl create secret generic app-secret --from-env-file=.env -n production

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help
