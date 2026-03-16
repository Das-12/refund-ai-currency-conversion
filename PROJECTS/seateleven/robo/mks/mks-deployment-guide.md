# OVHcloud Managed Kubernetes (MKS) Deployment Reference

This document serves as the official reference for deploying services to OVHcloud Managed Kubernetes (MKS) using GitHub Actions.

## Architecture Overview
Deployments bypass SSH intermediaries by communicating directly with the Kubernetes API using a cluster-specific `kubeconfig`.

## Required GitHub Secrets
Each repository must have the following secrets configured:

| Secret Name | Description | Used In |
|-------------|-------------|---------|
| `KUBE_CONFIG` | The full content of the OVHcloud MKS kubeconfig file. | Deployment |
| `GHCR_TOKEN` / `GHCR_PAT` | Personal Access Token with package permissions for GHCR. | Docker Build & Pull |
| `GHCR_SECRET` | Used specifically in the `booking` service for Docker builds and Pull secrets. | Docker Build & Pull |

> [!TIP]
> To remain resilient across different repositories, the workflows now use fallbacks: `${{ secrets.GHCR_TOKEN || secrets.GHCR_PAT || secrets.GITHUB_TOKEN }}`.

## Standard Workflow Template
The standard workflow for MKS deployment is triggered on the `travoze_beta` branch.

### Key Steps:
1.  **Build & Push**:
    *   Uses `docker/build-push-action@v5`.
    *   Authenticates with GHCR.
    *   Passes `GH_TOKEN` as a build secret for private Go modules.
2.  **Set Kubernetes Context**:
    *   Uses `azure/k8s-set-context@v3` with `KUBE_CONFIG`.
3.  **Apply Manifests**:
    *   Uses `kubectl kustomize` to render manifests.
    *   Applies image pull secrets (`ghcr-secret`).
    *   Updates the target deployment image with the latest commit SHA.

## Service Specifics

### 1. Authentication Service
- **Source**: `ovhloud_deploy/authentication`
- **Kustomize Path**: `deployments/kubernetes/overlays/staging/travoze/`
- **Secrets**: Uses `GHCR_TOKEN`.

### 2. Aggregator Service
- **Source**: `ovhloud_deploy/aggregator`
- **Kustomize Path**: `deployments/kubernetes/base/`
- **Containers**: Updates both `server` and `consumer` containers in a single pod.
- **Secrets**: Uses `GHCR_TOKEN`.

### 3. Booking Service
- **Source**: `ovhloud_deploy/booking`
- **Kustomize Path**: `deployments/kubernetes/overlays/beta/` (Clean base, no TLS)
- **Secrets**: Uses `GHCR_SECRET`.

### 4. Fareos Dashboard
- **Source**: `ovhloud_deploy/fareos-dashboard`
- **Manifests Path**: `k8s/` (Direct YAML apply)
- **Secrets**: Uses `GHCR_SECRET`.

## Common Troubleshooting
- **Build Fails (Repository not found)**: Ensure the `GH_TOKEN` secret name matches what is configured in the repository.
- **Push Fails (0 deltas)**: Ensure you have **committed** the changes locally before pushing.
- **Mismatched Remotes**: Use `git remote set-url --push origin <url>` if pushes go to the wrong repo.

---
*Created on 2026-03-10*
