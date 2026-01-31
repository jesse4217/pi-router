"""Scan devices on the current WiFi network using ARP(Address Resolution Protocol)."""

import ipaddress
import socket
import subprocess
import sys


def get_local_subnet():
    """Detect the local IP and derive the /24 subnet."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return ipaddress.ip_network(f"{local_ip}/24", strict=False)


def scan(subnet):
    """Ping-sweep the subnet then read the ARP table."""
    flag = "-c" if sys.platform != "win32" else "-n"
    procs = []
    for host in subnet.hosts():
        p = subprocess.Popen(
            ["ping", flag, "1", "-W", "1", str(host)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        procs.append(p)
    for p in procs:
        p.wait()

    result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
    devices = []
    for line in result.stdout.splitlines():
        if "incomplete" in line or "no entry" in line:
            continue
        parts = line.split()
        if len(parts) >= 4:
            ip = parts[1].strip("()")
            mac = parts[3]
            if mac.count(":") == 5 or mac.count("-") == 5:
                devices.append((ip, mac))
    return devices


if __name__ == "__main__":
    subnet = get_local_subnet()
    print(f"Scanning {subnet} ...")
    devices = scan(subnet)
    print(f"\n{'IP Address':<18} {'MAC Address'}")
    print("-" * 38)
    for ip, mac in sorted(devices, key=lambda d: ipaddress.ip_address(d[0])):
        print(f"{ip:<18} {mac}")
    print(f"\n{len(devices)} device(s) found.")
