# Dedicated Infrastructure Deployment Guide (Remote)

This guide provides the steps to deploy the core infrastructure components using the dedicated manifest files in `beta-infra/` and the automated CI/CD workflows for each service.

## Prerequisites
- `kubectl` configured with access to your remote cluster.
- Namespace `infra-beta` exists for infrastructure.
- Namespace `travoze` exists for microservices.

## Deployment Steps

### 1. Apply All Infrastructure Manifests
This command applies all core databases and messaging systems to the `infra-beta` namespace:
```bash
kubectl apply -R -f beta-infra/ -n infra-beta
```
*Note: This includes Postgres, NATS, Kafka, Redis, MongoDB, OpenSearch, Jaeger, and OTel Collector.*

### 2. Specialized Setup for APISix
If you are managing the API Gateway via Helm:
```bash
helm repo add apisix https://charts.apiseven.com
helm repo update
helm install apisix apisix/apisix \
  --namespace travoze \
  -f beta-infra/apisix/apisix-values.yaml
```

### 3. Install Cert-Manager (Required for TLS)
Before deploying services, you must install `cert-manager` to handle internal gRPC TLS certificates:

```bash
# 1. Install cert-manager CRDs and controllers
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml

# Wait a minute for the pods to start running in the cert-manager namespace
# kubectl get pods -n cert-manager

# 2. Apply the internal Certificate Authority
kubectl apply -f beta-infra/cert-manager/
```

### 4. Initialize the Databases
Since this is a fresh Postgres instance, you MUST create the databases manually for each service:

```bash
# Create the aggregator database
kubectl exec -it postgres-0 -n infra-beta -- psql -U postgres -c "CREATE DATABASE travoze_aggregator;"

# Create the booking database
kubectl exec -it postgres-0 -n infra-beta -- psql -U postgres -c "CREATE DATABASE travoze_booking;"

# Create the configuration database
kubectl exec -it postgres-0 -n infra-beta -- psql -U postgres -c "CREATE DATABASE travoze_configuration;"

# Create the notifications database
kubectl exec -it postgres-0 -n infra-beta -- psql -U postgres -c "CREATE DATABASE travoze_notifications;"

# Create the payment database
kubectl exec -it postgres-0 -n infra-beta -- psql -U postgres -c "CREATE DATABASE travoze_payments;"

# Create the logging database
kubectl exec -it postgres-0 -n infra-beta -- psql -U postgres -c "CREATE DATABASE logging_b2c;"

# Create the supplier database
kubectl exec -it postgres-0 -n infra-beta -- psql -U postgres -c "CREATE DATABASE travoze_supplier;"
```

### 4. Automated Service Deployment
Each service now follows the **Aggregator Pattern** with a standard `base` manifest and a `beta` kustomize overlay. Pushing to the `travoze_beta` branch triggers the deployment:

| Service | Repository | Deploy Command |
| --- | --- | --- |
| **Aggregator** | `aggregator` | `git push origin travoze_beta` |
| **Booking** | `booking` | `git push origin travoze_beta` |
| **Configuration**| `configuration` | `git push origin travoze_beta` |
| **Dashboard** | `fareos-dashboard` | `git push origin travoze_beta` |
| **Logging** | `fareos-logging` | `git push origin travoze_beta` |
| **Notifications**| `fareos-notifications`| `git push origin travoze_beta` |
| **Payment** | `payment` | `git push origin travoze_beta` |
| **Frontend** | `Unimoni-b2c-frontend` | `git push origin travoze_beta` |
| **Supplier** | `supplier` | `git push origin travoze_beta` |
| **Travel Portal** | `Travel-Impression-B2C-Portal` | `git push origin travoze_beta` |

### 5. Connection Details (Internal DNS)
Microservices in the `travoze` namespace connect to these internal endpoints in `infra-beta`:

| Component | Internal DNS Hostname |
| --- | --- |
| **Postgres** | `postgres.infra-beta.svc.cluster.local` |
| **NATS** | `nats-client.infra-beta.svc.cluster.local` |
| **Kafka** | `kafka-service.infra-beta.svc.cluster.local` |
| **Redis** | `redis-master.infra-beta.svc.cluster.local` |
| **MongoDB** | `mongodb.infra-beta.svc.cluster.local` |
| **OpenSearch** | `opensearch.infra-beta.svc.cluster.local` |
| **Jaeger** | `jaeger.travoze.svc.cluster.local` |

## Verification
To check if a service is healthy and connected:
```bash
# Check pod logs
kubectl logs -f deployment/<service-name> -n travoze

# Verify pod status
kubectl get pods -n travoze
```
