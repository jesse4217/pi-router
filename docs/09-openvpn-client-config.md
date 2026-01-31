# Step 9: OpenVPN Client Configuration

## Overview

In this final step, we'll initialize the OpenVPN server, generate client profiles, install the OpenVPN client on our router, and connect everything together to create a fully secure travel router.

## Prerequisites

- Completed Steps 1-8
- EC2 instance running
- SSH key file saved locally
- Router connected to internet

## Part A: Initialize OpenVPN Server

### 9.1 Connect to EC2 Instance

1. Open a terminal on your local computer
2. Navigate to where you saved the key file:

```bash
cd ~/Downloads  # or wherever you saved the key
```

3. Set correct permissions on the key file:

```bash
chmod 400 router-openvpn-key.pem
```

4. Connect via SSH:

```bash
ssh -i router-openvpn-key.pem openvpnas@YOUR_EC2_PUBLIC_IP
```

> **Important**: Use `openvpnas` as the username, NOT `root`!

### 9.2 Complete OpenVPN Setup Wizard

You'll be prompted with several questions. For most, accept defaults:

```
Welcome to OpenVPN Access Server

Please enter 'yes' to indicate your agreement [no]: yes

Will this be the primary Access Server node? [yes]: yes

Please specify the network interface... [all]: (press Enter)

Please specify the port number for the Admin Web UI [943]: (press Enter)

Please specify the TCP port number... [443]: (press Enter)

Should client traffic be routed by default through the VPN? [no]: yes

Should client DNS traffic be routed by default through the VPN? [no]: yes

Use local authentication via internal DB? [yes]: yes

Should private subnets be accessible to clients by default? [yes]: (press Enter)

Do you wish to login to the Admin UI as "openvpn"? [yes]: yes

Please specify your OpenVPN-AS license key (or leave blank to specify later):
(press Enter to skip)

> Please enter a new password for the 'openvpn' account:
```

5. **Set a strong password** when prompted
6. Leave the license key blank (free tier allows 2 connections)

### 9.3 Note the Admin URLs

After setup completes, you'll see:

```
Admin  UI: https://YOUR_EC2_IP:943/admin
Client UI: https://YOUR_EC2_IP:943/
```

Save these URLs!

## Part B: Configure OpenVPN Server

### 9.4 Access Admin Web Interface

1. Open a web browser
2. Navigate to: `https://YOUR_EC2_IP:943/admin`
3. Accept the security warning (self-signed certificate)
4. Login:
   - **Username**: `openvpn`
   - **Password**: (password you just created)

### 9.5 Configure VPN Routing

1. Click **VPN Settings** in the left menu
2. Scroll to **Routing** section
3. Find: "Should client Internet traffic be routed through the VPN?"
4. Set to: **Yes**
5. Scroll down and click **Save Settings**
6. Click **Update Running Server** at the top

### 9.6 Create Client Profile

1. Go to **User Management** → **User Profiles**
2. Click **+ New Profile**
3. Enter a **Comment**: `raspi-router`
4. Click **Create**
5. Click the download icon next to the profile
6. Save the `.ovpn` file to your computer

## Part C: Install OpenVPN on Router

### 9.7 SSH to Your Router

```bash
ssh root@10.123.1.1
```

### 9.8 Update Packages

```bash
opkg update
```

### 9.9 Install OpenVPN Packages

```bash
opkg install openvpn-openssl luci-app-openvpn
```

### 9.10 Reboot Router

```bash
reboot
```

Wait 60 seconds for reboot to complete.

## Part D: Configure OpenVPN Client on Router

### 9.11 Access Router Web Interface

1. Open browser and go to: `http://10.123.1.1`
2. Login with your router password
3. Navigate to **VPN** → **OpenVPN**

You should see the new OpenVPN page.

### 9.12 Upload Configuration File

1. In the OpenVPN page, find **OVPN configuration file upload**
2. Click **Choose File** and select the `.ovpn` file you downloaded
3. Give it a name: `router-manager`
4. Click **Upload**

### 9.13 Configure Authentication

1. Find your new `router-manager` instance in the list
2. Click **Edit**
3. Find the line `auth-user-pass`
4. Change it to: `auth-user-pass /etc/openvpn/auth.txt`
5. Save the configuration

### 9.14 Create Authentication File

Via SSH:

```bash
vi /etc/openvpn/auth.txt
```

Add two lines:
```
openvpn
YourOpenVPNPassword
```

Where:
- Line 1: OpenVPN username (`openvpn`)
- Line 2: The password you created in step 9.2

Save and exit (`:wq`)

Set correct permissions:

```bash
chmod 600 /etc/openvpn/auth.txt
```

### 9.15 Start OpenVPN Connection

1. Return to web interface: **VPN** → **OpenVPN**
2. Find your `router-manager` instance
3. Click the **Start** button (or toggle from Stop to Start)

## Part E: Verify VPN Connection

### 9.16 Check Connection Status

In the router web interface:
- The OpenVPN instance should show "Running" or have a green indicator

Via SSH:

```bash
# Check if tunnel interface exists
ifconfig tun0

# Check OpenVPN process
ps | grep openvpn

# Check routing
route -n
```

### 9.17 Verify IP Address Change

1. Connect a device to your "RaspiRouter" network
2. Visit: [https://whatismyipaddress.com](https://whatismyipaddress.com)
3. The IP should show your **AWS region**, not your actual location!

**Example:**
- Before VPN: Tokyo, Japan (your real location)
- After VPN: Sydney, Australia (your AWS region)

### 9.18 Additional Verification

You might notice:
- Advertisements change language based on VPN location
- Region-locked content becomes accessible
- IP geolocation services show different location

## Automatic VPN Connection on Boot

### 9.19 Enable Auto-Start

Via SSH:

```bash
/etc/init.d/openvpn enable
```

Or via web interface:
1. Go to **VPN** → **OpenVPN**
2. Find your instance
3. Enable the **Enabled** checkbox
4. Save & Apply

## Complete Network Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                   │
│  ┌─────────────┐    ┌─────────────────────┐    ┌──────────────┐ │
│  │ Your Phone  │    │   Raspberry Pi      │    │  Public      │ │
│  │ Your Laptop │───▶│   Travel Router     │───▶│  Wi-Fi       │ │
│  │ etc.        │    │   (RaspiRouter)     │    │  (Hotel/     │ │
│  └─────────────┘    └──────────┬──────────┘    │  Airport)    │ │
│                                │               └──────────────┘ │
│       Private                  │ Encrypted                       │
│       Wi-Fi                    │ VPN Tunnel                      │
│       Network                  ▼                                 │
│                     ┌─────────────────────┐                     │
│                     │   AWS OpenVPN       │                     │
│                     │   Server            │                     │
│                     │   (Sydney/Tokyo/    │                     │
│                     │    US/etc.)         │                     │
│                     └──────────┬──────────┘                     │
│                                │                                 │
│                                ▼                                 │
│                     ┌─────────────────────┐                     │
│                     │     Internet        │                     │
│                     │   (Appears from     │                     │
│                     │    AWS location)    │                     │
│                     └─────────────────────┘                     │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| VPN won't start | Check auth.txt file; verify credentials |
| No tun0 interface | Restart OpenVPN; check logs |
| Connected but no internet | Check firewall rules; verify server config |
| Slow speeds | Try different AWS region; check bandwidth |
| Connection drops | Add `keepalive 10 60` to config |

### View OpenVPN Logs

```bash
logread | grep -i openvpn
```

### Manual Start/Stop

```bash
# Start
/etc/init.d/openvpn start

# Stop
/etc/init.d/openvpn stop

# Restart
/etc/init.d/openvpn restart
```

### Test Connectivity Through VPN

```bash
# Should show AWS server IP
curl ifconfig.me

# Or
wget -qO- ipinfo.io
```

## Security Best Practices

1. **Regularly update** both router and EC2 instance
2. **Rotate passwords** periodically
3. **Monitor AWS billing** to avoid surprises
4. **Use strong encryption** (AES-256)
5. **Keep key files secure** and backed up

## Congratulations! 🎉

You've successfully built a portable, secure travel router that:

- ✅ Creates a private Wi-Fi network
- ✅ Connects to public Wi-Fi safely
- ✅ Encrypts all traffic through VPN
- ✅ Masks your real location
- ✅ Works on battery power
- ✅ Auto-configures on boot

Stay safe on public networks!

---

## Quick Reference Card

| Task | Command/URL |
|------|-------------|
| Router SSH | `ssh root@10.123.1.1` |
| Router Web UI | `http://10.123.1.1` |
| OpenVPN Admin | `https://EC2_IP:943/admin` |
| Check VPN Status | `ifconfig tun0` |
| View Logs | `logread \| grep openvpn` |
| Restart VPN | `/etc/init.d/openvpn restart` |
| Check External IP | `curl ifconfig.me` |
