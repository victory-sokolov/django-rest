helm-upgrade: ## Upgrade Helm chart
	helm upgrade --namespace production django-blog infra/k8s --values infra/k8s/values.yaml

helm-apply: ## Apply Helm chart
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
