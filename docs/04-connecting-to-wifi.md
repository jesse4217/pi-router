# Step 4: Connecting to Wi-Fi

## Overview

In this step, we'll use the OpenWRT web interface (LuCI) to scan for available Wi-Fi networks and connect the router to an existing Wi-Fi network for internet access.

## Prerequisites

- Completed Steps 1-3
- Router accessible at `10.123.1.1`
- A Wi-Fi network to connect to (with password)

## Instructions

### 4.1 Access the Web Interface

1. Open a web browser on your computer
2. Navigate to: `http://10.123.1.1`
3. Enter your password (set in Step 2)
4. Click **Login**

### 4.2 Navigate to Wireless Settings

1. Click on the **Network** tab in the top menu
2. Click on **Wireless** from the dropdown

### 4.3 Scan for Available Networks

1. Find and click the **Scan** button
2. Wait for the scan to complete (5-10 seconds)
3. A list of available Wi-Fi networks will appear

### 4.4 Join a Network

1. Find your desired Wi-Fi network in the list
2. Click **Join Network** next to it

### 4.5 Configure Connection Settings

In the dialog that appears:

1. **Check the box**: "Replace wireless configuration"
2. Enter the **Wi-Fi password** for the network
3. Leave other settings as default
4. Click **Submit**

```
┌─────────────────────────────────────────────┐
│     Join Network                            │
├─────────────────────────────────────────────┤
│  Network: MyHomeWiFi                        │
│                                             │
│  ☑ Replace wireless configuration           │
│                                             │
│  WPA passphrase: ••••••••••••              │
│                                             │
│  [Submit]  [Cancel]                         │
└─────────────────────────────────────────────┘
```

### 4.6 Review and Apply Changes

1. You'll be taken to a configuration page
2. Leave all settings as default
3. Click **Save**
4. Look for **Unsaved Changes** notification at the top
5. Click it to see pending changes (these are UCI commands!)
6. Click **Save & Apply**

Wait a few seconds for the configuration to be applied.

### 4.7 Configure Firewall

To allow proper routing, we need to adjust firewall settings:

1. Go to **Network** → **Firewall**
2. Find the **WAN** zone
3. Change the **Input** option from "reject" to **Accept**
4. Click **Save & Apply**

### 4.8 Verify Internet Connection

Return to SSH terminal and test connectivity:

```bash
ssh root@10.123.1.1
```

Once connected:

```bash
ping -c 4 youtube.com
```

**Expected output:**

```
PING youtube.com (142.250.xxx.xxx): 56 data bytes
64 bytes from 142.250.xxx.xxx: seq=0 ttl=117 time=15.234 ms
64 bytes from 142.250.xxx.xxx: seq=1 ttl=117 time=14.567 ms
64 bytes from 142.250.xxx.xxx: seq=2 ttl=117 time=15.891 ms
64 bytes from 142.250.xxx.xxx: seq=3 ttl=117 time=14.234 ms

--- youtube.com ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
```

## Understanding the Configuration

When you click "Unsaved Changes," you'll see the UCI commands that were generated:

```bash
uci set wireless.@wifi-iface[0].ssid='YourNetworkName'
uci set wireless.@wifi-iface[0].encryption='psk2'
uci set wireless.@wifi-iface[0].key='YourPassword'
uci set wireless.@wifi-iface[0].network='wwan'
```

This shows how the web interface translates your actions into configuration commands.

## Network Status After This Step

```
Internet ←──→ Wi-Fi Router ←──→ Raspberry Pi ←──→ Your Laptop
              (Public WiFi)     (Our Router)      (Ethernet)
                                10.123.1.1
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No networks found | Move closer to Wi-Fi source; check if onboard Wi-Fi is enabled |
| Wrong password | Re-scan and rejoin the network with correct password |
| Connected but no internet | Check firewall settings; verify the source network has internet |
| Web interface won't load | Clear browser cache; try different browser |
| Changes won't apply | Click "Unsaved Changes" and then "Save & Apply" |

## Next Step

→ [Step 5: USB Wi-Fi Adapter Setup](./05-usb-wifi-adapter-setup.md)
