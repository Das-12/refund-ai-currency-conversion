# GitHub Action CI/CD Pattern

This pattern is used for building and deploying microservices (Frontend/Backend) to a Kubernetes cluster over SSH.

## Workflow Overview
1. **Trigger**: Push to `development` branch.
2. **Build & Push**: 
   - Builds Docker image using `Dockerfile`.
   - Tags with GitHub SHA and `latest`.
   - Pushes to GitHub Container Registry (GHCR).
3. **Deployment**:
   - Downloads image artifact.
   - Sets up SSH access (Port 2142).
   - Copies Kubernetes manifests to a temporary remote directory.
   - Applies ConfigMap, Secret, Service, and Ingress.
   - Updates the deployment image in the cluster.
   - Cleans up temporary files.

## Template (`deploy.yml`)

```yaml
name: Build & Deploy {{SERVICE_NAME}}
on:
  push:
    branches: [ "development" ]

permissions:
  contents: read
  packages: write

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${\{ github.repository_owner \}\}
          password: ${\{ secrets.GITHUB_TOKEN \}\}
      - name: Build & Push Docker Image
        run: |
          IMAGE_NAME="ghcr.io/${{ github.repository_owner }}/{{REPO_NAME}}"
          IMAGE_NAME=$(echo $IMAGE_NAME | tr '[:upper:]' '[:lower:]')
          IMAGE="${IMAGE_NAME}:${{ github.sha }}"
          
          docker build -f Dockerfile -t $IMAGE .
          docker push $IMAGE
          docker tag $IMAGE "${IMAGE_NAME}:latest"
          docker push "${IMAGE_NAME}:latest"
          
          echo $IMAGE > image_name.txt
      - name: Upload image name as artifact
        uses: actions/upload-artifact@v4
        with:
          name: image_name
          path: image_name.txt

  deploy:
    runs-on: ubuntu-latest
    needs: build_and_push
    env:
      DEPLOYMENT_NAME: {{DEPLOYMENT_NAME}}
      K8S_NAMESPACE: {{K8S_NAMESPACE}}
      REMOTE_TMP_DIR: /tmp/{{SERVICE_NAME}}-k8s
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Download image name artifact
        uses: actions/download-artifact@v4
        with:
          name: image_name
      - name: Read image name
        id: read_image
        run: |
          IMAGE=$(cat image_name.txt | xargs)
          echo "IMAGE=$IMAGE" >> $GITHUB_ENV
      - name: Install SSH Client
        run: |
          sudo apt-get update
          sudo apt-get install -y openssh-client
      - name: Setup SSH Key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" | base64 -d > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -p 2142 103.214.234.68 >> ~/.ssh/known_hosts
      - name: Copy Kubernetes manifests to server
        run: |
          ssh -p 2142 -i ~/.ssh/id_rsa deployer@103.214.234.68 "mkdir -p ${\{ env.REMOTE_TMP_DIR \}\}"
          scp -P 2142 -i ~/.ssh/id_rsa ./k8s/*.yaml deployer@103.214.234.68:${\{ env.REMOTE_TMP_DIR \}\}/
      - name: Apply ConfigMap & Secret
        run: |
          ssh -p 2142 -i ~/.ssh/id_rsa deployer@103.214.234.68 "kubectl apply -f ${\{ env.REMOTE_TMP_DIR \}\}/configmap.yaml"
          ssh -p 2142 -i ~/.ssh/id_rsa deployer@103.214.234.68 "kubectl apply -f ${\{ env.REMOTE_TMP_DIR \}\}/secret.yaml"
      - name: Apply Service & Deployment
        run: |
          ssh -p 2142 -i ~/.ssh/id_rsa deployer@103.214.234.68 "kubectl apply -f ${\{ env.REMOTE_TMP_DIR \}\}/service.yaml"
          ssh -p 2142 -i ~/.ssh/id_rsa deployer@103.214.234.68 "kubectl apply -f ${\{ env.REMOTE_TMP_DIR \}\}/deployment.yaml"
          ssh -p 2142 -i ~/.ssh/id_rsa deployer@103.214.234.68 "kubectl apply -f ${\{ env.REMOTE_TMP_DIR \}\}/ingress.yaml"
      - name: Update Deployment Image
        run: |
          ssh -p 2142 -i ~/.ssh/id_rsa deployer@103.214.234.68 "kubectl set image deployment/${{ env.DEPLOYMENT_NAME }} {{CONTAINER_NAME}}=${{ env.IMAGE }} -n ${{ env.K8S_NAMESPACE }}"
      - name: Cleanup
        run: |
          ssh -p 2142 -i ~/.ssh/id_rsa deployer@103.214.234.68 "rm -rf ${{ env.REMOTE_TMP_DIR }}"
```

## Required Secrets
- `GHCR_TOKEN`
- `SSH_PRIVATE_KEY`
