helm-upgrade: ## Upgrade Helm chart
	helm upgrade --namespace production django-blog infra/k8s --values infra/k8s/values.yaml

helm-apply: ## Apply Helm chart
	helmfile --namespace production --file helmfile.yaml apply
