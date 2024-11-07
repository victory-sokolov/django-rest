

build-lint:
	jsonnet -J vendor dashboard.jsonnet -o dashboard.json
	dashboard-linter lint dashboard.json
