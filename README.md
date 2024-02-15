# Djangolog application

## Install dependencies

```bash
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
password: superPassword

```bash
make create-superuser
```

## Access Kibana logs
