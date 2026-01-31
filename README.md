# Raspberry Pi Travel Router with OpenWRT and OpenVPN

A complete guide to building a portable, secure travel router using Raspberry Pi 5, OpenWRT, and OpenVPN.

## Overview

This project creates a personal travel router that:
- Connects to public Wi-Fi networks (hotels, airports, cafes)
- Creates a private, secure Wi-Fi access point for your devices
- Routes all traffic through a VPN for privacy and security
- Runs on a mobile battery for portability

## Hardware Requirements

| Component | Description |
|-----------|-------------|
| Raspberry Pi 5 | Main router hardware |
| MicroSD Card | For the OpenWRT operating system |
| SD Card Reader | To flash the OS from your laptop |
| USB Wi-Fi Adapter | Configured as an access point |
| Ethernet Cable | For initial setup connection |
| USB Type-C Cable | Power supply |
| Mobile Battery (Optional) | For portable power |

## Software Requirements

- OpenWRT (Operating System)
- Balena Etcher (Image flashing tool)
- Terminal/SSH Client
- AWS Account (for VPN server)

## Guide Structure

Follow these steps in order:

1. [Flashing OpenWRT](./01-flashing-openwrt.md) - Download and flash the OS
2. [Initial SSH Setup](./02-initial-ssh-setup.md) - First connection and password configuration
3. [Network Configuration](./03-network-configuration.md) - IP address and interface setup
4. [Connecting to Wi-Fi](./04-connecting-to-wifi.md) - Join an existing network
5. [USB Wi-Fi Adapter Setup](./05-usb-wifi-adapter-setup.md) - Install drivers and packages
6. [Access Point Configuration](./06-access-point-configuration.md) - Create your private network
7. [Auto-Start Script](./07-auto-start-script.md) - Automatic startup on boot
8. [AWS OpenVPN Server Setup](./08-aws-openvpn-setup.md) - Create VPN server on AWS
9. [OpenVPN Client Configuration](./09-openvpn-client-config.md) - Connect router to VPN

## Network Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Public Wi-Fi   │────▶│  Raspberry Pi    │────▶│  Your Devices   │
│  (Untrusted)    │     │  Travel Router   │     │  (Secure)       │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                                 │ VPN Tunnel
                                 ▼
                        ┌─────────────────┐
                        │  AWS OpenVPN    │
                        │  Server         │
                        └─────────────────┘
```

## Quick Reference

- Default OpenWRT IP: `192.168.1.1`
- Custom IP (this guide): `10.123.1.1`
- OpenWRT Web Interface: `http://10.123.1.1`
- Default SSH User: `root`

## Troubleshooting

See individual step files for step-specific troubleshooting. For general issues:

- **Cannot SSH**: Check Ethernet connection and IP address
- **No Internet**: Verify Wi-Fi credentials and firewall settings
- **USB Adapter not detected**: Try different USB port or check driver installation
- **VPN not connecting**: Verify credentials and server configuration

## License

This guide is provided as-is for educational purposes.
