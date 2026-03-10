Version: 2.0.0
Overview
APISIX Ingress Controller is a Kubernetes ingress controller using Apache APISIX as the high performance reverse proxy.

APISIX Ingress Controller can be configured using the native Kubernetes Ingress or Gateway API, as well as with APISIX’s own declarative and easy-to-use custom resources. The controller translates these resources into APISIX configuration.

See the Getting Started tutorials to set up and start using the APISIX Ingress Controller.

Features#
To summarize, APISIX ingress controller has the following features:

Declarative configuration with CRDs.
Supports native Kubernetes Ingress v1 and Gateway API.
Supports service discovery through Kubernetes Service.
Supports load balancing based on pods (Upstream nodes).
Rich Plugins with custom Plugin support.
Get involved#
You can contribute to the development of APISIX ingress controller. See Development guide for instructions on setting up the project locally.

See the Contribute to APISIX section for details on the contributing flow.

Compatibility with APISIX#
The table below shows the compatibility between APISIX ingress controller and the APISIX proxy.

note
APISIX Ingress Controller 2.0.0+ support the APISIX Standalone API-driven Mode, but require APISIX 3.13+.

APISIX ingress controller	Supported APISIX versions	Recommended APISIX version
master	>=3.0	3.13
2.0.0	>=3.0	3.13
1.6.0	>= 2.15, >=3.0	2.15, 3.0
1.5.0	>= 2.7	2.15
1.4.0	>= 2.7	2.11
1.3.0	>= 2.7	2.10
1.2.0	>= 2.7	2.8
1.1.0	>= 2.7	2.7
1.1.0	>= 2.7	2.7
1.0.0	>= 2.7	2.7
0.6	>= 2.6	2.6
0.5	>= 2.4	2.5
0.4	>= 2.4	


Get APISIX and APISIX Ingress Controller
APISIX Ingress Controller is a Kubernetes ingress controller using Apache APISIX as the high performance reverse proxy.

APISIX Ingress Controller can be configured using the native Kubernetes Ingress or Gateway API, as well as with APISIX’s own declarative and easy-to-use custom resources. The controller translates these resources into APISIX configuration.

This tutorial series walks you through how to quickly get started with APISIX on a kind Kubernetes cluster and use the APISIX Ingress Controller to manage resources.

Prerequisites#
Install Docker as a dependency of kind.
Install kind to start a local Kubernetes cluster, or use any existing Kubernetes cluster (version 1.26+).
Install Helm (version 3.8+).
Install kubectl to run commands against Kubernetes clusters.
Create a Cluster and Configure Namespace#
In this section, you will be creating a kind cluster and configuring the namespace. Skip to the next section if you already have an existing cluster and a corresponding namspace.

Ensure you have Docker running and start a kind cluster:

kind create cluster
Create a new namespace ingress-apisix:

kubectl create namespace ingress-apisix
Set the namespace to ingress-apisix to avoid specifying it explicitly in each subsequent command:

kubectl config set-context --current --namespace=ingress-apisix
Install APISIX and APISIX Ingress Controller (Standalone API-driven mode)#
Install the Gateway API CRDs, APISIX Standalone API-driven mode, and APISIX Ingress Controller:

helm repo add apisix https://apache.github.io/apisix-helm-chart
helm repo update

helm install apisix \
  --namespace ingress-apisix \
  --create-namespace \
  --set apisix.deployment.role=traditional \
  --set apisix.deployment.role_traditional.config_provider=yaml \
  --set etcd.enabled=false \
  --set ingress-controller.enabled=true \
  --set ingress-controller.config.provider.type=apisix-standalone \
  --set ingress-controller.apisix.adminService.namespace=ingress-apisix \
  --set ingress-controller.gatewayProxy.createDefault=true \
  apisix/apisix
More details on the installation can be found in the Installation Guide.

Verify Installation#
Check the statuses of resources in the current namespace:

kubectl get all
You should wait for all pods to be running before proceeding:

NAME                                             READY   STATUS    RESTARTS   AGE
pod/apisix-7c5fb8d546-gtfqn                      1/1     Running   0          113s
pod/apisix-ingress-controller-56c46fd54f-f8fxt   1/1     Running   0          113s

NAME                             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/apisix-admin             ClusterIP   10.96.174.119   <none>        9180/TCP       113s
service/apisix-gateway           NodePort    10.96.231.33    <none>        80:31321/TCP   113s
service/apisix-metrics-service   ClusterIP   10.96.77.248    <none>        8443/TCP       113s

NAME                                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/apisix                      1/1     1            1           113s
deployment.apps/apisix-ingress-controller   1/1     1            1           113s

NAME                                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/apisix-7c5fb8d546                      1         1         1       113s
replicaset.apps/apisix-ingress-controller-56c46fd54f   1         1         1       113s
To verify the installed APISIX version, map port 80 of the apisix-gateway service to port 8080 on the local machine:

kubectl port-forward svc/apisix-gateway 9080:80 &
Send a request to the gateway:

curl -sI "http://127.0.0.1:9080" | grep Server
If everything is ok, you should see the APISIX version:

Server: APISIX/x.x.x
Edit this page


Version: 2.0.0
Install with Helm
Helm is a package manager for Kubernetes that automates the release and management of software on Kubernetes.

This document guides you through installing the APISIX ingress controller using Helm.

Prerequisites#
Before installing APISIX ingress controller, ensure you have:

A working Kubernetes cluster (version 1.26+)

Production: TKE, EKS, AKS, or other cloud-managed clusters
Development: minikube, kind, or k3s
Kubernetes 1.26+ is required because the controller uses CEL (Common Expression Language) validation rules in CRDs, IngressClass Namespaced Params support, and EndpointSlice terminating conditions.

kubectl installed and configured to access your cluster

Helm (version 3.8+) installed

Make sure to update the Helm repositories:

helm repo add apisix https://apache.github.io/apisix-helm-chart
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
Install APISIX and APISIX Ingress Controller#
The script below installs APISIX and APISIX Ingress Controller:

helm install apisix \
  --namespace ingress-apisix \
  --create-namespace \
  --set ingress-controller.enabled=true \
  --set ingress-controller.apisix.adminService.namespace=ingress-apisix \
  --set ingress-controller.gatewayProxy.createDefault=true \
  apisix/apisix
Install APISIX and APISIX Ingress Controller (Standalone API-driven mode)#
To run APISIX in APISIX Standalone API-driven mode, use the following script to install APISIX and the APISIX Ingress Controller:

helm install apisix \
  --namespace ingress-apisix \
  --create-namespace \
  --set apisix.deployment.role=traditional \
  --set apisix.deployment.role_traditional.config_provider=yaml \
  --set etcd.enabled=false \
  --set ingress-controller.enabled=true \
  --set ingress-controller.config.provider.type=apisix-standalone \
  --set ingress-controller.apisix.adminService.namespace=ingress-apisix \
  --set ingress-controller.gatewayProxy.createDefault=true \
  apisix/apisix
Install APISIX Ingress Controller#
The script below installs APISIX Ingress Controller:

# Set the access address and adminkey for apisix
helm install apisix-ingress-controller \
  --create-namespace \
  -n ingress-apisix \
  --set gatewayProxy.createDefault=true \
  --set gatewayProxy.provider.controlPlane.auth.adminKey.value=edd1c9f034335f136f87ad84b625c8f1 \
  --set apisix.adminService.namespace=apisix-ingress \
  --set apisix.adminService.name=apisix-admin \
  --set apisix.adminService.port=9180 \
  apisix/apisix-ingress-controller