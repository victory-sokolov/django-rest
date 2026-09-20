.PHONY: redis-certs memray memray-record memray-flamegraph memray-summary

GIT_COMMIT_HASH ?= $(shell git rev-parse --short HEAD 2>/dev/null)
EXCLUDED_DIRS = infra/k8s/haproxy
ENV := $(or ${DJANGO_ENV}, local)
PORT := $(or ${PORT}, 8080)
RUN_IN_DOCKER := $(or ${IN_DOCKER}, true)
UV_RUN ?= uv run

MEMRAY_DIR ?= memray
MEMRAY_BIN ?= $(MEMRAY_DIR)/app.bin
MEMRAY_FLAMEGRAPH ?= $(MEMRAY_DIR)/flamegraph.html
MEMRAY_COMMAND ?= manage.py runserver 0.0.0.0:8001 --noreload

NPROCS := $(shell getconf _NPROCESSORS_ONLN)
FAIL_TEST_UNDER := 100

export DOCKER_BUILDKIT ?= 1

ifeq ($(RUN_IN_DOCKER), true)
	MEMRAY_COMPOSE := docker compose -f docker-compose.yml -f docker-compose.memray.yml
	CMD := $(MEMRAY_COMPOSE) run --rm app
	MEMRAY_RECORD_CMD := $(MEMRAY_COMPOSE) run --rm --service-ports app
	MEMRAY_REPORT_CMD := $(MEMRAY_COMPOSE) run --rm app
	MEMRAY_PATH := /app
else:
	CMD :=
	MEMRAY_COMPOSE :=
	MEMRAY_RECORD_CMD :=
	MEMRAY_REPORT_CMD :=
	MEMRAY_PATH := ./
endif

shell: ## Django shell
	DJANGO_ENV=$(ENV) uv run python manage.py shell_plus

check-migrations: ## Check for unapplied migrations
	DJANGO_ENV=$(ENV) uv run python manage.py makemigrations --check

migrate: ## Run migrations
	$(CMD) sh -c 'DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py migrate --no-input'
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
	DJANGO_ENV=$(ENV) uv run python manage.py check --deploy
	DJANGO_ENV=$(ENV) uv run python manage.py check


test: ## Run tests with coverage
	@$(CMD) sh -c ' \
		DJANGO_ENV=test; \
			uv run coverage run manage.py test -v 2 && \
			uv run coverage combine && \
			uv run coverage report; \
		'

test-single: ## Run a single test with coverage
	DJANGO_ENV=test uv run python manage.py test

redis-certs: ## Generate local Redis TLS certificates when they are missing
	@if [ ! -f docker/redis/tls/ca.crt ] || [ ! -f docker/redis/tls/redis.crt ] || [ ! -f docker/redis/tls/redis.key ]; then \
		bash docker/redis/generate_redis_certs.sh; \
	fi

memray-record: redis-certs ## Record allocations while running MEMRAY_COMMAND (Ctrl-C to stop)
	@mkdir -p $(MEMRAY_DIR)
	$(MEMRAY_RECORD_CMD) sh -c 'exec memray run --native --force -o $(MEMRAY_PATH)/$(MEMRAY_BIN) $(MEMRAY_COMMAND)'

memray-flamegraph: ## Generate a leak-focused interactive HTML flame graph
	@test -f $(MEMRAY_BIN) || (echo "Missing $(MEMRAY_BIN); run 'make memray-record' first" >&2; exit 1)
	@mkdir -p $(MEMRAY_DIR)
	$(MEMRAY_REPORT_CMD) memray flamegraph --leaks --force -o $(MEMRAY_PATH)/$(MEMRAY_FLAMEGRAPH) $(MEMRAY_PATH)/$(MEMRAY_BIN)

memray-summary: ## Print the allocation summary for the latest recording
	@test -f $(MEMRAY_BIN) || (echo "Missing $(MEMRAY_BIN); run 'make memray-record' first" >&2; exit 1)
	$(MEMRAY_REPORT_CMD) memray summary $(MEMRAY_PATH)/$(MEMRAY_BIN)

memray: ## Record allocations and generate a flame graph (Ctrl-C stops recording)
	@$(MAKE) memray-record; status=$$?; \
	if [ $$status -ne 0 ] && [ $$status -ne 130 ] && [ $$status -ne 143 ]; then exit $$status; fi
	@$(MAKE) memray-flamegraph

build-local: load-fixtures migrate create-superuser create-posts  ## Build local environment
	DJANGO_ENV=local uv install --no-root

load-fixtures: ## Load local and test fixtures
	$(CMD) sh -c 'DJANGO_ENV=$(ENV) uv run python manage.py loaddata djangoblog/fixtures/*.yaml'

flush-db: ## Reset local DB
	DJANGO_ENV=local uv run python manage.py flush

create-superuser: ## Create a new superuser
	$(CMD) sh -c 'DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py create_superuser \
		--user=admin \
		--password=superPassword12 \
		--email=admin@gmail.com'

create-posts: ## Generate random posts
	$(CMD) sh -c 'DJANGO_ENV=$(ENV) $(UV_RUN) python manage.py create_posts --count 100'

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

compose-up: ## Docker compose up
	docker network create docker-elk_elk 2>/dev/null || true
	COMPOSE_BAKE=true docker compose up

compose-down: ## Remove main docker containers and local containers
	COMPOSE_BAKE=true docker compose -f docker-compose.yml -f docker-compose.local.yml down --remove-orphans -v

docker-local: ## Run local docker compose with metrics
	COMPOSE_BAKE=true docker compose -f docker-compose.yml -f docker-compose.local.yml up

docker-profile:
	COMPOSE_BAKE=true docker compose -f docker-compose.yml -f docker-compose.profile.yml up

minikube-start: ## Start Minikube cluster
	minikube start --driver=docker --cpus=4 --memory=6g --disk-size=25g
	minikube addons enable metrics-server
	minikube addons enable ingress
	minikube addons enable storage-provisioner
	minikube addons enable default-storageclass
	@kubectl create namespace production --dry-run=client -o yaml | kubectl apply -f -
	@if ! kubectl get secret app-secret -n production &>/dev/null; then \
		echo "Creating app-secret..."; \
		kubectl create secret generic app-secret --from-env-file=.env.prod -n production; \
	else \
		echo "app-secret already exists, skipping creation"; \
	fi


push-image: ## Push Docker image to registry
	@if ! docker buildx inspect orbstack-builder >/dev/null 2>&1 && \
	   ! docker buildx inspect desktop-builder >/dev/null 2>&1; then \
		if docker info 2>/dev/null | grep -q "orbstack\|OrbStack"; then \
			echo "Creating orbstack-builder..."; \
			docker buildx create --name orbstack-builder --driver docker-container --use 2>/dev/null || docker buildx use orbstack-builder; \
		else \
			echo "Creating desktop-builder..."; \
			docker buildx create --name desktop-builder --driver docker-container --use 2>/dev/null || docker buildx use desktop-builder; \
		fi \
	fi
	docker buildx build \
		-t victorysokolov/django-blog:${GIT_COMMIT_HASH} \
		--platform linux/amd64,linux/arm64 \
		--push \
		--cache-from=type=registry,ref=victorysokolov/django-blog:buildcache \
		--cache-to=type=registry,ref=victorysokolov/django-blog:buildcache,mode=max \
		.

deploy: push-image ## Deploy application to Kubernetes
	# Modify image tag
	sed -i "s/tag:[[:space:]]*[^[:space:]]*/tag: ${GIT_COMMIT_HASH}/g" infra/k8s/values.yaml

terraform-apply: ## Apply Terraform configuration
	cd infra/terraform && terraform -chdir=infra/terraform/providers/gcloud apply --parallelism=20 -auto-approve

kube-secrets: ## Create secrets for kubernetes from .env file
	kubectl create secret generic app-secret --from-env-file=.env -n production

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help
