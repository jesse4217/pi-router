# Step 10: Automated Setup with Ansible

## Overview

Steps 3-7 and 9 involve many repetitive SSH commands. This project includes Ansible playbooks that run all of those commands for you in a single shot. Instead of typing dozens of UCI commands by hand, you edit one config file and run one command.

## What Gets Automated

| Role | Manual Step | What It Does |
|------|-------------|--------------|
| `network` | Step 3 | Changes LAN IP, creates WWAN interface, sets DNS |
| `wifi_client` | Step 4 | Connects to upstream WiFi, configures firewall |
| `usb_wifi` | Step 5 | Installs USB adapter packages and drivers |
| `access_point` | Steps 6+7 | Sets up AP with custom SSID/password, creates boot script |
| `openvpn` | Step 9 | Installs OpenVPN, uploads profile, starts VPN tunnel |

## What You Still Do Manually

| Step | Why |
|------|-----|
| Step 1: Flash SD card | Physical task on your laptop |
| Step 2: First SSH + password | Must happen before Ansible can connect |
| Step 8: AWS OpenVPN server | AWS Console / GUI setup |

## Prerequisites

- Completed Steps 1 and 2 (SD card flashed, password set, Ethernet connected)
- Ansible installed on your laptop
- Downloaded `.ovpn` profile from AWS (if setting up VPN)

### Install Ansible

```bash
# macOS
brew install ansible

# Ubuntu/Debian
sudo apt install ansible

# pip (any platform)
pip install ansible
```

Verify installation:

```bash
ansible --version
```

## Project Structure

```
ansible/
    inventories/
        hosts               # Router IP and SSH settings
    group_vars/
        openwrt.yml         # All configuration variables
    site.yml                # Master playbook
    roles/
        network/            # Step 3
        wifi_client/        # Step 4
        usb_wifi/           # Step 5
        access_point/       # Steps 6+7
        openvpn/            # Step 9
```

## Quick Start

### 1. Edit the Variables

Open `ansible/group_vars/openwrt.yml` and set your values:

```yaml
# The upstream WiFi you want the router to connect to
upstream_wifi_ssid: "HotelWiFi"
upstream_wifi_password: "the-hotel-password"

# Your private access point name and password
ap_ssid: "RaspiRouter"
ap_password: "YourSecurePassword123"

# OpenVPN credentials (from Step 8)
openvpn_user: "openvpn"
openvpn_password: "your-vpn-password"
openvpn_profile_local: "~/Downloads/client.ovpn"
```

If your USB WiFi adapter uses a different chipset, update the driver packages:

```yaml
wifi_driver_packages:
  - usbutils
  - usb-modeswitch
  - kmod-rtl8xxxu          # Change this for your adapter
  - rtl8192cu-firmware      # Change this for your adapter

wifi_driver_module: "rtl8xxxu"  # Change this for your adapter
```

See [Step 5](./05-usb-wifi-adapter-setup.md) for a driver/chipset reference table.

### 2. Verify Ansible Can Reach the Router

Make sure your laptop is connected to the Pi via Ethernet and can SSH in:

```bash
cd ansible
ansible -i inventories/hosts openwrt -m raw -a "uci show system.@system[0].hostname"
```

You should see the router's hostname in the output.

### 3. Run the Playbook

**Full setup (steps 3-7 + 9):**

```bash
ansible-playbook -i inventories/hosts site.yml
```

**Router config only (steps 3-7, no VPN):**

```bash
ansible-playbook -i inventories/hosts site.yml --tags network,wifi
```

**VPN only (step 9, after AWS setup is done):**

```bash
ansible-playbook -i inventories/hosts site.yml --tags vpn
```

### 4. Verify

After the playbook finishes:

1. Look for your AP SSID (e.g. "RaspiRouter") on your phone
2. Connect and verify internet access
3. If VPN was configured, visit [whatismyipaddress.com](https://whatismyipaddress.com) to confirm your IP shows the AWS region

## Recommended Workflow

The fastest path from unboxing to working router:

```
1. Flash SD card with OpenWRT                     (laptop, Step 1)
2. Boot Pi, Ethernet to laptop, SSH in, set pwd   (laptop, Step 2)
3. Edit ansible/group_vars/openwrt.yml             (laptop)
4. ansible-playbook site.yml --tags network,wifi   (laptop)
   └── Steps 3-7 run automatically
5. Set up AWS OpenVPN server                       (browser, Step 8)
6. Download .ovpn profile                          (browser)
7. ansible-playbook site.yml --tags vpn            (laptop)
   └── Step 9 runs automatically
8. Done — verify on your phone
```

## Re-deploying to a New Location

When you arrive at a new hotel/airport, you only need to update the upstream WiFi credentials and re-run the wifi role:

```bash
# Edit group_vars/openwrt.yml — change upstream_wifi_ssid and upstream_wifi_password

ansible-playbook -i inventories/hosts site.yml --tags wifi
```

Everything else (AP config, VPN) stays the same.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `unreachable` error | Check Ethernet cable; verify you can `ssh root@10.123.1.1` manually |
| `Permission denied` | Ensure you set a password in Step 2; add `ansible_ssh_pass` to inventory or use `--ask-pass` |
| `ping` task fails | Upstream WiFi credentials may be wrong; check `group_vars/openwrt.yml` |
| VPN `tun0` check fails | Verify `.ovpn` profile path exists; check OpenVPN server is running on AWS |
| Wrong USB driver | Run `lsusb` on the Pi to identify your adapter, then update `wifi_driver_packages` |

### Using SSH Password Instead of Key

If you haven't set up SSH keys, add `--ask-pass` to prompt for the router password:

```bash
ansible-playbook -i inventories/hosts site.yml --ask-pass
```

Or install `sshpass`:

```bash
# macOS
brew install sshpass

# Ubuntu/Debian
sudo apt install sshpass
```

## Previous Step

← [Step 9: OpenVPN Client Configuration](./09-openvpn-client-config.md)
