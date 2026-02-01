# Step 7: Auto-Start Script

## Overview

In this step, we'll create an init script that automatically configures the USB Wi-Fi adapter and starts the access point every time the router boots up.

## Prerequisites

- Completed Steps 1-6
- Access point working manually
- SSH access to the router

## Why This Is Needed

The USB Wi-Fi adapter configuration may not persist automatically after reboot. This script ensures:
- The Wi-Fi adapter is properly initialized
- The access point starts reliably
- A small delay allows system stability before starting

## Instructions

### 7.1 Navigate to Init Directory

```bash
cd /etc/init.d
```

### 7.2 Create the Auto-Start Script

Create a new script file:

```bash
vi wifi-adapter
```

### 7.3 Add the Script Content

Press `i` to enter insert mode and paste the following:

```bash
#!/bin/sh /etc/rc.common

START=99
STOP=10

start() {
    sleep 5
    wifi
}

stop() {
    wifi down
}
```

### 7.4 Understanding the Script

| Line | Explanation |
|------|-------------|
| `#!/bin/sh /etc/rc.common` | Uses OpenWRT's init system |
| `START=99` | High priority - runs after most services |
| `STOP=10` | Low priority - stops before most services |
| `sleep 5` | 5-second delay for system stability |
| `wifi` | Reloads wireless configuration |
| `wifi down` | Stops wireless interfaces |

### 7.5 Save and Exit

1. Press `Esc` to exit insert mode
2. Type `:wq` and press Enter to save and quit

### 7.6 Make the Script Executable

```bash
chmod +x /etc/init.d/wifi-adapter
```

### 7.7 Enable the Script

Register the script to run at boot:

```bash
/etc/init.d/wifi-adapter enable
```

### 7.8 Verify the Script is Enabled

```bash
ls -la /etc/rc.d/ | grep wifi
```

You should see a symlink like `S99wifi-adapter`.

### 7.9 Test the Script Manually

```bash
/etc/init.d/wifi-adapter start
```

### 7.10 Reboot and Test

Reboot the router to verify everything works:

```bash
reboot
```

After reboot (wait ~60 seconds):
1. Look for your SSID (e.g., "RaspiRouter") on your phone/device
2. Connect to verify it's working

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Script doesn't run at boot | Verify symlink exists in `/etc/rc.d/` |
| Permission denied | Run `chmod +x /etc/init.d/wifi-adapter` |
| SSID doesn't appear after boot | Increase sleep delay; check logs |
| Driver not loading | Add explicit `modprobe` command |

### Common Issues

1. **Script syntax error**: Verify shebang line is exactly `#!/bin/sh /etc/rc.common`
2. **Wrong permissions**: Script must be executable
3. **Missing symlink**: Re-run `enable` command
4. **Driver issues**: Add driver loading to script

## Complete File Check

Verify your script:

```bash
cat /etc/init.d/wifi-adapter
```

Should output:

```bash
#!/bin/sh /etc/rc.common

START=99
STOP=10

start() {
    sleep 5
    wifi
}

stop() {
    wifi down
}
```

## Next Step

→ [Step 8: AWS OpenVPN Server Setup](./08-aws-openvpn-setup.md)
