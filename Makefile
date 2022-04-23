
make-migrations: ## Run migrations
	python manage.py makemigrations
	python manage.py migrate

test:
	coverage run manage.py test -v 2
	coverage report
	coverage html

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help
