# Step 5: USB Wi-Fi Adapter Setup

## Overview

In this step, we'll install the necessary packages and drivers to make the USB Wi-Fi adapter work with the Raspberry Pi. This adapter will serve as our access point for client devices.

## Prerequisites

- Completed Steps 1-4
- Router connected to internet
- USB Wi-Fi adapter ready
- SSH access to the router

## Instructions

### 5.1 Update Package Lists

First, update the package repository:

```bash
opkg update
```

Wait for the update to complete.

### 5.2 Install USB Utilities

Install USB-related tools:

```bash
opkg install usbutils
```

### 5.3 Check USB Devices (Before Inserting Adapter)

List current USB devices:

```bash
lsusb
```

**Example output:**

```
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
```

### 5.4 Insert USB Wi-Fi Adapter

1. Insert your USB Wi-Fi adapter into one of the Raspberry Pi's USB ports
2. Wait a few seconds for detection

### 5.5 Verify Adapter Detection

Run `lsusb` again:

```bash
lsusb
```

You should see a new device. For example:

```
Bus 001 Device 002: ID 0bda:xxxx Realtek Semiconductor Corp. ...
```

> **Note**: The exact ID will depend on your adapter model.

### 5.6 Install USB Mode Switch

Some adapters start in "disk mode" and need to be switched to network mode:

```bash
opkg install usb-modeswitch
```

After installation, the adapter should automatically switch modes. Verify with:

```bash
lsusb
```

The device description should change from something like "Mass Storage" to "Network Interface Controller" or similar.

### 5.7 Install Wi-Fi Adapter Driver

The driver needed depends on your adapter's chipset. For Realtek adapters (common):

```bash
opkg install kmod-rtl8xxxu rtl8192cu-firmware
```

> **Important**: The exact package names may vary depending on your adapter model. Common alternatives include:
> - `kmod-rtl8192cu` - For RTL8188CUS/RTL8192CU chipsets
> - `kmod-rt2800-usb` - For Ralink chipsets
> - `kmod-mt76x0u` - For MediaTek chipsets

### 5.8 Load the Driver

Load the driver module:

```bash
modprobe rtl8xxxu
```

> **Note**: Replace `rtl8xxxu` with the appropriate driver name for your adapter.

### 5.9 Check Wireless Interfaces

Check if the new interface is recognized:

```bash
iw dev
```

**At this point, you may only see one interface** - this is normal. We'll configure the second interface in the next steps.

### 5.10 Alternative Check

```bash
ip link show
```

Look for a new wireless interface (e.g., `wlan1`).

## Finding the Right Driver

If the above driver doesn't work, identify your adapter:

```bash
lsusb -v | grep -i wireless
```

Or check the USB ID:

```bash
lsusb
# Note the ID (e.g., 0bda:8179)
```

Then search online for "OpenWRT [USB ID] driver" to find the correct package.

## Common USB Wi-Fi Adapter Drivers

| Chipset | Package |
|---------|---------|
| Realtek RTL8188CUS | `kmod-rtl8192cu` |
| Realtek RTL8812AU | `kmod-rtl8812au-ct` |
| Realtek RTL8188EU | `kmod-rtl8xxxu` |
| Ralink RT5370 | `kmod-rt2800-usb` |
| MediaTek MT7601U | `kmod-mt7601u` |
| Atheros AR9271 | `kmod-ath9k-htc` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Adapter not detected | Try different USB port; some ports have power limitations |
| Driver won't install | Run `opkg update` again; check available packages with `opkg list | grep kmod` |
| Module won't load | Check for errors with `dmesg | tail -20` |
| Still in disk mode | Unplug, wait 5 seconds, replug; ensure usb-modeswitch is installed |

### Check Kernel Messages

For detailed debugging information:

```bash
dmesg | tail -50
```

Look for messages about USB devices and wireless interfaces.

### List Available Wireless Packages

```bash
opkg list | grep -E "kmod-.*wireless|kmod-rtl|kmod-rt2|kmod-mt7"
```

## Hardware Compatibility Note

Not all USB Wi-Fi adapters are compatible with OpenWRT. Before purchasing, check the OpenWRT hardware compatibility list or look for adapters specifically marketed as Linux-compatible.

## Verified Working Adapters

Some adapters known to work well:
- TP-Link TL-WN722N (v1 only)
- Alfa AWUS036ACH
- Panda PAU05
- Edimax EW-7811Un

## Next Step

→ [Step 6: Access Point Configuration](./06-access-point-configuration.md)
