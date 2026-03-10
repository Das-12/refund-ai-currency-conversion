# OVHcloud Reference Notes

This document contains combined notes from previous conversations regarding OVHcloud infrastructure, specifically tailored for the `seateleven` projects (like Travoze).

## 1. Managed Kubernetes Service (MKS) Recommendations for Travoze

Based on current cluster metadata, the **travoze** suite requests approximately **6.4 vCPUs** and **9GB of RAM**. The previous 8-core node was running near its limit (290% CPU overcommit).

### Control Plane (Master Node)
*   **Cost:** Free/Included on the Standard Plan.
*   **Selection:** Use the **Standard Plan** (99.9% SLA, dedicated `etcd`) for production workloads.
*   The control plane is managed by OVHcloud, meaning no manual updates or API server management.

### Worker Nodes (Node Pool)
Recommended configurations to ensure High Availability (HA) and performance:
| Configuration | Flavors | Total Resources | Reasoning |
| :--- | :--- | :--- | :--- |
| **Option A: Balanced (Recommended)** | **3x b2-15** (4 vCPU / 15GB RAM) | 12 vCPU / 45GB RAM | Allows one node to fail while still handling baseline load. |
| **Option B: Performance** | **2x b2-30** (8 vCPU / 30GB RAM) | 16 vCPU / 60GB RAM | Fewer nodes, less granular scaling. Best for large pods. |
| **Option C: Cost Optimized** | **2x b2-15** (4 vCPU / 15GB RAM) | 8 vCPU / 30GB RAM | Minimum required. Running at ~80% capacity baseline. |

### Database Strategy (PostgreSQL & Redis)
Move from running databases in pods to **Managed Databases**.
*   **PostgreSQL:** Managed Database v15+ (Business or Enterprise plan for HA). Automated backups and patch management.
*   **Redis:** Managed Redis for guaranteed uptime for caching/sessions, offloading memory from K8s nodes.
*   *Crucial:* Attach them to the **vRack** so Kubernetes can talk to them privately.

### API Gateway (APISIX)
Run APISIX inside the Kubernetes cluster.
*   Use OVHcloud **Block Storage** as the StorageClass for `etcd` (the database APISIX uses).
*   Create a `Service` of type `LoadBalancer`. OVH will automatically provision a **Cloud Load Balancer** and assign a public IP.

## 2. OVHcloud General Kubernetes Deployment Guide

### Service Overview
*   **Managed Kubernetes Service (MKS):** CNCF-certified. Control plane is free (Standard plan). Supports autoscaling.
*   **Worker Nodes (Instances):**
    *   **B2/C2 (General Purpose):** Balanced CPU/RAM, gold standard for most web apps.
    *   **C2 (Compute Optimized):** High frequency for CPU-intensive tasks.
    *   **R2 (Memory Optimized):** For data-heavy applications or caching.
    *   Billed per instance.
*   **Storage Solutions:**
    *   **Block Storage (Cinder CSI):** For Persistent Volumes (PV). Billed per GB/month.
    *   **Object Storage (S3-Compatible):** For static assets/backups. Typically no charge for ingress/egress.
*   **Networking & Connectivity:**
    *   **vRack (Private Network):** Connects K8s nodes, Databases, etc., in a secure, isolated VLAN. **Free** with unlimited private bandwidth.
    *   **Load Balancer:** Routes external traffic to K8s services, handles SSL termination. Billed separately.

### Pricing Summary Model (Estimate)
| Service | Billed For | Typical Cost (Estimate) |
| :--- | :--- | :--- |
| **Kubernetes Master** | Free (Standard) | $0.00 |
| **Worker Nodes** | Per Instance (RAM/CPU) | ~$10 - $50+ /node/month |
| **Block Storage** | Per GB stored | ~$0.10 / GB / month |
| **Managed DB** | Instance + Storage | ~$20 - $100+ / month |
| **Load Balancer** | Per unit / Traffic | Base price per month |
| **vRack** | Service Usage | $0.00 |

### Recommended First Steps for New Setup:
1.  **Create a Public Cloud Project:** The foundation for all services.
2.  **Activate vRack:** Set up the private network first.
3.  **Deploy Managed Kubernetes:** Start with a small node pool and scale as needed.
