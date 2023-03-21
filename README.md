# Djangolog application

## Install dependencies

```bash
poetry install
```

## Start project

1. Start Docker and run `docker-compose up -d`
2. Start Celery worker `make worker`
3. Start Django app `python manage.py runserver`

## Create superuser

```bash
python manage.py createsuperuser
```

