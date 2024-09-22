# Djangolog application

## Install dependencies

```bash
poetry env use 3.12.5
poetry install
# Install npm dependencies
npm install
```

## Start project

1. Create local certs to use server over HTTPS: `mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1`. Put generated files into `certs` directory
2. Start Docker and run `docker-compose up -d` from `docker` directory. Run local version of docker-compose: `docker-compose -f docker-compose.yml -f docker-compose.local.yml up`
3. Start Celery worker `make worker`
4. Start Django app `poetry run python manage.py runserver` or `make dev`
******5**. Visit `https://localhost:8000/`

## Create superuser

Creates superuser with the following credentials

email: admin@gmail.com
password: superPassword12

```bash
make create-superuser
```

## Populate Post database with some random data

`DJANGO_ENV=local poetry run python manage.py shell`

```python
from djangoblog.factory import AccountFactory
AccountFactory.create_batch(50)
```

## Swagger Docs

API documentation is available at: `/api/docs`

## Load testing

For load testing we are using Locust
`poetry run locust -f locustfile.py --host=http://localhost:9020`

## Terraform

1. `terraform apply --parallelism=20`
2. Create secret from file: `kubectl create secret generic google-credentials --from-file=infra/terraform/gcp-creds.json -n default`
3. Create secrets from `.env` file: `kubectl create secret generic djapp --from-env-file=<(env -i sh -c "set -a; . .test-secret; printenv | grep -v '^PWD='")`
4. Apply kubernetes config `kubernetes apply -f infra/k8`
