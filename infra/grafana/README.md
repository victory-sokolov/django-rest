
## Requirements

1. Install jsonnet: `brew install jsonnet`
2. Install `jb`. The jsonnet-bundler is a package manager for Jsonnet. Note it requries Go. `go install -a github.com/jsonnet-bundler/jsonnet-bundler/cmd/jb@latest`
3. Insall Grafana json linter: `go install github.com/grafana/dashboard-linter@latest`
4. Run `jb install` inside `infra/grafana` directory
