# Djangolog application

- Run makefile commands in the Docker container
```bash
export RUN_IN_DOCKER=true
make test
```


## Install dependencies

```bash
uv init
uv pip install
# Install npm dependencies
npm install
```

## Start project

1. Create local certs to use server over HTTPS: `mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1`. Put generated files into `certs` directory
2. Start Docker and run `docker-compose up -d` from `docker` directory. Run local version of docker-compose: `docker-compose -f docker-compose.yml -f docker-compose.local.yml up`
3. Start Celery worker `make worker`
4. Start Django app `uv run python manage.py runserver` or `make dev`.
5. Visit `https://localhost:8000/`

## Create superuser

Creates superuser with the following credentials

email: admin@gmail.com
password: superPassword12

```bash
make create-superuser
```

## Populate post table with some random data

`DJANGO_ENV=local uv run python manage.py shell`

```python
from djangoblog.factory import AccountFactory
AccountFactory.create_batch(50)
```

## Swagger Docs

API documentation is available at: `/api/docs`

## Load testing

For load testing we are using Locust
`uv run locust -f locustfile.py --host=http://localhost:9020`

Run with entr to reload on changes
Install: `brew install entr`
Run: `ls locustfile.py | entr -r uv run locust -f locustfile.py --host=http://localhost:9020`

## Launch Debugger

- `docker-compose -f docker-compose.yml -f docker-compose.debug.yml up`

## Terraform

1. `terraform apply --parallelism=20 -auto-approve`
2. Create secret from file: `kubectl create secret generic google-credentials --from-file=infra/terraform/gcp-creds.json -n default`
3. Create secrets from `.env` file: `kubectl create secret generic app --from-env-file=<(env -i sh -c "set -a; . .env; printenv | grep -v '^PWD='")`
4. Apply kubernetes config `kubernetes apply -f infra/k8`


# Install Kibana and Elasticsearch

1. Clone repo https://github.com/deviantony/docker-elk
2. `docker compose up setup`
3. `docker compose up`
4. Open Kibana: `http://localhost:5601/`
5. Credentials:
  - username: `elastic`
  - password: `changeme`


## Perform test mutation

1. Initialise session `uv run cosmic-ray init test_mutation.toml test.sqlite`
2. `uv run cosmic-ray --verbosity=INFO baseline test_mutation.toml`
3. `uv run cosmic-ray exec test_mutation.toml test.sqlite`
