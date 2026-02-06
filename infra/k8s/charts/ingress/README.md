# Ingress Chart

Kubernetes Ingress resources for routing external traffic to services.

## Prerequisites

- NGINX Ingress Controller installed in your cluster
- cert-manager installed (if TLS is enabled)

## Installation

This chart is included as a dependency of the `apps` umbrella chart.

### Enable Ingress

Edit `infra/k8s/charts/apps/values.yaml`:

```yaml
gateway-api:
  enabled: false

ingress:
  enabled: true
  # ... configure your domain, etc.
```

Then deploy:

```bash
make helm-apply
```

### Switch back to Gateway API

Edit `infra/k8s/charts/apps/values.yaml`:

```yaml
gateway-api:
  enabled: true

ingress:
  enabled: false
```

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable Ingress resources | `false` |
| `ingress.className` | IngressClass name | `nginx` |
| `ingress.namespace` | Namespace for Ingress resources | `production` |
| `django.host` | Hostname for Django app | `django.example.com` |
| `static.host` | Hostname for static files | `django.example.com` |
| `tls.enabled` | Enable TLS | `true` |
| `tls.secretName` | TLS secret name | `django-tls` |

## TLS/SSL

TLS is enabled by default with cert-manager. Update the `clusterIssuer` annotation in values.yaml.
