# Step 1: Flashing OpenWRT to SD Card

## Overview

In this step, we'll download the OpenWRT operating system and flash it to the microSD card that will be used in the Raspberry Pi 5.

## Prerequisites

- MicroSD card (8GB or larger recommended)
- SD card reader
- Computer with internet access
- Balena Etcher (or similar flashing tool)

## Instructions

### 1.1 Download OpenWRT Image

1. Navigate to the official OpenWRT website: [https://openwrt.org](https://openwrt.org)
2. Go to the **Downloads** or **Installation** section
3. Find the Raspberry Pi 5 section
4. Click the **factory image** link to download the image file

> **Note**: OpenWRT is a lightweight operating system, so the download should be relatively quick.

### 1.2 Prepare the SD Card

1. Insert your microSD card into the card reader
2. Connect the card reader to your laptop/computer
3. Make note of the drive letter/device name assigned to the SD card

> **Warning**: Make sure you select the correct drive to avoid overwriting important data!

### 1.3 Flash the Image

1. Download and install [Balena Etcher](https://www.balena.io/etcher/) if you haven't already
2. Open Balena Etcher
3. Click **"Flash from file"** and select the downloaded OpenWRT image
4. Click **"Select target"** and choose your microSD card
5. Click **"Flash!"** to begin the process

```
┌─────────────────────────────────────────────┐
│           Balena Etcher                     │
├─────────────────────────────────────────────┤
│  1. Select Image  →  openwrt-xxx.img        │
│  2. Select Target →  SD Card (Your card)    │
│  3. Flash!                                  │
└─────────────────────────────────────────────┘
```

6. Wait for the flashing process to complete (typically 1-3 minutes)
7. Wait for verification to complete
8. Safely eject the SD card

### 1.4 Insert SD Card into Raspberry Pi

1. Remove the microSD card from the card reader
2. Insert the card into the Raspberry Pi 5's microSD slot
3. **Do not power on yet** - we'll do this in the next step

## Verification

- Balena Etcher shows "Flash Complete!" message
- No errors during the flashing process
- SD card is properly seated in the Raspberry Pi

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Flash fails | Try a different SD card or USB port |
| Image won't select | Ensure the file downloaded completely |
| SD card not detected | Try a different card reader |
| Verification fails | Re-download the image and try again |

## Next Step

→ [Step 2: Initial SSH Setup](./02-initial-ssh-setup.md)
