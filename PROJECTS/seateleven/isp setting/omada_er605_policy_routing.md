# FINAL SETUP: API-Specific Static IP Routing

Follow these steps exactly in your portal at `https://192.168.0.1:1025`. This setup ensures your Wi-Fi users browse the web normally but use the Static IP ONLY when connecting to your provider's API.

---

### Step 1: Add the API Provider's IP Address
1. Go to **Preferences** -> **IP Group**.
2. Click the **IP Address** tab and click **Add**.
   - **Name**: `API_Provider_IP`
   - **IP Address Type**: IP Address Range
   - **Start IP - End IP**: Type `20.207.120.18` - `20.207.120.18`
   - Click **OK**.

### Step 2: Create the API Destination Group
1. Switch to the **IP Group** tab and click **Add**.
   - **Group Name**: `API_Destination_Group`
   - **Select IP Addresses**: Check the box for `API_Provider_IP`.
   - Click **OK**.

### Step 3: Create the Routing Rule
1. Go to **Transmission** -> **Routing** -> **Policy Routing**.
2. Click **Add**. Fill it out exactly like this:
   - **Policy Name**: `Force_API_to_Static`
   - **Service Type**: `ALL`
   - **Source IP**: `IPGROUP_ANY` (This means all your Wi-Fi devices)
   - **Destination IP**: Select your **`API_Destination_Group`**
   - **WAN Port**: Select whichever port is your **Static ISP** (WAN or WAN2).
   - **Status**: Check "Enable"
   - Click **OK**.

### Step 4: Verification
- Open your browser and go to `whatismyip.com`. It should show your **Normal ISP IP**.
- Run your API test application. It should now connect successfully because the router will recognize the API's address and shift that traffic to the Static IP port.
