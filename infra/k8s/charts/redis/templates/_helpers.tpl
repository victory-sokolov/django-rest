{{/*
Add common labels for ConfigMap grouping in ArgoCD
*/}}
{{- define "configmap.labels" -}}
argocd.argoproj.io/group: "django-configmaps"
app.kubernetes.io/component: config
{{- end }}
