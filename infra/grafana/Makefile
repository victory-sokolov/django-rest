setup: ## Setup
	go install -a github.com/jsonnet-bundler/jsonnet-bundler/cmd/jb@latest
	go install github.com/grafana/dashboard-linter@latest
	jb install

build-lint: ## Build and lint Grafana dashboard
	jsonnet -J vendor dashboard.jsonnet -o provisioning/dashboards/dashboard.json
	dashboard-linter lint provisioning/dashboards/dashboard.json


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
