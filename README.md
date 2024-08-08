# Djangolog application

## Install dependencies

```bash
poetry env use 3.10.14
poetry install
# Install npm dependencies
npm install
```

## Start project

1. Start Docker and run `docker-compose up -d` from `docker` directory
2. Start Celery worker `make worker`
3. Start Django app `poetry run python manage.py runserver` or `make dev`
4. Visit `https://localhost:8000/`

## Create superuser

Creates superuser with the following credentials

email: admin@gmail.com
password: superPassword12

```bash
make create-superuser
```

## Load testing

For load testing we are using Locust
`poetry run locust -f locustfile.py --host=http://localhost:9020`

## Access Kibana logs
