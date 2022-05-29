
analyze: ## Run prospektor for static analysis
	prospector --profile prospector djangoblog

make-migrations: ## Run migrations
	python manage.py makemigrations
	python manage.py migrate

worker: ## Run celery worker
	watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A djangoblog worker -l info

test: ## Run tests with coverage
	coverage run manage.py test -v 2
	coverage report
	coverage html

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help
