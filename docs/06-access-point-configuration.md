# Step 6: Access Point Configuration

## Overview

In this step, we'll enable the USB Wi-Fi adapter as an access point and configure a custom SSID and password for your private network.

## Prerequisites

- Completed Steps 1-5
- USB Wi-Fi adapter detected and driver installed
- SSH access to the router

## Instructions

### 6.1 Navigate to Wireless Configuration

```bash
cd /etc/config
```

### 6.2 Edit the Wireless Configuration File

Open the wireless configuration file:

```bash
vi wireless
```

### 6.3 Enable the Second Radio Interface

Look for the `radio1` section (this is your USB adapter). Find the line:

```
option disabled '1'
```

Change it to:

```
option disabled '0'
```

### 6.4 Vi Editor Quick Reference

| Command | Action |
|---------|--------|
| `i` | Enter insert mode (to edit) |
| `Esc` | Exit insert mode |
| `:w` | Save (write) the file |
| `:q` | Quit |
| `:wq` | Save and quit |
| `dd` | Delete current line |
| `/text` | Search for "text" |

### 6.5 Save and Exit

1. Press `Esc` to exit insert mode
2. Type `:w` and press Enter to save
3. Type `:q` and press Enter to quit

### 6.6 Reload Wireless Configuration

Apply the wireless configuration:

```bash
wifi
```

### 6.7 Verify New Interface

Check that both interfaces are now active:

```bash
iw dev
```

**Expected output:**

```
phy#0
    Interface wlan0
        ifindex 8
        wdev 0x1
        addr xx:xx:xx:xx:xx:xx
        type managed
        
phy#1
    Interface wlan1
        ifindex 9
        wdev 0x100000001
        addr yy:yy:yy:yy:yy:yy
        type AP
```

The `type AP` indicates the interface is configured as an Access Point.

### 6.8 Customize the SSID

Edit the wireless configuration again:

```bash
vi /etc/config/wireless
```

Find the `wifi-iface` section associated with `radio1` and change:

```
option ssid 'OpenWrt'
```

To your custom name:

```
option ssid 'RaspiRouter'
```

### 6.9 Set a Wi-Fi Password

In the same `wifi-iface` section, add these lines:

```
option encryption 'psk2'
option key 'YourSecurePassword123'
```

**Complete wifi-iface example:**

```
config wifi-iface 'default_radio1'
    option device 'radio1'
    option network 'lan'
    option mode 'ap'
    option ssid 'RaspiRouter'
    option encryption 'psk2'
    option key 'YourSecurePassword123'
```

### 6.10 Save and Apply

1. Save the file (`:wq`)
2. Reload wireless:

```bash
wifi
```

### 6.11 Verify the Access Point

On your phone or another device:

1. Open Wi-Fi settings
2. Look for your custom SSID (e.g., "RaspiRouter")
3. Connect using the password you set
4. Verify you can access the internet

## Configuration via UCI Commands (Alternative)

If you prefer command-line configuration:

```bash
# Set custom SSID
uci set wireless.default_radio1.ssid='RaspiRouter'

# Set encryption type
uci set wireless.default_radio1.encryption='psk2'

# Set password
uci set wireless.default_radio1.key='YourSecurePassword123'

# Save changes
uci commit wireless

# Apply changes
wifi
```

## Understanding the Configuration

```
┌─────────────────────────────────────────────────────┐
│  Wireless Configuration                             │
├─────────────────────────────────────────────────────┤
│  radio0 (onboard) - Connects to external Wi-Fi     │
│    └── wlan0 - Client mode (WWAN)                  │
│                                                     │
│  radio1 (USB adapter) - Your private network       │
│    └── wlan1 - Access Point mode (LAN)             │
│         └── SSID: RaspiRouter                      │
│         └── Encryption: WPA2-PSK                   │
└─────────────────────────────────────────────────────┘
```

## Security Recommendations

1. **Use WPA2 or WPA3**: Never use WEP or open networks
2. **Strong Password**: At least 12 characters with mixed case, numbers, symbols
3. **Unique SSID**: Avoid default or common names
4. **Hide SSID** (optional): Add `option hidden '1'` to hide your network

### Optional: Hide Your Network

```bash
uci set wireless.default_radio1.hidden='1'
uci commit wireless
wifi
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| SSID doesn't appear | Run `wifi` command; check if radio is disabled |
| Can't connect | Verify password; check encryption type matches |
| Connected but no internet | Check that interface is bridged to `lan` network |
| Slow speeds | Try different Wi-Fi channel; check for interference |

### Reset Wireless Configuration

If things go wrong:

```bash
# Remove all wireless config
rm /etc/config/wireless

# Regenerate default config
wifi config

# Edit and reconfigure
vi /etc/config/wireless
```

## Network Topology After This Step

```
                                    ┌─────────────────┐
                                    │  Your Phone     │
Internet ←→ Public ←→ Raspberry Pi ←┤                 │
             WiFi     Travel Router │  Your Laptop    │
           (wlan0)    ┌─────────┐   │                 │
                      │ wlan1   │   │  Other Devices  │
                      │ (AP)    │   └─────────────────┘
                      │RaspiRouter
                      └─────────┘
```

## Next Step

→ [Step 7: Auto-Start Script](./07-auto-start-script.md)
