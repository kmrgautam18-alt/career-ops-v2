# AWS EC2 Deployment Guide — Career-Ops v2

## 1. Create an EC2 Instance

1. Go to [AWS EC2 Console](https://console.aws.amazon.com/ec2/)
2. Click **Launch Instance**
3. Configure:

| Setting | Value |
|---|---|
| Name | `career-ops-prod` |
| AMI | **Ubuntu 24.04 LTS** (HVM, SSD) |
| Instance type | `t3.medium` (2 vCPU, 4 GB RAM — good starting point) |
| Key pair | Create or select an existing `.pem` key |
| Network settings | Create security group (see below) |
| Storage | 20 GB gp3 |
| Advanced > User data | Paste the `ec2-bootstrap.sh` script |

## 2. Security Group Rules

| Type | Protocol | Port | Source | Purpose |
|---|---|---|---|---|
| SSH | TCP | 22 | `0.0.0.0/0` | Admin access (restrict to your IP in production) |
| HTTP | TCP | 80 | `0.0.0.0/0` | Frontend (Nginx) |
| HTTPS | TCP | 443 | `0.0.0.0/0` | Frontend (TLS — add later) |

> ⚠️ **Do NOT open port 8000 to the public.** The Nginx reverse proxy handles API requests internally.

## 3. IAM Access Keys (for CI/CD)

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Create a user `career-ops-deploy` with **Programmatic access**
3. Attach the **minimum policy** (create a custom one):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeInstanceStatus",
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

4. Save the **Access Key ID** and **Secret Access Key**

## 4. Keys Required (add in Freebuff Keys tab)

| Key | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | Your IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | Your IAM user secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `EC2_HOST` | EC2 public DNS (e.g. `ec2-xx-xx-xx-xx.compute-1.amazonaws.com`) |
| `EC2_SSH_KEY` | Paste the full content of your `.pem` private key |

## 5. Deploy

### Option A — Manual (first time)
```bash
# SSH into the instance
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com

# Set up env
cd ~/career-ops-v2
nano .env                                      # Fill in secrets
docker compose up -d --build                   # Start everything
docker compose exec backend alembic upgrade head  # Run migrations
```

### Option B — Automated (updates)
```bash
# From your local machine
EC2_HOST="ec2-xx-xx-xx-xx.compute-1.amazonaws.com" \
EC2_SSH_KEY="~/.ssh/your-key.pem" \
bash scripts/deploy-ec2.sh
```

## 6. Verify

```bash
curl http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com
# → {"application":"Career-Ops v2","status":"healthy"}
```
