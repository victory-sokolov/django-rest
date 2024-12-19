# Djangolog application

- Run makefile commands in the Docker container
```bash
export RUN_IN_DOCKER=true
make test
```


## Install dependencies

```bash
uv init
uv pip install
# Install npm dependencies
npm install
```

## Start project

1. Create local certs to use server over HTTPS: `mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1`. Put generated files into `certs` directory
2. Start Docker and run `docker-compose up -d` from `docker` directory. Run local version of docker-compose: `docker-compose -f docker-compose.yml -f docker-compose.local.yml up`
3. Start Celery worker `make worker`
4. Start Django app `uv run python manage.py runserver` or `make dev`.
5. Visit `https://localhost:8000/`

## Create superuser

Creates superuser with the following credentials

email: admin@gmail.com
password: superPassword12

```bash
make create-superuser
```

## Populate post table with some random data

`DJANGO_ENV=local uv run python manage.py shell`

```python
from djangoblog.factory import AccountFactory
AccountFactory.create_batch(50)
```

## Swagger Docs

API documentation is available at: `/api/docs`

## Load testing

For load testing we are using Locust
`uv run locust -f locustfile.py --host=http://localhost:9020`



Run with entr to reload on changes
Install: `brew install entr`
Run: `ls locustfile.py |entr -r uv run locust -f locustfile.py --host=http://localhost:9020`

## Launch Debugger

- `docker-compose -f docker-compose.yml -f docker-compose.debug.yml up`


## Run with minikube

1. `kubectl create secret generic app-secret --from-env-file=.env`

## Terraform

1. `terraform apply --parallelism=20 -auto-approve`
2. Create secret from file: `kubectl create secret generic google-credentials --from-file=infra/terraform/gcp-creds.json -n default`
3. Create secrets from `.env` file: `kubectl create secret generic app --from-env-file=<(env -i sh -c "set -a; . .env; printenv | grep -v '^PWD='")`
4. Apply kubernetes config `kubernetes apply -f infra/k8`


## ArgoCD

1. Install Helm Chart
```bash
helm repo add argo-cd https://argoproj.github.io/argo-helm
helm dep update charts/argo-cd/
```
2. Install Helm chart: `helm install argo-cd charts/argo-cd/`
3. To access web UI: `kubectl port-forward svc/argo-cd-argocd-server 8089:443`
Visit `http://localhost:8089`
4. Username: `admin`.
Get password: `kubectl get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`
5. Apply manifest. From `infra/k8s/charts` directory run: `helm template root-app/ | kubectl apply -f -`

# Install Kibana and Elasticsearch

1. Clone repo https://github.com/deviantony/docker-elk
2. `docker compose up setup`
3. `docker compose up`
4. Open Kibana: `http://localhost:5601/`
5. Credentials:
  - username: `elastic`
  - password: `changeme`
