# Eva-Chat K8s and Pipeline Setup: Session Summary

This document stores the configuration patterns and troubleshooting steps identified during the setup of Eva-Chat backend and frontend.

## 1. Project Structure
Standardized on a **flat folders** approach within each repository:
- `eva_chat/` (Backend): Contains `k8s/` folder with Deployment, Service, ConfigMap, Secret, and Ingress.
- `evachat_frontend/` (Frontend): Contains `k8s/` folder with Deployment, Service, and Ingress.

## 2. Infrastructure Highlights

### Backend (eva_chat)
- **Database**: Connected to a dedicated `postgres-vector` instance in the `infra` namespace.
- **Port**: Standardized on internal port **8080**.
- **Ingress**: Uses path-based routing at `/api/evachat`. Uses `rewrite-target: /$2` to strip the prefix before sending to the backend.

### Frontend (evachat_frontend)
- **Container**: Nginx-based, listening on port **3055** (as per `nginx.conf`).
- **Build Args**: Uses `REACT_APP_API_URL` during Docker build to point the React app to the backend ingress URL (`https://evalicense.ecogo.ai/api/evachat`).
- **Health Check**: Uses `/health` (defined in Nginx) for K8s probes.

## 3. Critical Troubleshooting & Lessons Learned

### Next.js / React Router Probes
- **Issue**: Pods entered `CrashLoopBackOff` even though logs said "Ready".
- **Cause**: Liveness/Readiness probes were hitting `/`. In this app structure, `/` returned a **404**, causing K8s to restart the pod.
- **Fix**: Update probes to hit a valid 200 path (e.g., `/login` or a dedicated `/health` endpoint).

### Bitbucket Pipelines Docker Build
- **Issue**: `authorization denied by plugin pipelines: --privileged=true is not allowed`.
- **Cause**: Standard Bitbucket Runners do not support privileged mode. BuildKit cache mounts (`RUN --mount=type=cache`) require this mode.
- **Fix**: Remove `--mount=type=cache` from `Dockerfile.production` and use standard `COPY` + `go mod download`.

### Ingress Rewrite Target
- **Format**: Always ensure the `rewrite-target` annotation is paired with matching regex in the path:
  - Path: `/api/evachat(/|$)(.*)`
  - Rewrite: `/$2`

## 4. Manual Verification Commands (on Server)
```bash
# Verify pods and probes
kubectl get pods -n evachat-bot

# Check ingress status
kubectl describe ingress evachat-ingress -n evachat-bot

# View logs for startup validation
kubectl logs -f deployment/evachat-api -n evachat-bot
```
