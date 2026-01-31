# Step 2: Initial SSH Setup

## Overview

In this step, we'll power on the Raspberry Pi, connect to it via Ethernet, and establish our first SSH connection to set up a secure password.

## Prerequisites

- Raspberry Pi 5 with OpenWRT SD card inserted (from Step 1)
- Ethernet cable
- USB Type-C power cable
- Computer with terminal/SSH client

## Instructions

### 2.1 Physical Connections

Connect everything in this order:

1. **Ethernet Cable**: Connect one end to the Raspberry Pi's Ethernet port, and the other end to your laptop/computer
2. **Power Cable**: Connect the USB Type-C power cable to the Raspberry Pi
3. Power on the Raspberry Pi

```
┌──────────────┐         ┌──────────────┐
│   Laptop     │─────────│  Raspberry   │
│              │ Ethernet│  Pi 5        │
└──────────────┘         └──────┬───────┘
                                │
                           USB-C Power
```

> **Note**: Wait approximately 30-60 seconds for the Pi to fully boot up.

### 2.2 Connect via SSH

1. Open a terminal on your computer

   - **macOS/Linux**: Use the built-in Terminal
   - **Windows**: Use PowerShell, Command Prompt, or PuTTY

2. Connect to the router using SSH:

```bash
ssh root@192.168.1.1
```

3. When prompted about the authenticity of the host, type `yes` and press Enter:

```
The authenticity of host '192.168.1.1' can't be established.
ED25519 key fingerprint is SHA256:xxxxx...
Are you sure you want to continue connecting (yes/no)? yes
```

4. You should now be logged in (no password required on first boot)

### 2.3 Set a Secure Password

**Important**: Setting a strong password is crucial for security!

1. Once logged in, you'll be prompted to set a password, or you can run:

```bash
passwd
```

2. Enter your new password when prompted
3. Confirm the password by entering it again

**Password Tips:**
- Use at least 12 characters
- Include uppercase, lowercase, numbers, and symbols
- Avoid common words or patterns
- Consider using a password manager

### 2.4 Verify the Connection

After setting the password, verify you're connected:

```bash
# Check the current IP configuration
ifconfig
```

You should see output showing the `br-lan` interface with IP `192.168.1.1`.

## Expected Output

```
BusyBox v1.36.1 (2024-xx-xx xx:xx:xx UTC) built-in shell (ash)

  _______                     ________        __
 |       |.-----.-----.-----.|  |  |  |.----.|  |_
 |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
 |_______||   __|_____|__|__||________||__|  |____|
          |__| W I R E L E S S   F R E E D O M
 -----------------------------------------------------
 OpenWrt xx.xx.x, r12345-xxxxx
 -----------------------------------------------------
root@OpenWrt:~#
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Wait longer for Pi to boot; check Ethernet cable |
| Network unreachable | Ensure your computer is set to DHCP or configure static IP in 192.168.1.x range |
| Permission denied | You may have already set a password; try the password |
| SSH command not found | Install OpenSSH or use PuTTY on Windows |

### Manual IP Configuration (if needed)

If your computer doesn't automatically get an IP, manually configure:

- **IP Address**: `192.168.1.2`
- **Subnet Mask**: `255.255.255.0`
- **Gateway**: `192.168.1.1`

## Security Note

The default OpenWRT installation has no password. Always set a strong password immediately after first login to prevent unauthorized access.

## Next Step

→ [Step 3: Network Configuration](./03-network-configuration.md)
