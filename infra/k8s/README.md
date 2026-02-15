## Prerequirements

1. `brew intall helm`
2. `brew install helmfile`
3. Install helm diff plugin `helm plugin install https://github.com/databus23/helm-diff`
4. Create secrets from `.env` file: `kubectl create secret generic app-secret --from-env-file=.env.prod -n production`
5. `cd infra/k8` and run `helmfile --file helmfile.yaml apply` or `make helm-apply`
6. `minikube tunnel` or run `make tunnel`
7. Set default namespace to production: `kubectl config set-context --current --namespace=production`

### Accessing the App

**Recommended**: Use port-forward (no tunnel needed)
```bash
make pf
# Then open: http://localhost:8080/
```

**Alternative**: Use minikube tunnel
```bash
make tunnel
# Then open: http://192.168.64.2:8080/
```

### Quick Reference

| Command | Description |
|---------|-------------|
| `make pf` | Port-forward HAProxy to localhost:8080 |
| `make tunnel` | Start minikube tunnel (requires sudo) |
| `make url` | Show app access URLs |
| `make helm-apply` | Apply Helm charts |

## Minikube

1. Install minikube: `brew install minikube`
2. Start minikube: `make minikube-start`

## Kube metrics

1. `cd infra/k8` install dependencies `helm dependency update`
2. `helm install kube-state-metrics .`
3. Forward port to acess metrics from local machine: `kubectl port-forward svc/kube-state-metrics 8085:8080 --address=0.0.0.0`

## ArgoCD

1. Install Helm chart: `helm install argo-cd charts/argo-cd/ -n argocd`
2. To access web UI: `kubectl port-forward svc/argo-cd-argocd-server 8089:443 -n argocd`
Visit `http://localhost:8089`
3. Username: `admin`.
Get password: `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" base64 -d; echo`
4. Apply manifest. From `infra/k8s/charts` directory run: `helm install root-app ./root-app/ -n argocd --create-namespace`
5. Upgrade after changes: `helm upgrade root-app ./charts/root-app/ -n argocd`

## Canary Deployments

Canary deployments allow gradual rollout of new versions by routing a percentage of traffic to the canary version while the majority goes to the stable version.

### Configuration

Canary is **disabled by default**. To enable it, update `charts/apps/values.yaml`:

```yaml
gateway-api:
  enabled: true
  canary:
    enabled: true
    weight: 10  # Percentage of traffic to canary (1-100)

django:
  image:
    repository: victorysokolov/django-blog
    tag: v1.2.0  # Stable version
  canary:
    enabled: true
    replicas: 1
    image:
      tag: v1.3.0  # New version to test
    weight: 10  # Should match gateway-api.canary.weight
```

### Gradual Rollout

```yaml
# Start with 10% traffic to canary
canary:
  weight: 10

# Increase to 30%
canary:
  weight: 30

# Increase to 50%
canary:
  weight: 50

# Full rollout - promote canary to stable
image:
  tag: v1.3.0  # Now becomes stable
canary:
  enabled: false
```

### Deploy with Canary

```bash
# Enable canary with 20% traffic
helm upgrade --install apps ./charts/apps -n production \
  --set gateway-api.enabled=true \
  --set gateway-api.canary.enabled=true \
  --set gateway-api.canary.weight=20 \
  --set django.canary.enabled=true \
  --set django.canary.image.tag=v1.3.0 \
  --set django.canary.weight=20
```

### Verify

```bash
# Check pods
kubectl get pods -l track=stable
kubectl get pods -l track=canary

# Check HTTPRoute traffic splitting
kubectl get httproute django-app-route -n production -o yaml
```
