# 🤖 n8n Workflow Automation — Zero-Cost Setup Guide

> **Goal:** Set up n8n workflow automation for Career-Ops with Telegram, Email, and Slack notifications — **all for $0/month**.

**Last Updated:** 2026-07-16 | **Total Cost:** $0.00

---

## 📋 What You'll Set Up

| # | Workflow | Trigger | What It Does | Cost |
|:-:|----------|---------|-------------|:----:|
| 1 | **🔔 Job Alerts** | Every 6 hours | Scrapes new jobs, sends Telegram + Email | $0 |
| 2 | **📋 Status Emails** | Webhook | Sends formatted email on status changes | $0 |
| 3 | **📊 Daily Digest** | Daily at 8 AM | Stats summary via Telegram + Email | $0 |
| 4 | **🔄 Follow-up Reminders** | Daily | Auto follow-up emails for pending apps | $0 |
| 5 | **🎯 Interview Detection** | Webhook | Notifies on interview scheduling | $0 |
| 6 | **📱 Telegram Notifications** | Webhook | All events → Telegram instantly | $0 |

**All 6 workflows. Zero cost. Fully automated.**

---

## 🧰 What You Need (All Free)

| Account | What For | Sign Up |
|---------|----------|---------|
| 🤖 **Telegram Bot** | Instant notifications | @BotFather on Telegram — 2 minutes |
| 📧 **Gmail** | Send application emails | Free Google account |
| 💬 **Slack** | Team notifications (optional) | Free Slack workspace |
| 🐳 **Docker** | Run n8n + Career-Ops | Already installed via deploy script |

---

## 🚀 Step 1: Start n8n

If you used the `deploy-zero-click.sh` script, n8n is already running. Verify:

```bash
docker compose ps n8n
# Should show: careerops-n8n   Up   0.0.0.0:5678->5678/tcp
```

If not running, start it:
```bash
cd ~/career-ops-v2
docker compose up -d n8n
```

**Access n8n:** Open `http://your-vm-ip:5678` in your browser.

On first visit, you'll see a sign-up page. Create an admin account for n8n (any email/password — this is local, not shared).

---

## 🤖 Step 2: Create Your Free Telegram Bot

Telegram is the fastest and freest notification channel. Let's set it up:

### 2.1 Create a Bot with @BotFather

1. Open Telegram and search for **@BotFather** (the official bot creation bot)
2. Start a chat and send: `/newbot`
3. Follow the prompts:
   ```
   BotFather: Alright, a name for your bot. What is it?
   You: CareerOps Notifier

   BotFather: Good. Now let's choose a username for your bot.
   You: careerops_notifier_bot
   ```
4. **Copy the token** — it looks like: `1234567890:ABCdefGHIjklmNOPqrstUVwxyz`
5. Save it: `echo 'Your bot token: 1234567890:ABCdefGHIjklmNOPqrstUVwxyz'`

### 2.2 Get Your Chat ID

1. Open Telegram and search for your bot's username (e.g., `@careerops_notifier_bot`)
2. Click **Start** to begin the conversation
3. Send any message: `hello`
4. Run this command to get your chat ID:
   ```bash
   curl -s "https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates" | python3 -c "
   import sys, json
   data = json.load(sys.stdin)
   for update in data.get('result', []):
       msg = update.get('message', {})
       chat = msg.get('chat', {})
       print(f'Chat ID: {chat.get(\"id\")} — {chat.get(\"first_name\", \"\")} {chat.get(\"last_name\", \"\")}')
   "
   ```
5. You'll see output like: `Chat ID: 123456789 — Your Name`
6. **Save your Chat ID** (it's a number, usually 8-10 digits)

### 2.3 Add Telegram Credentials to n8n

1. In n8n, go to **Credentials** → **New Credential**
2. Search for **Telegram** and select it
3. Fill in:
   - **Access Token:** Your bot token from @BotFather
4. Click **Save**

---

## 📧 Step 3: Set Up Free Email (Gmail App Password)

### 3.1 Generate Gmail App Password

1. Go to your Google Account → **Security** → **2-Step Verification** → Turn it **ON**
2. Go to **Security** → **App Passwords** (search if not visible)
3. Select: **App: Mail** → **Device: Other** → Name it: `Career-Ops n8n`
4. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)
5. Save it immediately — you won't see it again!

### 3.2 Add SMTP Credentials to n8n

1. In n8n, go to **Credentials** → **New Credential**
2. Search for **SMTP** and select it
3. Fill in:
   - **Host:** `smtp.gmail.com`
   - **Port:** `587`
   - **User:** Your full Gmail address (e.g., `yourname@gmail.com`)
   - **Password:** The 16-character App Password
   - **SSL/TLS:** Toggle ON
4. Click **Save** and then **Test** to verify

---

## 💬 Step 4: Set Up Slack (Optional)

### 4.1 Create Slack Webhook

1. Go to: https://api.slack.com/apps → **Create New App** → **From scratch**
2. Name it: `Career-Ops Alerts`, select your workspace
3. Go to **Incoming Webhooks** → Toggle **Activate Incoming Webhooks**
4. Click **Add New Webhook to Workspace**
5. Choose a channel (e.g., `#careerops-alerts`) → **Allow**
6. **Copy the webhook URL** (looks like: `https://hooks.slack.com/services/T.../B.../xxx`)

### 4.2 Add Slack Credentials to n8n

1. In n8n, go to **Credentials** → **New Credential**
2. Search for **Slack** and select **OAuth2**
3. Or simpler: use the **Webhook** node instead and post to the URL directly
4. Save

---

## 📥 Step 5: Import Pre-Built Workflows

### 5.1 Find the Workflow Files

The workflows are on your VM at:
```bash
ls ~/career-ops-v2/monitoring/n8n/workflows/
```

You'll see:
```
application-status-email.json
daily-digest-workflow.json
follow-up-automation-workflow.json
interview-detection-workflow.json
job-alert-workflow.json
telegram-notifications.json
```

### 5.2 Import into n8n

1. Open n8n at `http://your-vm-ip:5678`
2. Click **Workflows** in the left sidebar
3. Click **Import from File** → Select each `.json` file
4. Import ALL 6 workflows (do this one at a time)

### 5.3 Configure Each Workflow

#### 🔔 Workflow 1: Job Alert
1. Open the **Job Alert** workflow
2. Double-click the **HTTP Request** node
3. Add Career-Ops API token as Authorization header:
   - Get your token: 
     ```bash
     curl -s -X POST http://localhost:8000/api/v1/auth/login \
       -H "Content-Type: application/json" \
       -d '{"email":"YOUR_ADMIN_EMAIL","password":"YOUR_ADMIN_PASSWORD"}' | \
       python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['access_token'])"
     ```
   - In n8n, create a **Header Auth** credential with your token
4. Configure **Slack** node with your webhook URL
5. Configure **SMTP** node with your Gmail credentials
6. Click **Save** → **Activate** (toggle at top)

#### 📋 Workflow 2: Status Email
1. Open the **Status Email** workflow
2. Configure **SMTP** node with Gmail credentials
3. The webhook URL is: `http://n8n:5678/webhook/careerops-application-status`
4. Click **Save** → **Activate**

#### 📊 Workflow 3: Daily Digest
1. Open the **Daily Digest** workflow
2. Add Career-Ops API token (same as Job Alert)
3. Configure **Telegram** node with your bot
4. Configure **SMTP** node with Gmail credentials
5. Click **Save** → **Activate**

#### 🔄 Workflow 4: Follow-up Reminders
1. Open the **Follow-up Automation** workflow
2. Add Career-Ops API token
3. Configure **SMTP** node with Gmail
4. Optionally configure **Telegram** node
5. Click **Save** → **Activate**

#### 🎯 Workflow 5: Interview Detection
1. Open the **Interview Detection** workflow
2. Configure **SMTP** with Gmail
3. Configure **Slack** (if using)
4. Click **Save** → **Activate**

#### 📱 Workflow 6: Telegram Notifications
1. Open the **Telegram Notifications** workflow
2. Configure **Telegram** node with your bot token
3. Set `TELEGRAM_CHAT_ID` in n8n environment variables:
   - Go to **Settings** → **Environment Variables**
   - Add: `TELEGRAM_CHAT_ID` = your chat ID number
4. Click **Save** → **Activate**

---

## 🔗 Step 6: Connect Backend Webhooks

For the webhook-triggered workflows to work, Career-Ops needs to send events to n8n.

### 6.1 Enable Webhooks in Career-Ops

```bash
# Edit your .env file
cd ~/career-ops-v2
nano .env

# Set these values:
N8N_ENABLED=true
N8N_WEBHOOK_BASE_URL=http://n8n:5678

# Restart the backend
docker compose restart backend
```

### 6.2 Verify Webhook Delivery

Test by creating an application via the API:
```bash
# Login first
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"YOUR_EMAIL","password":"YOUR_PASS"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])")

# Create a job first
JOB=$(curl -s -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Test Job","company":"Test Company","description":"Testing webhooks"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# Create an application (this should trigger the webhook)
curl -X POST http://localhost:8000/api/v1/applications \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"job_id\":$JOB,\"status\":\"applied\",\"applied_date\":\"$(date +%Y-%m-%d)\"}"
```

### 6.3 Check n8n Executions

1. In n8n, go to **Executions** in the left sidebar
2. You should see recent executions with **Success** status
3. If any failed, click to see the error message

---

## 📱 Step 7: Test Telegram Notifications

### 7.1 Manual Test

In n8n, open the **Telegram Notifications** workflow:
1. Click **Execute Workflow** button
2. Enter test data: `{ "event": "application.created", "company": "Google", "job_title": "Senior Engineer", "applied_date": "2026-07-16" }`
3. Click **Execute**
4. Check your Telegram — you should see a notification like:

```
✅ New Application Created

📌 Company: Google
💼 Position: Senior Engineer
📅 Applied: 2026-07-16

Status: saved
```

### 7.2 Real Test

Create an application through the Career-Ops UI or API, and within seconds you should receive a Telegram notification.

---

## 📊 Step 8: Production Checklist

### ✅ Webhook Endpoints

| Endpoint | Event | Workflow |
|----------|-------|----------|
| `/webhook/careerops-application-created` | New application added | Status Email, Telegram |
| `/webhook/careerops-application-status` | Status changed | Status Email, Telegram |
| `/webhook/careerops-application-deleted` | Application removed | Status Email, Telegram |

### ✅ Active Workflows

| Workflow | Status | Runs At |
|----------|:------:|---------|
| 🔔 Job Alert | ☐ Active | Every 6 hours |
| 📋 Status Email | ☐ Active | On status change |
| 📊 Daily Digest | ☐ Active | 8 AM daily |
| 🔄 Follow-up | ☐ Active | 8 AM daily |
| 🎯 Interview Detection | ☐ Active | On interview |
| 📱 Telegram Notifications | ☐ Active | On any event |

### ✅ Environment Variables in n8n

```
TELEGRAM_CHAT_ID=your_chat_id_number
CAREER_OPS_API_URL=http://careerops-backend:8000
CAREER_OPS_API_TOKEN=your_jwt_token
CAREER_OPS_URL=https://careerops.duckdns.org
```

---

## 🎯 Step 9: Get Realistic Results

### What to Expect When Live

Once everything is connected, here's your real-world automation flow:

```
📱 You search "Python Developer" on LinkedIn via Career-Ops
     ↓
🔔 Job Alert workflow finds matching jobs
     ↓
💾 Jobs saved to Career-Ops automatically
     ↓
🤖 AI tailors your resume for each job
     ↓
📧 Auto-Apply sends application via SMTP
     ↓
🔄 Application status tracked
     ↓
📱 Telegram notification: "Status updated: Applied → Interview"
     ↓
🎯 Interview detected → Telegram + Email prep tips
     ↓
🔄 Follow-up sent 7 days later automatically
     ↓
📊 Daily digest every morning at 8 AM
```

### Real Metrics to Track

| Metric | Target | How to Track |
|--------|:------:|-------------|
| Applications sent per day | 5-20 | Career-Ops dashboard |
| Interview rate | 10-25% | Status tracking |
| Telegram notifications received | Daily | Your Telegram app |
| Follow-up emails sent | 3-7 days after | Automatic |
| Daily digest delivery | Every 8 AM | Email + Telegram |
| Response rate after follow-up | 30-50% | Manual tracking |

### Example: Your Day with Career-Ops + n8n

| Time | Event | Automated Action |
|:----:|-------|-----------------|
| 6 AM | New jobs posted on LinkedIn | Job Alert workflow scrapes and saves |
| 8 AM | Daily Digest | Summary of yesterday's activity |
| 9 AM | Application sent | Telegram notification: "Applied to Google" |
| 3 PM | Status → Interview | Telegram: "🎯 Interview Scheduled!" |
| 5 PM | Interview prep email | SMTP sends preparation tips |
| 7 days later | Follow-up | Auto email + Telegram reminder |

---

## 🛠️ Troubleshooting — Free Fixes

| Problem | Solution |
|---------|----------|
| ❌ **Webhook not firing** | Check `N8N_ENABLED=true` in `.env`; restart backend: `docker compose restart backend` |
| ❌ **Telegram not sending** | Verify bot token in n8n credentials; check `TELEGRAM_CHAT_ID` is a number, not a string |
| ❌ **Email not sending** | Gmail: Enable "Allow less secure apps" OR use App Password (must have 2FA ON) |
| ❌ **n8n can't reach backend** | Use Docker internal URL: `http://careerops-backend:8000` |
| ❌ **Workflow executions failing** | Open the execution in n8n → hover over red nodes → see exact error |
| ❌ **"401 Unauthorized"** | Regenerate your API token; it may have expired |
| ❌ **Workflow not activating** | Ensure all credentials are configured and valid |
| ❌ **DuckDNS not resolving** | Check cron: `crontab -l`; run updater manually: `sudo /opt/duckdns/duck.sh` |

---

## 📚 Reference

| Resource | Link |
|----------|------|
| n8n Dashboard | `http://your-vm-ip:5678` |
| Career-Ops API | `http://your-vm-ip:8000/docs` |
| Telegram BotFather | `https://t.me/botfather` |
| Gmail App Passwords | `https://myaccount.google.com/apppasswords` |
| Slack Webhooks | `https://api.slack.com/apps` |
| DuckDNS | `https://duckdns.org` |

---

## 🏁 You're Done!

You now have a **fully automated, zero-cost Career-Ops + n8n system** that:

- 🤖 Scrapes jobs automatically every 6 hours
- 📧 Sends AI-tailored applications via email
- 📱 Notifies you on **Telegram** instantly on any event
- 💬 Posts to **Slack** for team visibility
- 🔄 Follows up with recruiters automatically
- 📊 Sends you a **daily digest** every morning
- 🎯 Detects interviews and sends prep tips

**All 6 workflows. All free. All automated.** 🚀
