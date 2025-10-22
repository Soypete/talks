---
marp: true
theme: default
paginate: true
title: GoWest 2025 Live Post-Mortem
backgroundImage: url('../images/soypete_background.png')
description: Monitoring Production AI - A Live Experiment in Breaking Things
---

<!-- _class: lead -->

# Production AI Monitoring: A Live Post-Mortem
by: Miriah Peterson

---

## Who Am I?

- Data Engineer at SchoolAI
- Organizer of GoWest, Forge Utah
- SoyPeteTech: Substack, Twitch, YouTube

**Want to learn Go?**
- I have a course on the O'Reilly Media platform!

---

## How many of you have built AI apps?
(Show of hands)
* Chatbots?
* Content generators?
* Agent systems?
* Anything calling LLM APIs?

---

## How many of you are running AI in production?
(Show of hands)
* Self-hosted models?
* Vendor APIs (OpenAI, Anthropic, etc)?
* Open-Router or similar?

---

## Meet Pedro: Why Go for AI?

API-based interactions mean **AI isn't just for Python anymore**

![bg right](../images/pedro.gif)

---

## Meet Pedro: Why Go for AI?

**Why this matters:**
- Go's concurrency handles multiple chat platforms simultaneously
- Production-grade error handling and monitoring
- Predictable performance under load

![bg right](../images/pedro.gif)

---

## 🏗️ Pedro's Architecture

**Everything running in Docker on my homelab:**

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Discord   │    │     Pedro    │    │    vLLM     │
│   Twitch    │───▶│   Go Bot    │───▶│   Model    │
│             |    │   Service    │    │   Server    │
└─────────────┘    └──────────────┘    └─────────────┘
                           │
                           ▼
                   ┌──────────────────────────┐
                   │   Observability Stack    │
                   │  Prometheus + Grafana    │
                   └──────────────────────────┘
```


---

## 🔧 Self-Hosting Reality Check

**Running your own models means managing:**

1. **Model infrastructure** - GPU servers, vLLM configuration
2. **Networking** - Latency, bandwidth, security
3. **Observability** - Observability Stack for App and AI metrics
4. **Scaling** - Handling traffic spikes
5. **Security** - Access control, data privacy

**The hard part isn't Go - it's the networking and ops**

---

## How do you monitor a production AI system?

---

## Monitoring Production AI
**That's what we're doing today!**

1. Pedro is live on [YouTube](https://www.youtube.com/watch?v=qKH3aT0owF8) and [Twitch](https://twitch.tv/soypetetech)
2. We'll watch the metrics together as things get interesting
3. I'll show you how to spot and debug problems in real-time

---

## Introducing Pedro

- Built [Pedro](https://github.com/soypetetech/IAM_pedro) — a self-hosted AI bot powered by vLLM
- Written in Go for speed and reliability
- Runs on my homelab behind Tailscale
- Connects to Discord, Twitch, YouTube for various interactions

![bg right](../images/pedro.gif)

--- 
## Let's Get Started: Join the Stream!


- **YouTube**: https://www.youtube.com/c/ForgeUtah/live
- **Twitch**: https://twitch.tv/soypetetech

**How to interact with Pedro:**

1. **Just mention "pedro" in chat** — that's it!
<!-- 2. Pedro remembers your last 10 messages (yours + his responses)
3. If more than 10 messages queue up... things might break (let's find out!)

**Fun challenge**: Pedro has a rule — he CANNOT talk about Java. Try to get him to break it. -->

---

## What Metrics Are We Tracking?


**vLLM Performance:**
- **Time to First Token (TTFT)**: How long before Pedro responds
- **End-to-End Latency**
- **Request Queue Depth** 
- **KV Cache Usage**: Memory pressure on the model
![bg right 60%](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzNrd2pxemNteHd3b295Y2dpaDZ2bzE3Y2g4dXM4dnNiMmxnNWpxeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1N4w8i2YOJIposEnye/giphy.gif)
---

## What Metrics Are We Tracking?

**Bot Performance:**
- **Message success/failure rates**
- **Empty responses** (when Pedro has nothing to say)
- **Memory usage** (Go heap allocation)

![bg right 60%](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzNrd2pxemNteHd3b295Y2dpaDZ2bzE3Y2g4dXM4dnNiMmxnNWpxeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1N4w8i2YOJIposEnye/giphy.gif)

---

##  Let's Look at Grafana

**Opening the dashboard now...**

**Live at**: http://blue2:3000/d/vllm-performance-metrics/vllm-performance-metrics

<!-- **What we're watching for:**

1. **Request Rate** climbing as you all chat with Pedro
2. **Latency spikes** when vLLM gets backed up
3. **Queue depth** when messages arrive faster than Pedro can respond
4. **KV Cache** filling up (this is memory for conversation context)

**Current baseline**: Let's see what "normal" looks like before chaos
-->
--- 

## The Alerts We Have Setup

**Critical Alerts (these mean Pedro is down):**
-  vLLM service offline
-  Discord/Twitch bots disconnected
-  LLM failure rate > 15%

![bg right 90%](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2ltc3JjaXZ6NW55cGdrdHRnNjFvNmEyajdmdTh2cmYxMDd3ZnNpcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/bC8EUWeuy5OIx6o7ul/giphy.gif)

--- 

## The Alerts We Have Setup
**Warning Alerts (Pedro is struggling):**
-  P95 Time to First Token > 1 second
-  P95 End-to-End Latency > 3 seconds
-  Request queue depth > 10
-  KV Cache usage > 85%

<!-- lets go to discord and see if any alerts are firing! -->
---

##  Scenario #1: High Latency

**Let's say we see P95 latency spike above 3 seconds...**

---

##  Scenario #1: High Latency

**What could be happening:**
1. **vLLM queue backing up** - too many requests
2. **KV cache full** - model is evicting old context
3. **Long prompts** - someone sent a huge message
4. **Network issues** - Tailscale/homelab connectivity

<!-- I have had the llms think it was responding but it was sending messages too long for twitch chat. that is why we have metrics on both vllm and twitch success rate -->
---

##  Scenario #1: High Latency
**How to diagnose:**
- Check "Waiting Requests" metric in Grafana
- Look at KV Cache usage
- Check if it correlates with request rate spike
- Make sure network is healthy (ping, Tailscale status)
- Check that twitch/discord success rates are normal

---

## ️ Fixing High Latency

**What I would do in production:**

**Quick wins:**
1. **Can I kill and restart vLLM?** - clears queue and cache
2. **Do I need to clear user history?** - reduces prompt size
3. **Throttle incoming requests** - temporarily limit chat frequency

<!-- it depends on how important history is for the use case. with twitch chat its not that important but for other use cases it might be. So I might just restart the app instance. -->

---

## ️ Fixing High Latency

**What I would do in production:**
**Longer term:**
4. **Scale horizontally** - Add more vLLM instances
5. **Add caching** - Cache common responses
6. **Evaluate Models and Prompts** - Are we using the right model for latency vs. quality?

<!-- quantized models and smaller models work better for low latency use cases, but they are kinda stupid. so its a tradeoff. -->

---

##  Scenario #2: Bad Actors

**What if someone tries to abuse Pedro?**

**Things people try:**
- Spam the same message repeatedly
- Try to jailbreak the system prompt
- Send really long messages to DOS the queue
- Try to get Pedro to say inappropriate things

---

##  Scenario #2: Bad Actors
**Our defenses:**
- Per-user message history (only 10 messages)
- Rate limiting on the Discord/Twitch side
- System prompt with guardrails
- The "no Java" rule (just for fun, but shows prompt control)


---

## ️ Handling Bad Actors
**If we see abuse patterns in Grafana:**

1. **Identify the pattern** - Look at empty response rate spiking
2. **Check the History** - I store all the interactions in Supabase for debugging?
3. **Apply rate limits** - Discord/Twitch have built-in tools
4. **Add more Guardrails** - Update system prompt, filter messages and responses, make ai do a second pass if needed

---

## ️ Handling Bad Actors
**Pedro's design helps:**
- Stateless by design
- Each platform (Discord/Twitch) has its own app and prompt and history.
- Go's concurrency means one slow request doesn't block others

<!-- I have been building it with twitch in mind. so people hacking it is expected.and has been dealt with -->
---

##  What We Learned Today

**Key takeaways from this live experiment:**

**AI-Specific Metrics Matter:**
- Time to First Token (TTFT) is user-facing latency
- Queue depth tells you about capacity
- KV cache shows memory pressure
- These aren't normal web app metrics

 ![bg right 90%](../images/PedroBot_4K_Professor.png)

---

##  What We Learned Today

**Key takeaways from this live experiment:**
**Go is Great for AI Infrastructure:**
- Handles concurrent requests across platforms easily
- Built-in observability with pprof
- Predictable performance and memory usage
- Fast enough for production API calls to vLLM

 ![bg right 90%](../images/PedroBot_4K_Professor.png)

---

## What We Learned Today

**Key takeaways from this live experiment:**
**Observability Stack:**
- Prometheus for metrics (latency, queue depth, memory)
- Grafana for visualization
- Alerts based on real user impact (not just server metrics)

![bg right 90%](../images/PedroBot_4K_Professor.png)

--- 
##  Key Takeaways

**What it takes to run production AI in Go:**

1. **Observability is not optional** - Prometheus + Loki + custom alerts
2. **Monitor AI-specific metrics** - These metrics are built into your AI stack. They are on every request or easily derived via vllm or llama.cpp
3. **Build safeguards into your code** - rate limits, circuit breakers, timeouts
4. **Use structured logging** - slog makes debugging production issues possible
5. **Test under realistic load** - AI workloads are different from HTTP APIs

---
##  Key Takeaways
**Go is excellent for AI infrastructure** - it is just a backend service making api calls. 

<!-- it is a separation of concerns problem. just run the model somewhere else. -->

---


## Should you self-host your AI models for Production?

**Start with vendors:**
- [Cerebras](https://cerebras.net/) - Fast inference at scale
- [OpenRouter](https://openrouter.ai/) - Multi-model API aggregator
- OpenAI, Anthropic, Cohere - The big players

**Self-host when:**
- You exceed vendor bandwidth limits
- You are ready to fine-tune models
- You have the infrastructure team to support it

<!-- **Networking is the hard part**, not the models. Use vendors until you have to self-host. -->

---


# Thank You


**Check out the code:**
- Pedro: [github.com/soypetetech/IAM_pedro](https://github.com/soypetetech/IAM_pedro)
- Grafana dashboards: [grafana.soypetetech.dev](https://grafana.soypetetech.dev)
- This talk: [github.com/soypetetech/talks](https://github.com/soypetetech/talks)

**Follow the journey:**
- Watch me build and break things live: [twitch.tv/soypetetech](https://twitch.tv/soypetetech)
- Blog I write about Go and AI: [@soypetetech](https://substack.com/@soypetetech)
- Chat about ai and go Discord: [discord.gg/ExTAH54KCE](https://discord.gg/ExTAH54KCE)

---

# Q&A

> "The goal isn't zero failures. The goal is to fail fast, learn quickly, and recover faster."

**Thanks for helping me stress test Pedro today!**

---

# Security & Privacy Note

**How Pedro handles your data:**

**Access Control:**
- All infrastructure behind Tailscale (zero-trust network)
- No public endpoints except the bot APIs
- Grafana requires authentication

---

# Security & Privacy Note

**Data Privacy:**
- Self-hosted model = **no data sent to OpenAI/Anthropic**
- Conversation history limited to 10 messages in memory
- No persistent storage of chat logs
- No data used for model training (it's my model!)

**Why this matters:** If you're building AI products, data sovereignty and privacy are real concerns. Self-hosting gives you full control.

--- 

##  What Did We See Today?

**Recap of our live experiment:**

- Watched real metrics in Grafana as you interacted with Pedro
- Saw how latency, queue depth, and KV cache behave under load
- Observed what happens when multiple people chat with Pedro simultaneously
- (Hopefully) triggered some alerts!

**The stack:**
- Go + vLLM + Prometheus + Grafana
- All open source, all running in Docker on my homelab
- Behind Tailscale for secure access
