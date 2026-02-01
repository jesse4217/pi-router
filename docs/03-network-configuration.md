# Step 3: Network Configuration

## Overview

In this step, we'll change the default IP address for better security and configure a new wireless interface for WAN connectivity.

## Prerequisites

- Completed Steps 1-2
- SSH connection to the router established

## Instructions

### 3.1 Navigate to Configuration Directory

First, navigate to the network configuration directory:

```bash
cd /etc/config
```

### 3.2 View Current Network Configuration

Examine the current network settings:

```bash
vi network
```

Press `Esc` then `:q` to exit the viewer without making changes.

> **Note**: The default IP address is `192.168.1.1`. We'll change this for better security.

### 3.3 Change the LAN IP Address

Use UCI (Unified Configuration Interface) commands to change the IP address:

```bash
uci set network.lan.ipaddr='10.123.1.1'
```

Save the changes:

```bash
uci commit network
```

### 3.4 Configure Wireless WAN Interface

Create a new wireless interface for connecting to external Wi-Fi networks:

```bash
# Create the WWAN interface
uci set network.wwan=interface

# Set protocol to DHCP (for dynamic IP assignment)
uci set network.wwan.proto='dhcp'

# Configure DNS servers (Cloudflare and Google)
uci set network.wwan.dns='1.1.1.1 8.8.8.8'

# Save all changes
uci commit network
```

### 3.5 Reboot to Apply Changes

Reboot the router to apply all configuration changes:

```bash
reboot
```

Wait approximately 60 seconds for the router to restart.

### 3.6 Reconnect with New IP Address

After reboot, try connecting with the old IP (it should fail):

```bash
ssh root@192.168.1.1
# This should fail - confirming our new IP is working
```

Now connect with the new IP address:

```bash
ssh root@10.123.1.1
```

Type `yes` when prompted and enter your password.

### 3.7 Verify New Configuration

Once connected, verify the new IP address:

```bash
ifconfig
```

You should see the new IP address `10.123.1.1` in the output.

## Configuration Summary

| Setting | Value |
|---------|-------|
| New LAN IP | `10.123.1.1` |
| WWAN Protocol | DHCP |
| DNS Servers | 1.1.1.1, 8.8.8.8 |

## Testing Internet Connectivity

At this point, the router is NOT connected to the internet yet. Verify this:

```bash
ping youtube.com
```

You should see no response (100% packet loss). This is expected - we'll fix this in the next step.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cannot SSH to new IP | Your computer may need a new IP. Reconnect Ethernet and let DHCP assign |
| UCI command not found | Ensure you're logged into OpenWRT, not your local machine |
| Changes not applied | Make sure you ran `uci commit` before rebooting |
| Old IP still works | Reboot didn't complete; try `reboot` again |

### Reset to Default (Emergency)

If you lose access completely, you may need to reflash the SD card and start over, or access via serial console if available.

## Network Diagram After This Step

```
┌─────────────────────────────────────────────────┐
│           Raspberry Pi Router                   │
│                                                 │
│   br-lan: 10.123.1.1                           │
│   └── Ethernet (to laptop)                     │
│                                                 │
│   wwan: Not connected yet                      │
│   └── Will connect to external Wi-Fi           │
└─────────────────────────────────────────────────┘
```

## Next Step

→ [Step 4: Connecting to Wi-Fi](./04-connecting-to-wifi.md)
