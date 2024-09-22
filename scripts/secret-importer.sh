#!/bin/bash

# Make sure you have the necessary permissions and gcloud SDK installed
# Also, ensure you have authenticated with gcloud

# Set the name of the Kubernetes secret
K8S_SECRET_NAME="djapp"

# Get the secret data from Kubernetes
kubectl get secret $K8S_SECRET_NAME -o json | jq -r '.data | map_values(@base64d) | to_entries | .[] | "\(.key)=\(.value)"' > secrets.txt

# Read the secrets and import them to Google Cloud Secret Manager
while IFS='=' read -r key value; do
    # Create or update the secret in Secret Manager
    echo "Creating secret: $key"
    echo -n "$value" | gcloud secrets create "$key" --data-file=-
done < secrets.txt

rm secrets.txt
