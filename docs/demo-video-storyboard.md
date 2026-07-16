# 🎥 Career-Ops Demo Video — Complete Storyboard

> **Goal:** A 3-minute walkthrough video showcasing Career-Ops from zero to live deployment, posted on LinkedIn to attract recruiters and demonstrate your technical skills.

**Duration:** 3:00 | **Tools:** OBS Studio (free) + DaVinci Resolve (free) | **Audience:** Recruiters + Engineering Managers

---

## 📋 Pre-Production Checklist

| Item | Done | Details |
|------|:----:|---------|
| ☐ | Open Career-Ops at `http://localhost:5173` | Ensure all features work |
| ☐ | Open n8n at `http://localhost:5678` | Activate all 6 workflows |
| ☐ | Open Telegram | Show bot notifications |
| ☐ | Open Grafana at `http://localhost:3001` | Show monitoring dashboard |
| ☐ | Have sample data ready | 3-5 jobs, applications, AI results |

---

## 🎬 Scene-by-Scene Breakdown

---

### Scene 1: Hook (0:00 — 0:15)

**Visual:** 
- Split screen: Left side = Your face + desk setup | Right side = Fast terminal scrolling (Docker build)

**Audio:**
```
"Most people spend 11 hours a week on job applications.
I built an AI that does it in 2 seconds."

[terminal sound effect — Docker build completing]

"Meet Career-Ops. Your Career, Supercharged by AI."
```

**On Screen Text:**
```
11 hours/week → 2 seconds
Career-Ops v2
```

**Recording Tips:**
- Dress professionally (business casual)
- Good lighting facing you
- Clean background

---

### Scene 2: The Problem (0:15 — 0:35)

**Visual:** Screen recording showing messy spreadsheets + 10 browser tabs

**Audio:**
```
"Job searching is broken. You're juggling:
→ A spreadsheet for applications
→ LinkedIn for searching
→ 5 different resume versions
→ Gmail drafts for follow-ups
→ Calendar reminders for interviews

It's exhausting. And it doesn't have to be."
```

**On Screen:** 
- Excel spreadsheet with job tracking columns
- Multiple browser tabs (LinkedIn, Indeed, Gmail, Google Calendar)
- Stack of paper resumes

---

### Scene 3: One-Command Deploy (0:35 — 1:00)

**Visual:** Terminal recording showing the deploy command

**Audio:**
```
"So I built Career-Ops. And the journey starts with ONE command."

[type: curl -fsSL https://raw.githubusercontent.com/... | bash]

"Fifteen minutes later — you have a production-grade Career
Operating System running on your own infrastructure.
Free domain, free HTTPS, free AI."
```

**On Screen:** Terminal output showing:
```
✅ DuckDNS configured
✅ Cloudflare Tunnel started
✅ 16 Docker services online
✅ AI (Gemini) connected
🎉 Deployment complete!
App is live at: https://careerops.duckdns.org
```

---

### Scene 4: Dashboard & Jobs (1:00 — 1:20)

**Visual:** Career-Ops Dashboard + Jobs page screen recording

**Audio:**
```
"The dashboard gives you real-time visibility into
your entire job search. Jobs found, applications sent,
interviews scheduled, and follow-ups pending.

One click to add a job, track status, or
let the AI do the heavy lifting."
```

**On Screen:** 
- Dashboard stat cards animating
- Jobs list with search/filter
- Status badges showing pipeline

---

### Scene 5: AI Resume Engine (1:20 — 1:40)

**Visual:** AI Tools page — ATS score + Resume optimization

**Audio:**
```
"This is where Career-Ops shines. Google Gemini AI
analyzes your resume against any job description.

ATS score, keyword gaps, formatting improvements —
all in real-time. And with streaming SSE,
you see the results as they're generated."
```

**On Screen:**
- ATS score: 73% → "AI Optimize" → 92%
- Streaming text appearing character by character
- Keyword gap analysis

---

### Scene 6: Auto-Apply Engine (1:40 — 2:00)

**Visual:** Auto-Apply page — Scrape modal + Pipeline progress

**Audio:**
```
"The Auto-Apply engine connects everything.
→ Scrape jobs from LinkedIn, Indeed, career pages
→ AI tailors your resume for each job
→ Sends a professional application email
→ Tracks responses
→ Follows up automatically

All from one dashboard. All automated."
```

**On Screen:**
- Scrape modal with source selection
- Jobs appearing as found
- "Full Pipeline" button click
- Progress: Sourced → Optimized → Emailed

---

### Scene 7: Notifications (2:00 — 2:20)

**Visual:** Phone showing Telegram notifications + Email inbox

**Audio:**
```
"Real-time notifications on EVERY event.
New job found → Telegram ping.
Application sent → Telegram ping.
Interview scheduled → Telegram ping.
Follow-up needed → Telegram ping.

Plus daily digests, weekly summaries, and
Slack integration for team visibility."
```

**On Screen:** 
- Phone notification: "✅ New Application Created — Google"
- Phone notification: "🎯 Interview Scheduled!"
- Email inbox showing daily digest
- Slack channel with Career-Ops alerts

**Split Screen:** 
- Left: Career-Ops dashboard
- Right: Telegram notifications arriving in real-time
- Center: Your video reacting to notifications

---

### Scene 8: Monitoring & Observability (2:20 — 2:35)

**Visual:** Grafana dashboard + Prometheus metrics

**Audio:**
```
"Full observability built in. Prometheus metrics,
Grafana dashboards with 12 panels, Loki log aggregation,
and 14 alerting rules keeping everything running smoothly.

16 Docker services. All monitored. All logged."
```

**On Screen:**
- Grafana dashboard with request rate, latency, error rate panels
- Prometheus targets: all UP
- Alertmanager rules

---

### Scene 9: Tech Stack Reveal (2:35 — 2:50)

**Visual:** Architecture diagram animating in

**Audio:**
```
"The tech stack:
→ FastAPI + Python 3.12 backend (140+ endpoints)
→ React 19 + TypeScript 6 + Framer Motion frontend
→ PostgreSQL 16 + Redis 7 + Celery workers
→ Google Gemini AI + n8n automation
→ Prometheus + Grafana + Loki monitoring
→ DuckDNS + Cloudflare — zero cost to deploy

115 passing tests. 16 Docker services.
Production-grade. Open source."
```

**On Screen:** Animated architecture diagram building up:
```
[React] → [FastAPI] → [PostgreSQL]
                         ↓
                    [Redis Cache]
                         ↓
                    [Celery Workers]
                         ↓
                    [Gemini AI]
                         ↓
                    [n8n Automation]
                         ↓
              [Prometheus + Grafana]
```

---

### Scene 10: Call to Action (2:50 — 3:00)

**Visual:** GitHub repo QR code + your face

**Audio:**
```
"Career-Ops is open source. Star it on GitHub.
Deploy it yourself in 15 minutes — for free.
Link in the comments.

Your career deserves better tools.
Let's build the future of work — together."
```

**On Screen:**
- GitHub QR code: `https://github.com/kmrgautam18-alt/career-ops-v2`
- Text: "Star on GitHub ⭐ · Deploy for $0 · Get Hired 🚀"
- Your name + title: "Kumar Gautam · Full Stack Engineer"

---

## 🎵 Background Music (Free)

| Scene | Mood | Track Source |
|:-----:|------|-------------|
| 1-2 | Building tension | YouTube Audio Library → "Ambient Cinematic" |
| 3-4 | Empowerment | YouTube Audio Library → "Corporate Inspiration" |
| 5-7 | Tech excitement | YouTube Audio Library → "Modern Technology" |
| 8-10 | Resolution | YouTube Audio Library → "Upbeat Motivation" |

---

## 📱 LinkedIn Post (Post Immediately After Video)

```
🎥 I built Career-Ops — An AI-Powered Career Operating System

From zero to production in 15 minutes. Here's what it does:

✅ One-command deploy (Docker + DuckDNS + Cloudflare)
✅ AI resumes tailored to every job (Gemini → ATS 92%)
✅ Auto-apply engine (scrape → optimize → send → track)
✅ Real-time Telegram/Slack/Email notifications
✅ Daily digests + weekly summaries
✅ Auto follow-up reminders
✅ Full monitoring (Prometheus + Grafana)
✅ 16 Docker services, 140 API endpoints

Tech stack: FastAPI · React · TypeScript · PostgreSQL · Redis
Celery · Gemini AI · n8n · Prometheus · Grafana · Docker

All open source. All free to deploy.

Star it on GitHub, try it yourself — link in comments! 🚀

#CareerOps #OpenSource #AI #JobSearch #Python #React
#Docker #DevOps #CareerGrowth #BuildInPublic

@CareerOps @FastAPI @React @Docker
```

---

## 🎬 Production Checklist

| Step | Task | Tool |
|:----:|------|------|
| 1 | Record screen at 1920x1080, 30fps | OBS Studio |
| 2 | Record webcam in corner (circle crop) | OBS Studio |
| 3 | Record clean audio (use a USB mic if possible) | OBS Studio |
| 4 | Import all clips into editor | DaVinci Resolve |
| 5 | Cut out pauses and mistakes | DaVinci Resolve |
| 6 | Add transitions (subtle crossfades) | DaVinci Resolve |
| 7 | Add text overlays for key stats | DaVinci Resolve |
| 8 | Add background music (low volume) | DaVinci Resolve |
| 9 | Export as MP4, 1080p, H.264 | DaVinci Resolve |
| 10 | Upload to LinkedIn → Write post → Publish | LinkedIn |

---

## 📊 Post-Engagement Strategy

| Time | Action |
|:----:|--------|
| Day 1 | Reply to every comment within 1 hour |
| Day 2 | Post a follow-up comment with the GitHub link |
| Day 3 | Create a poll: "Which Career-Ops feature would you use?" |
| Day 5 | Share a screenshot of a new feature/bug fix |
| Day 7 | Post weekly progress update using linkedin-automation.sh |

---

<div align="center">

**🎬 Ready to record! Let's get you hired.** 🚀

*"Your career deserves better tools."*

</div>
