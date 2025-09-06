## Prerequirements

1. `brew intall helm`
2. `brew install helmfile`
3. Install helm diff plugin `helm plugin install https://github.com/databus23/helm-diff`
4. Create secrets from `.env` file: `kubectl create secret generic app-secret --from-env-file=.env.prod -n production`
5. `cd infra/k8` and run `helmfile --file helmfile.yaml apply`
6. `minikube tunnel`
7. Set default namespace to production: `kubectl config set-context --current --namespace=production`

## Minikube

1. Install minikube: `brew install minikube`
2. Start minikube: `make minikube-start`

## Kube metrics

1. `cd infra/k8` install dependencies `helm dependency update`
2. `helm install kube-state-metrics .`
3. Forward port to acess metrics from local machine: `kubectl port-forward svc/kube-state-metrics 8085:8080 --address=0.0.0.0`

## ArgoCD

1. Install Helm chart: `helm install argo-cd charts/argo-cd/`
2. To access web UI: `kubectl port-forward svc/argo-cd-argocd-server 8089:443`
Visit `http://localhost:8089`
3. Username: `admin`.
Get password: `kubectl get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`
4. Apply manifest. From `infra/k8s/charts` directory run: `helm template root-app/ | kubectl apply -f -`
