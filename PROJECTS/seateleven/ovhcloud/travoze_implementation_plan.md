# OVHcloud Managed Kubernetes Recommendation for Travoze

Based on your current cluster metadata, the **travoze** suite is requesting approximately **6.4 vCPUs** and **9GB of RAM**. Your total CPU limits are overcommitted at **290% (23 vCPUs)**, which is normal for bursty workloads but suggests your current single 8-core node is running near its limit.

## Proposed Infrastructure

For a production-ready and scalable environment, I recommend moving to **OVHcloud Managed Kubernetes (MKS)**.

### 1. Control Plane (Master Node)
In OVH MKS, the control plane is managed by OVHcloud.
- **Cost:** Free/Included.
- **Selection:** Use the **Standard Plan** (99.9% SLA, dedicated `etcd`) instead of the Free plan for production workloads.
- **Benefit:** You don't have to manage the master node, updates, or API server availability; OVH does it for you.

---

### 2. Worker Nodes (The "Virtual Rack")
I recommend using a **Node Pool** with one of the following configurations to ensure High Availability (HA) and performance.

| Configuration | Flavors | Total Resources | Reasoning |
| :--- | :--- | :--- | :--- |
| **Option A: Balanced (Recommended)** | **3x b2-15** (4 vCPU / 15GB RAM) | 12 vCPU / 45GB RAM | Allows one node to fail while still having 8 vCPU to handle the ~6.4 vCPU baseline load. |
| **Option B: Performance** | **2x b2-30** (8 vCPU / 30GB RAM) | 16 vCPU / 60GB RAM | Fewer nodes to manage, but less granular scaling. Best if you have large pods. |
| **Option C: Cost Optimized** | **2x b2-15** (4 vCPU / 15GB RAM) | 8 vCPU / 30GB RAM | Minimum required. Running at ~80% capacity baseline. Low headroom for bursts. |

---

### 3. Database Strategy (PostgreSQL & Redis)
For production stability, I recommend **Managed Databases** instead of running them as pods.

| Component | Recommendation | Why? |
| :--- | :--- | :--- |
| **PostgreSQL** | **Managed Database v15+** | Automated backups, HA, and patch management. No PVC management needed. |
| **Redis** | **Managed Redis** | Guaranteed uptime for caching/sessions. Offloads memory from Kubernetes nodes. |

**Process:**
1. In the OVH Manager, go to **Public Cloud** > **Managed Databases**.
2. Select **PostgreSQL** and/or **Redis**.
3. **Plan:** Business or Enterprise (for HA).
4. **Networking:** Attach them to the **vRack** so Kubernetes can talk to them privately.

---

### 4. API Gateway (APISIX)
APISIX is high-performance and should run inside your Kubernetes cluster.

**Process:**
1. **Repository:** Add the APISIX Helm chart repository.
2. **Persistence:** Use OVHcloud **Block Storage** as the StorageClass for `etcd` (the database APISIX uses).
3. **Ingress:** Configure APISIX as your Ingress Controller.
4. **Public Access:** Create a `Service` of type `LoadBalancer`. OVH will automatically provision a **Cloud Load Balancer** and assign a public IP.

---

### 5. Networking (vRack Overview)
- **Deployment:** Connect your Managed Kubernetes cluster and Managed Databases to the **same vRack**.
- **Benefit:** Secure, private communication without public exposure.

## Summary of Benefits
1. **Zero-Management Control Plane:** No more SSH-ing into the master node for maintenance.
2. **Auto-scaling:** OVH MKS can automatically add more worker nodes if Travoze's load increases.
3. **Self-Healing:** If a worker node (flavor) fails, OVH automatically restarts it or replaces it.

## Verification Plan
Once we decide on the flavor:
1. Create the MKS cluster in the OVH Manager.
2. Download the new `kubeconfig`.
3. Verify node readiness: `kubectl get nodes`.
4. Deploy Travoze and check resource distribution: `kubectl describe nodes`.
