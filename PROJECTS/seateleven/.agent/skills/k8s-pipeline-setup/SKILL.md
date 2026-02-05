---
name: k8s-pipeline-setup
description: Setup Kubernetes manifests and Bitbucket Pipelines for a new microservice.
---

# Kubernetes & Bitbucket Pipeline Setup Skill

This skill guides you through creating the standard infrastructure configuration for a new service in the `seateleven` project.

## 1. Kubernetes Manifests
Create a `k8s/` directory in the service root.

### Files to Create:
1.  **`deployment.yaml`**
    -   **Pattern**: Copy from `aggregator-b2c` or `configuration-b2c`.
    -   **Key Changes**:
        -   `metadata.name` & `spec.selector.matchLabels.app`: Service Name (e.g., `my-service`).
        -   `image`: `ghcr.io/arshadm25/<service-name>:v1`.
        -   `containerPort`: Match the Dockerfile `EXPOSE` or `CMD` port.
        -   `envFrom.configMapRef.name`: `<service-name>-env`.

2.  **`service.yaml`**
    -   **Pattern**: Copy from `aggregator-b2c`.
    -   **Key Changes**:
        -   `metadata.name`: Service Name.
        -   `port` & `targetPort`: Match container port.
        -   **CRITICAL**: `nodePort`: Pick a UNIQUE port in range `30000-32767`. Check other services to avoid conflicts.
            -   `aggregator-b2c`: `30083`
            -   `tripjack`: `30086`
            -   `configuration-b2c`: `30087`

3.  **`configmap.yaml`**
    -   **Source**: Extract non-secret values from `.env`.
    -   **Format**: Key-value pairs under `data`.

4.  **`secret.yaml`**
    -   **Content**: Standard `ghcr-secret` for Docker registry access.
    -   **Note**: Usually identical across services.

## 2. Bitbucket Pipeline
Create `bitbucket-pipelines.yml` in the service root.

### Configuration:
-   **Image**: `docker:24.0.5`
-   **Variables**:
    -   `SSH_HOST`: `103.214.234.68`
    -   `SSH_PORT`: `2142`
    -   `K8S_NAMESPACE`: `seateleven`
-   **Steps**:
    1.  **Build**: Build & Push to GHCR. Use `export DOCKER_BUILDKIT=0`.
    2.  **Deploy**:
        -   SSH to server.
        -   Copy `k8s/*.yaml` to `/tmp/<service-name>-k8s`.
        -   `kubectl apply -f` the manifests.
        -   `kubectl set image` to update the deployment.
        -   `kubectl rollout status`.

## 3. Verification
-   Run `kubectl apply -f k8s/` locally to validate syntax.
-   Commit push to `development` to trigger pipeline.

## 3. GitHub Action (Alternative)
Create `.github/workflows/ci.yml` in the service root if using GitHub Actions.

### Configuration:
-   **Trigger**: Push to `main` or `development`.
-   **Secrets Required**: `GHCR_USER`, `GHCR_TOKEN`, `SSH_PRIVATE_KEY`.
-   **Workflow Structure**:
    1.  **Build & Push**:
        -   Build Docker image.
        -   **IMPORTANT**: If Dockerfile is not in root, use `-f deployments/docker/Dockerfile`.
        -   Push to GHCR.
        -   Save image name as artifact.
    2.  **Deploy**:
        -   Download image artifact.
        -   SSH to server (similar to Bitbucket Pipeline).
        -   Copy `k8s/*.yaml` to `/tmp/<service-name>-k8s`.
        -   Apply manifests.
        -   Set image on deployment.
        -   Wait for rollout.
