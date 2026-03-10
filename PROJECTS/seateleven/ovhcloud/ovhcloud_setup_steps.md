# Starting with Kubernetes on OVHcloud

You have two ways to start. One is "Easy & Managed" (Recommended), and the other is "Manual/DIY" (Like your Ubuntu server).

## Option A: Managed Kubernetes Service (Recommended)
In this option, OVH manages the **Master Node** for you. You don't have to install anything on it. You only manage the **Worker Nodes**.

### Step 1: Create the Cluster (The Master)
1.  Log in to your [OVHcloud Manager](https://manager.ca.ovhcloud.com/).
2.  Click **Public Cloud** in the top menu.
3.  In the left sidebar, under "Containers & Orchestration", click **Managed Kubernetes Service**.
4.  Click **Create a cluster**.
5.  **Configuration**:
    *   **Name**: Give it a name (e.g., `my-k8s-cluster`).
    *   **Version**: Select the latest stable Kubernetes version.
    *   **Region**: Pick one close to your users (e.g., Gravelines - FRA, Beauharnois - BHS).

### Step 2: Create a Node Pool (The Workers)
Once the cluster is creating, you need to add "Nodes" (the muscle):
1.  Select your new cluster.
2.  Go to the **Node Pools** tab and click **Add a node pool**.
3.  **Flavor**: Choose the server type (e.g., `B2-7` is a good starting point).
4.  **Size**: Select how many worker nodes you want (Minimum 3 is best for production, but 1 or 2 is fine for testing).
5.  **Billing**: Choose Hourly or Monthly.

### Step 3: Connect to it
1.  Once the cluster is `Ready`, go to the cluster dashboard in OVH.
2.  Download the **Kubeconfig** file.
3.  On your computer (where you have `kubectl` installed), point to this file:
    ```bash
    export KUBECONFIG=~/Downloads/kubeconfig_my-k8s.yaml
    kubectl get nodes
    ```
    *You will see your OVH worker nodes listed here!*

---

## Option B: DIY / Manual Installation (Like your Local Server)
If you want to do exactly what you did on your physical Ubuntu server:
1.  Go to **Public Cloud** -> **Instances**.
2.  Create 3 separate Ubuntu instances (1 for Master, 2 for Workers).
3.  **Networking**: Connect them all to the same **vRack** (Private Network) so they can see each other.
4.  **Install**: SSH into each one and run your `kubeadm`, `kubelet`, and `docker/containerd` commands manually.

### Comparison
| Feature | Managed (Option A) | DIY (Option B) |
| :--- | :--- | :--- |
| **Effort** | Low (Automatic) | High (Manual) |
| **Master Node Cost** | **Free** | You pay for the Instance |
| **Maintenance** | OVH updates the Master | You must update everything |
| **Reliability** | High Availability included | You have to set up HA yourself |

**My Recommendation**: Start with **Option A (Managed)**. It saves you the headache of managing the Master Node and the database (`etcd`), and since the Master node is free on OVH, it's actually cheaper!
