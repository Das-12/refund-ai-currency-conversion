#!/bin/bash
# Helper script to install Calico via Helm

# 1. Add the Calico helm repo
echo "Adding Calico Helm repository..."
helm repo add projectcalico https://docs.tigera.io/calico/charts
helm repo update

# 2. Create the tigera-operator namespace
echo "Creating tigera-operator namespace..."
kubectl create namespace tigera-operator --dry-run=client -o yaml | kubectl apply -f -

# 3. Install the Tigera Operator
echo "Installing Calico via Tigera Operator..."
helm install calico projectcalico/tigera-operator --version v3.31.3 -f values.yaml --namespace tigera-operator

echo "Calico installation initiated. Monitoring pods in calico-system..."
kubectl get pods -n calico-system -w
