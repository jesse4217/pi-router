# Step 11: Wireless Troubleshooting

## Overview

This guide covers diagnosing and fixing common wireless issues on OpenWrt with Raspberry Pi 4, particularly when the Access Point isn't working or USB WiFi adapters aren't recognized.

## Prerequisites

- SSH access to the router
- Basic understanding of OpenWrt configuration

## Common Issues

### Issue: AP Not Broadcasting / "Generic Unknown" Radio

**Symptoms:**
- LuCI shows "Generic unknown" for radio1
- Wireless interface shows "disabled"
- No SSID visible to connect to

**Root Cause:**
The USB WiFi adapter's radio is disabled in configuration, or driver/firmware issues.

## Diagnostic Commands

### 1. Check Wireless Configuration

```bash
uci show wireless
```

**Key things to look for:**
- `wireless.radio1.disabled='1'` - Radio is disabled
- `wireless.default_radio1.device='radio1'` - AP interface assignment
- `wireless.default_radio1.encryption='none'` - No encryption set

### 2. Check Wireless Status

```bash
wifi status
```

Shows JSON output of current wireless state including if interfaces are active.

### 3. Check Active Interfaces

```bash
iwinfo
```

**Example healthy output:**
```
phy0-sta0 ESSID: "Buffalo-G-1670"
          Mode: Client  Channel: 11 (2.462 GHz)
          Hardware: [Cypress CYW43455]

phy1-ap0  ESSID: "OpenWrt"
          Mode: Master  Channel: 36 (5.180 GHz)
          Hardware: USB 0BDA:C811 [Generic MAC80211]
```

### 4. Check USB Device Detection

```bash
lsusb
```

**Example output:**
```
Bus 001 Device 004: ID 0bda:c811 Realtek 802.11ac NIC
```

### 5. Check Driver Loading

```bash
# Check loaded modules
lsmod | grep rtl
lsmod | grep rtw

# Check kernel messages for driver
dmesg | grep -i rtw
dmesg | grep -i rtl
```

**Successful driver load:**
```
[    8.347497] usbcore: registered new interface driver rtw_8821cu
[  214.306098] rtw_8821cu 1-1.2:1.0: Firmware version 24.11.0, H2C version 12
```

### 6. Check for Firmware Issues

```bash
dmesg | grep -i firmware
```

Look for "failed" or "error" messages indicating missing firmware.

### 7. Check PHY Devices

```bash
ls /sys/class/ieee80211/
iw dev
```

## The Fix

### Step 1: Enable the Disabled Radio

```bash
uci set wireless.radio1.disabled='0'
uci commit wireless
```

### Step 2: Set Up Encryption (Important!)

```bash
uci set wireless.default_radio1.encryption='psk2'
uci set wireless.default_radio1.key='YourSecurePassword'
uci commit wireless
```

### Step 3: Reload Wireless

```bash
wifi reload
```

### Step 4: Verify AP is Running

```bash
iwinfo
iw dev
```

**Expected output:**
```
phy#1
    Interface phy1-ap0
        ssid OpenWrt
        type AP
        channel 36 (5180 MHz), width: 80 MHz
```

## Pi4 Built-in WiFi Limitation

**Important:** The Raspberry Pi 4's built-in Cypress CYW43455 WiFi does **NOT** support VAPs (Virtual Access Points).

```bash
iwinfo
# Shows: Supports VAPs: no
```

**What this means:**
- You cannot run AP + Client mode simultaneously on radio0
- You MUST use a USB WiFi adapter for the Access Point
- The built-in WiFi should be used only for the WAN uplink (client mode)

## USB WiFi Adapter Drivers

### RTL8811CU (0bda:c811)

This chip uses the `rtw88` driver series:

```bash
# Check if driver loaded
lsmod | grep rtw88

# Should see:
# rtw88_8821cu
# rtw88_usb
# rtw88_core
```

### Common Realtek Drivers

| USB ID | Chipset | Driver Package |
|--------|---------|----------------|
| 0bda:c811 | RTL8811CU | rtw88 (built-in) |
| 0bda:8812 | RTL8812AU | `kmod-rtl8812au-ct` |
| 0bda:8179 | RTL8188EU | `kmod-rtl8xxxu` |
| 0bda:b812 | RTL8812BU | `kmod-rtl88x2bu` |

### Installing Drivers

```bash
opkg update
opkg list | grep kmod-rtl
opkg install kmod-rtl8812au-ct  # Example
```

## Quick Diagnostic Script

Run this to get all relevant info at once:

```bash
echo "=== Wireless Config ===" && uci show wireless
echo ""
echo "=== Active Interfaces ===" && iwinfo
echo ""
echo "=== USB Devices ===" && lsusb
echo ""
echo "=== Driver Status ===" && dmesg | grep -i -E "rtw|rtl|firmware" | tail -10
echo ""
echo "=== PHY Devices ===" && ls /sys/class/ieee80211/
```

## Troubleshooting Checklist

| Check | Command | What to Look For |
|-------|---------|------------------|
| Radio enabled | `uci show wireless \| grep disabled` | Should be `'0'` |
| Driver loaded | `dmesg \| grep -i rtw` | "Firmware version" message |
| USB detected | `lsusb` | Your adapter's USB ID |
| Interface up | `iwinfo` | `phy1-ap0` with `Mode: Master` |
| Firmware OK | `dmesg \| grep -i firmware` | No "failed" messages |

## Network Zones

Ensure proper zone assignment:

```bash
uci show network | grep interface
uci show firewall | grep -E "zone|network"
```

- Client interface (wwan) → WAN zone
- AP interface (lan) → LAN zone

## Summary of Our Fix

1. **Diagnosed** using `uci show wireless` and `iwinfo`
2. **Found** radio1 was disabled (`disabled='1'`)
3. **Verified** driver was loaded and firmware working via `dmesg`
4. **Enabled** radio1: `uci set wireless.radio1.disabled='0'`
5. **Set** WPA2 encryption for security
6. **Applied** changes: `uci commit wireless && wifi reload`
7. **Verified** AP running with `iwinfo` showing `phy1-ap0` in Master mode

## Related Documentation

- [Step 5: USB Wi-Fi Adapter Setup](./05-usb-wifi-adapter-setup.md)
- [Step 6: Access Point Configuration](./06-access-point-configuration.md)
