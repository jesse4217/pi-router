# Step 8: AWS OpenVPN Server Setup

## Overview

In this step, we'll set up an OpenVPN server on AWS EC2. This server will encrypt all traffic from your travel router, masking your real location and securing your connection.

## Prerequisites

- AWS account (free tier eligible)
- Credit card for AWS verification (won't be charged for free tier)
- Email address for account setup
- Completed Steps 1-7

## Why AWS?

- **Free tier**: T2.micro instance is free for 12 months
- **Global regions**: Choose server location worldwide
- **Reliable**: 99.99% uptime SLA
- **Scalable**: Upgrade if needed

## Instructions

### 8.1 Create AWS Account (If Needed)

If you don't have an AWS account:

1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click **Create an AWS Account**
3. Follow the registration process
4. Verify your identity with a credit card

### 8.2 Create an IAM User

Using the root account is not recommended. Create a dedicated user:

1. Sign in to AWS Console
2. Search for **IAM** in the services search bar
3. Click **Users** in the left sidebar
4. Click **Create user**

**User Configuration:**
- **User name**: `router-manager`
- **Check**: Provide user access to the AWS Management Console
- **Password**: Choose "I want to create an IAM user" and set a custom password

Click **Next**

### 8.3 Set User Permissions

1. Select **Attach policies directly**
2. Search for and select: **AdministratorAccess**
3. Click **Next**

> **Note**: For production, use more restrictive permissions. AdminAccess is used here for simplicity.

### 8.4 Complete User Creation

1. Review the user details
2. Click **Create user**
3. **Important**: Click **Download .csv file** to save the sign-in credentials
4. Note the sign-in URL for IAM users

### 8.5 Sign In as IAM User

1. Sign out of the root account
2. Go to the IAM sign-in URL (from step 8.4)
3. Enter the IAM username and password
4. Sign in

### 8.6 Select AWS Region

Choose a region for your VPN server based on your needs:

| Region | Use Case |
|--------|----------|
| Sydney (ap-southeast-2) | Access Australian content |
| Tokyo (ap-northeast-1) | Access Japanese content |
| US East (us-east-1) | Access US content, low latency to Europe |
| London (eu-west-2) | Access UK content |

Click the region dropdown in the top-right and select your preferred region.

### 8.7 Launch EC2 Instance

1. Search for **EC2** in the services search bar
2. Click **Instances** in the left sidebar
3. Click **Launch instances**

### 8.8 Configure Instance - AMI Selection

1. Give your instance a name: `OpenVPN-Server`
2. Click **Browse more AMIs**
3. Search for: `OpenVPN`
4. Select **OpenVPN Access Server** (BYOL - Bring Your Own License)
5. Click **Select**
6. Review the AMI details and click **Subscribe Now** if prompted

### 8.9 Configure Instance - Instance Type

Select: **t2.micro** (Free tier eligible)

```
┌─────────────────────────────────────────┐
│  Instance Type Selection                │
├─────────────────────────────────────────┤
│  ☑ t2.micro                            │
│    1 vCPU, 1 GiB Memory                 │
│    Free tier eligible                   │
└─────────────────────────────────────────┘
```

### 8.10 Create Key Pair

1. Click **Create new key pair**
2. **Key pair name**: `router-openvpn-key`
3. **Key pair type**: RSA
4. **Private key file format**: .pem (for Mac/Linux) or .ppk (for Windows/PuTTY)
5. Click **Create key pair**
6. **Save the downloaded file** - you cannot download it again!

### 8.11 Configure Security Group

Under **Network settings**:

1. Click **Edit**
2. **Security group name**: `openvpn-sg`
3. For **SSH (port 22)**: Change "Anywhere" to **My IP**
4. For **HTTPS (port 443)**: Change "Anywhere" to **My IP**
5. For **Custom UDP (port 1194)**: Keep "Anywhere" or set to **My IP**

### 8.12 Launch the Instance

1. Review all settings
2. Click **Launch instance**
3. Wait for "Success" message
4. Click **View all instances**

### 8.13 Wait for Instance to Initialize

1. Wait for **Instance state** to change from "Pending" to **Running**
2. Wait for **Status checks** to show **2/2 checks passed**
3. This typically takes 2-5 minutes

### 8.14 Note Important Information

From the instance details, note:
- **Public IPv4 address**: e.g., `52.xx.xx.xx`
- **Public IPv4 DNS**: e.g., `ec2-52-xx-xx-xx.region.compute.amazonaws.com`

## Security Group Ports Reference

| Port | Protocol | Purpose |
|------|----------|---------|
| 22 | TCP | SSH access |
| 443 | TCP | Admin web interface |
| 943 | TCP | Client web interface |
| 1194 | UDP | OpenVPN tunnel |

## Estimated AWS Costs

Using free tier (first 12 months):
- EC2 t2.micro: **Free** (750 hours/month)
- Data transfer: First 100GB/month **Free**
- Storage: 30GB **Free**

After free tier:
- t2.micro: ~$8.50/month (on-demand)
- Consider Reserved Instances for savings

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Instance won't start | Check service quotas; verify region |
| Cannot see OpenVPN AMI | Search in AWS Marketplace |
| Key pair download failed | Delete and create new key pair |
| Status checks failing | Wait longer; check instance logs |

### View Instance Logs

1. Select your instance
2. Click **Actions** → **Monitor and troubleshoot** → **Get system log**

## Next Step

→ [Step 9: OpenVPN Client Configuration](./09-openvpn-client-config.md)
