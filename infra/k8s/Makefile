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

argo-pass:
	kubectl get secret argocd-initial-admin-secret -n argocd \
  		-o jsonpath="{.data.password}" | base64 -d; echo

argo-port-forward:
	kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=30s
