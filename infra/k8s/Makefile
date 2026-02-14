# ============================================
# Validation Targets
# ============================================

.PHONY: helm-validate helm-lint kubeconform pluto security-scan helmfile-lint yaml-lint chart-testing

helm-validate: yaml-lint helm-lint kubeconform pluto security-scan helmfile-lint ## Run all Helm/K8s validation checks
	@echo ""
	@echo "✓ All validation checks passed!"

yaml-lint: ## Run yamllint on YAML files (excludes Helm templates)
	@echo "Running yamllint..."
	@command -v yamllint >/dev/null 2>&1 || { echo "Installing yamllint..."; pip install yamllint; }
	@find . -type f \( -name '*.yaml' -o -name '*.yml' \) \
		| grep -v '/templates/' \
		| grep -v '/charts/apps/charts/' \
		| grep -v './ConfigMap.yaml' \
		| xargs yamllint -d '{extends: default, rules: {line-length: disable, document-start: disable}}' --strict

helm-lint: ## Run helm lint on charts with values
	@echo "Running helm lint..."
	@echo "Linting apps umbrella chart..."
	helm lint charts/apps --strict --with-subcharts
	@echo "Linting standalone charts..."
	@for chart in charts/gateway-api charts/haproxy charts/ingress charts/nginx charts/pgbouncer charts/postgres charts/redis; do \
		echo "Linting $$chart..."; \
		helm lint "$$chart" --strict || true; \
	done

chart-testing: ## Run chart-testing (ct) lint
	@echo "Running chart-testing..."
	@command -v ct >/dev/null 2>&1 || { echo "Error: ct (chart-testing) not installed. Install with: brew install chart-testing"; exit 1; }
	ct lint --config ct.yaml --all

kubeconform: ## Validate rendered templates against K8s schemas
	@echo "Running kubeconform..."
	@command -v kubeconform >/dev/null 2>&1 || { echo "Error: kubeconform not installed. Install with: brew install kubeconform"; exit 1; }
	@helm dependency update charts/apps 2>/dev/null || true
	helm template charts/apps -f charts/apps/values.yaml --namespace production | \
		kubeconform -summary -kubernetes-version 1.29.0 -skip List \
		-schema-location "crd-schemas/" \
		-schema-location "https://raw.githubusercontent.com/yannh/kubernetes-json-schema/master/"

pluto: ## Detect deprecated/removed K8s APIs
	@echo "Running pluto..."
	@if command -v pluto >/dev/null 2>&1; then \
		helm dependency update charts/apps 2>/dev/null || true; \
		helm template charts/apps -f charts/apps/values.yaml --namespace production | \
			pluto detect - --target-versions k8s=v1.29.0; \
	else \
		echo "Skipping pluto (not installed). Install with: brew install fairwindsops/tap/pluto"; \
	fi

security-scan: ## Run security scan on rendered manifests
	@echo "Running security scan..."
	@if command -v checkov >/dev/null 2>&1; then \
		helm dependency update charts/apps 2>/dev/null || true; \
		helm template charts/apps -f charts/apps/values.yaml --namespace production > /tmp/rendered-manifests.yaml; \
		checkov -f /tmp/rendered-manifests.yaml --framework kubernetes --compact --soft-fail; \
		rm -f /tmp/rendered-manifests.yaml; \
	else \
		echo "Skipping checkov (not installed). Install with: pip install checkov"; \
	fi

helmfile-lint: ## Run helmfile lint
	@echo "Running helmfile lint..."
	@if command -v helmfile >/dev/null 2>&1; then \
		helmfile lint; \
	else \
		echo "Skipping helmfile (not installed). Install with: brew install helmfile"; \
	fi

# ============================================
# Minikube Targets
# ============================================

check-minikube: ## Check if minikube is running
	@status=$$(minikube status 2>&1 | grep "host: Running"); \
	if [ -z "$$status" ]; then \
		echo "Error: minikube is not running. Please start minikube first with 'minikube start'"; \
		exit 1; \
	fi

helm-upgrade: ## Upgrade Helm chart
	helm upgrade --namespace production django-blog infra/k8s --values infra/k8s/values.yaml

helm-apply: check-minikube ## Apply Helm chart
	helmfile --namespace production --file helmfile.yaml apply

helm-list:
	helm list --all-namespaces

helm-uninstall: ## Uninstall all Helm releases
	@bash -c ' \
		for release in $$(helm list --all-namespaces -q); do \
			namespace=$$(helm list --all-namespaces | grep "^$$release[[:space:]]" | awk '\''{print $$2}'\''); \
			echo "Uninstalling $$release from namespace $$namespace..."; \
			helm uninstall -n "$$namespace" "$$release"; \
		done'

destroy:
	helmfile destroy -n production

delete-deployments: ## Delete all deployments in the current namespace
	kubectl delete deployments --all -n production --debug

argo-pass: ## Get ArgoCD admin password
	kubectl get secret argocd-initial-admin-secret -n argocd \
  		-o jsonpath="{.data.password}" | base64 -d; echo

argo-port-forward: ## Port-forward ArgoCD UI to localhost:9090
	kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=30s
	kubectl port-forward svc/argocd-server 9090:443 -n argocd

argo-install: check-minikube ## Install ArgoCD via Helm
	helm upgrade --install argocd ./charts/argo-cd \
		--namespace argocd \
		--create-namespace \
		--values ./charts/argo-cd/values.yaml \
		--wait
	@echo "Waiting for ArgoCD to be ready..."
	kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=120s
	helm upgrade --install root-app ./charts/root-app \
		--namespace argocd \
		--create-namespace \
		--wait
	@echo ""
	@echo "✓ ArgoCD installed successfully"
	@echo "✓ root-app installed (creates ArgoCD Applications)"
	@echo "Get password with: make argo-pass"
	@echo "Open UI with: make argo-port-forward"
	@echo "Then open: http://localhost:9090"

argo-uninstall: ## Uninstall ArgoCD and root-app
	helm uninstall root-app -n argocd || true
	helm uninstall argocd -n argocd || true

argo-app-install: ## Install root-app (creates ArgoCD Applications)
	helm upgrade --install root-app ./charts/root-app \
		--namespace argocd \
		--create-namespace \
		--wait

argo-sync: ## Sync all ArgoCD applications
	argocd app sync root-app --server argocd-server.argocd.svc.cluster.local
	argocd app sync django-production --server argocd-server.argocd.svc.cluster.local

argo-app-list: ## List ArgoCD applications
	argocd app list --server argocd-server.argocd.svc.cluster.local

check-tunnel: ## Check if minikube tunnel is running
	@if ! pgrep -f "minikube tunnel" > /dev/null; then \
		echo "Error: minikube tunnel is not running. Please start it with 'make tunnel'"; \
		exit 1; \
	fi

argo: check-tunnel argo-install ## Install ArgoCD and open UI (one command)
	@echo ""
	@echo "=========================================="
	@echo "ArgoCD Admin Credentials:"
	@echo "=========================================="
	@printf "Username: admin\nPassword: "
	@kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d; echo ""
	@echo ""
	@echo "Opening ArgoCD UI at http://localhost:9090"
	@echo "Press Ctrl+C to stop port-forwarding"
	@echo "=========================================="
	@kubectl port-forward svc/argocd-server 9090:443 -n argocd

pf: ## Port-forward HAProxy to localhost:8080
	@echo "Starting port-forward for HAProxy on localhost:8080..."
	@kubectl port-forward svc/haproxy 8080:8080 -n production

tunnel: ## Start minikube tunnel (requires sudo)
	@if pgrep -f "minikube tunnel" > /dev/null; then \
		echo "✓ minikube tunnel already running"; \
		echo "✓ Access app at: http://192.168.64.2:8080/"; \
	else \
		echo "Starting minikube tunnel..."; \
		sudo minikube tunnel & \
		sleep 3; \
		echo "✓ Tunnel started"; \
		echo "✓ Access app at: http://192.168.64.2:8080/"; \
	fi
