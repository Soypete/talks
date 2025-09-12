---
marp: true
theme: default
paginate: true
title: GoWest 2025 Survey Post-Mortem
backgroundImage: url('../images/soypete_background.png')
description: What Went Wrong When We Tried to Survey 500+ Gophers with AI
---

<!-- _class: lead -->

# GoWest 2025 Survey Post-Mortem  
### What Went Wrong When We Tried to Survey 500+ Gophers with AI
by: Miriah Peterson  

---

## Who Am I?

- Engineer & tinkerer (6+ years writing Go professionally)
- Tech lead on data + AI systems
- Organizer of GoWest, Forge Utah, Women Who Go Utah
- Built [Pedro](https://github.com/soypetetech/IAM_pedro) — a Twitch & Discord AI bot
- Stream all my work at [twitch.tv/soypetetech](https://twitch.tv/soypetetech)

![bg right](../images/pedro.gif)

---

## What We Tried to Do

**Build a real-time AI-powered survey for GoWest 2025**

- Live audience polling during this talk
- AI analysis of responses using Pedro (our Go-based AI bot)
- Real-time sentiment analysis and summarization
- All self-hosted, all open source, all in Go

---

## Meet Pedro: Our AI Survey Bot

**Pedro is a 100% open source AI assistant built in Go**

- GitHub: [github.com/soypetetech/IAM_pedro](https://github.com/soypetetech/IAM_pedro)
- Self-hosted using Ollama + Llama.cpp
- Integrates with Discord, Twitch, and now... conference surveys
- Built for real-time interaction and analysis

![bg right](../images/pedro.gif)

---

## The Survey Setup

**How we hosted the survey:**

- **Frontend**: Simple Go web server with WebSocket connections
- **AI Backend**: Pedro running Llama 3.1 8B via Ollama
- **Infrastructure**: Single DigitalOcean droplet (4 CPU, 8GB RAM)
- **Monitoring**: Prometheus + Grafana + Loki for logs
- **Database**: SQLite (because we're optimists)

*Survey URL: `survey.gowest2025.dev` (if it's still up...)*

---

## The Survey Questions

**What we asked you:**

1. How many years have you been writing Go?
2. What's your biggest Go pain point?
3. What Go feature do you want most?
4. Rate your AI experience (1-10)
5. One word to describe Go

*Pedro was supposed to analyze responses in real-time and provide insights...*

---

## 🚨 Alert #1: Response Time Spike

**Time**: 10:15 AM (5 minutes into the talk)

```
Grafana Alert: HTTP Response Time > 5s
Query: rate(http_request_duration_seconds[5m]) > 5
Severity: WARNING
```

**What we saw:**
- Survey responses taking 8-12 seconds
- CPU usage spiking to 95%
- Memory usage climbing steadily

---

## 🔍 Investigation: What Was Happening?

**Grafana Dashboard showed:**

- **HTTP requests/sec**: 50+ (expected ~10)
- **Ollama inference time**: 3-8 seconds per request
- **Go GC pressure**: 15% of CPU time
- **SQLite lock contention**: Growing queue

**The problem**: Every survey response triggered AI analysis

---

## 📊 Loki Logs: The Smoking Gun

```
level=error msg="ollama request timeout" duration=30s
level=warn msg="sqlite: database is locked" retry=3
level=error msg="websocket write timeout" client_id=user_123
level=info msg="ai analysis queued" queue_size=47
```

**Root cause**: No request queuing, no circuit breakers, no timeouts

---

## 🚨 Alert #2: Memory Exhaustion

**Time**: 10:22 AM (12 minutes in)

```
Grafana Alert: Memory Usage > 90%
Query: (1 - (node_memory_available_bytes / node_memory_total_bytes)) > 0.9
Severity: CRITICAL
```

**What happened:**
- Go heap size: 6.2GB (of 8GB total)
- Ollama model cache: 2.1GB
- Survey responses backing up in memory

---

## 🛠️ Emergency Fixes (Live Debugging)

**What we did in real-time:**

1. **Disabled AI analysis** for new responses
2. **Added request rate limiting** (5 req/sec per IP)
3. **Implemented circuit breaker** for Ollama calls
4. **Switched to async processing** with Redis queue
5. **Added connection pooling** for SQLite

*Yes, we debugged this live during the talk...*

---

## 📈 Results After Fixes

**Metrics improved dramatically:**

- **Response time**: 8s → 200ms
- **Memory usage**: 90% → 45%
- **CPU usage**: 95% → 30%
- **Survey completion rate**: 23% → 87%

**But we learned some hard lessons...**

---

## 🎯 What We Should Have Done

**Architecture mistakes we made:**

1. **No load testing** with realistic AI workloads
2. **Synchronous AI processing** instead of async queues
3. **Single point of failure** (one droplet)
4. **No graceful degradation** when AI was slow
5. **SQLite for concurrent writes** (should've used Postgres)

**Go wasn't the problem - our architecture was**

---

## 🏗️ Better Architecture for Next Time

**What we'd do differently:**

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Load      │    │   Survey     │    │   Redis     │
│  Balancer   │───▶│   Service    │───▶│   Queue     │
└─────────────┘    └──────────────┘    └─────────────┘
                           │                    │
                           ▼                    ▼
                   ┌──────────────┐    ┌─────────────┐
                   │  PostgreSQL  │    │ AI Workers  │
                   │   Database   │    │  (Pedro)    │
                   └──────────────┘    └─────────────┘
```

---

## 🔧 Scaling Solutions We Considered

**Horizontal scaling options:**

1. **Multiple Ollama instances** behind load balancer
2. **Kubernetes deployment** with HPA based on queue depth
3. **Separate AI service** with gRPC communication
4. **Cloud AI APIs** as fallback (OpenAI, Claude)
5. **Edge deployment** with Fly.io or Railway

**We chose**: Quick fixes first, proper architecture later

---

## 📊 Final Survey Results

**Despite the chaos, we got great data:**

- **427 responses** from GoWest attendees
- **Average Go experience**: 4.2 years
- **Top pain point**: Generics complexity (31%)
- **Most wanted feature**: Better error handling (28%)
- **Go in one word**: "Reliable" (47 mentions)

*Pedro eventually analyzed it all... just not in real-time*

---

## 🎓 Lessons for Production AI in Go

1. **Load test with realistic AI workloads** (not just HTTP)
2. **Always use async processing** for AI operations
3. **Circuit breakers are mandatory** for external AI services
4. **Monitor AI-specific metrics**: tokens/sec, model memory, queue depth
5. **Have a fallback plan** when AI is slow/down
6. **Go is excellent for AI infrastructure** - just design it right

---

## 🔗 Resources & Code

**Check out the code:**
- Pedro: [github.com/soypetetech/IAM_pedro](https://github.com/soypetetech/IAM_pedro)
- Survey tool: [github.com/soypetetech/gowest-survey](https://github.com/soypetetech/gowest-survey)
- Grafana dashboards: [grafana.gowest2025.dev](https://grafana.gowest2025.dev)

**Follow the journey:**
- Stream: [twitch.tv/soypetetech](https://twitch.tv/soypetetech)
- Blog: [@soypetetech](https://substack.com/@soypetetech)

---

# Final Thoughts

> "Post-mortems aren't about failure - they're about learning. Today we learned that Go + AI works great... when you architect it right."

**The survey is still running** (hopefully): `survey.gowest2025.dev`

---

# Q&A

Let's talk about:  
- Your production AI horror stories
- Monitoring strategies for AI workloads  
- Go vs Python for AI infrastructure
- Self-hosting vs API trade-offs

---

# Thank You  

Follow the post-mortem series at [@soypetetech](https://substack.com/@soypetetech)  
Watch me fix things live at [twitch.tv/soypetetech](https://twitch.tv/soypetetech)