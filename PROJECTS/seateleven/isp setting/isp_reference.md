# TP-Link ER605 Policy Routing Reference Notes

This document contains combined notes from previous conversations regarding the internet service provider (ISP) and policy routing configurations on the TP-Link ER605 Omada router for the `seateleven` network.

## The Working Principle of Policy Routing

Policy Routing forces a specific group of devices on the network to use a specific external internet connection (WAN). 

### Configuration Logic
The configuration is built in three layered steps:

**1. Defining the IP Range (IP Address)**
*   An **IP Address Range** (e.g., named `WiFi_Network_IPs`) is created.
*   *Purpose:* This defines the exact block of local network IPs that the rule will target (for example, `192.168.0.100` to `192.168.0.254`).

**2. Grouping the IPs (IP Group)**
*   An **IP Group** (e.g., named `Production_Servers`) is created.
*   *Purpose:* The previously defined IP Address Range is assigned to this group. This allows the router to apply larger policy rules to the whole block of addresses simultaneously.

**3. The Policy Routing Rule (Transmission -> Routing -> Policy Routing)**
*   A rule (e.g., `Force_WiFi_to_Normal_ISP`) is created:
    *   **Source IP:** Set to the IP Group (`Production_Servers`).
    *   **Destination IP:** Set to `IPGROUP_ANY` (applies regardless of the external website/server being accessed).
    *   **WAN:** Set to a specific WAN port (e.g., `WAN/LAN2`).
    *   **Mode:** Set to `Priority`.
*   *Purpose:* Whenever any device with an IP address within the defined range tries to access the internet, the router intercepts that traffic and forces it out through the specific WAN/LAN2 port. If `WAN/LAN2` goes offline, the `Priority` mode means those devices will likely fail over to the other configured WAN port. Devices entirely outside that chosen IP range are handled by default routing or active Load Balancing rules.

## Expanding the IP Range to the Entire Subnet (192.168.0.0 - .254)

It is technically possible to expand the policy routing IP Address Range to encompass the entire subnet (e.g., `192.168.0.2` to `192.168.0.254`).

### Consequences and Considerations
*   **Forcing All Traffic:** Expanding the range to cover everyone means the Policy Routing rule will catch **literally every device** on the network. All phones, computers, switches, APs, and servers will be forced to use the internet connection plugged into the target WAN port.
*   **Load Balancing Alternative:** If the sole goal is for all devices to use a specific WAN port primarily, standard Policy Routing is not explicitly required. It is usually cleaner to modify the **Load Balancing** settings (disabling the other WAN) or setting up Link Backup/Failover instead of writing a manual routing policy for the entire subnet.
*   **Sparing Devices:** If even a single device needs to use the other WAN port, the target IP range *must not* span from `.2` to `.254`. A gap must be left in the IP addresses assigned (e.g., `.2` to `.99`) so those exceptions can use the default WAN.
*   **The Router IP:** It is best practice to begin IP ranges at `192.168.0.2` instead of `192.168.0.0` or `192.168.0.1`. The `.1` address is standard for the ER605 Router itself; excluding it prevents the router from accidentally applying strict policy rules to its own internal system traffic.
