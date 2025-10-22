---
marp: true
theme: default
paginate: true
title: GoWest 2025 Live Post-Mortem
backgroundImage: url('../images/soypete_background.png')
description: Monitoring Production AI - A Live Experiment in Breaking Things
---

<!-- _class: lead -->

# Production AI Monitoring: A Live Experiment
### Let's Stress Test Pedro Together
by: Miriah Peterson

---

## Who Am I?

- Engineer & tinkerer (6+ years writing Go professionally)
- Tech lead on data + AI systems
- Organizer of GoWest, Forge Utah, Women Who Go Utah
- Built [Pedro](https://github.com/soypetetech/IAM_pedro) — a self-hosted AI bot powered by vLLM
- Stream all my work at [twitch.tv/soypetetech](https://twitch.tv/soypetetech)

![bg right](../images/pedro.gif)

---

## Today's Plan: Break Things LIVE

**This is happening RIGHT NOW**

1. You're going to interact with Pedro (my production AI bot)
2. We'll watch the metrics together as things get interesting
3. I'll show you how to spot and fix problems in real-time

**Your mission**: Help me stress test Pedro

---

## 🚀 Let's Get Started: Join the Stream!

**Everyone, grab your phones/laptops:**

- **YouTube**: https://www.youtube.com/watch?v=qKH3aT0owF8
- **Twitch**: https://twitch.tv/soypetetech

**How to interact with Pedro:**

1. **Just mention "pedro" in chat** — that's it!
2. Pedro remembers your last 10 messages (yours + his responses)
3. If more than 10 messages queue up... things might break (let's find out!)

**Fun challenge**: Pedro has a rule — he CANNOT talk about Java. Try to get him to break it.

---

## Meet Pedro: Why Go for AI?

**Pedro is a Go application powered by vLLM**

- Self-hosted LLM (not OpenAI, not Anthropic)
- Built in Go because we wanted it **fast** and **reliable**
- API-based interactions mean **AI isn't just for Python anymore**

**Why this matters:**
- Go's concurrency handles multiple chat platforms simultaneously
- Production-grade error handling and monitoring
- Predictable performance under load

![bg right](../images/pedro.gif)

---

## What Metrics Are We Tracking?

**Let's talk about what we're measuring in Pedro:**

**vLLM Performance:**
- **Time to First Token (TTFT)**: How long before Pedro starts responding
- **End-to-End Latency**: Full response time
- **Request Queue Depth**: How many requests are waiting
- **KV Cache Usage**: Memory pressure on the model

**Bot Performance:**
- **Message success/failure rates**
- **Empty responses** (when Pedro has nothing to say)
- **Memory usage** (Go heap allocation)

---

## 📊 Let's Look at Grafana

**Opening the dashboard now...**

**Live at**: http://blue2:3000/d/vllm-performance-metrics/vllm-performance-metrics

**What we're watching for:**

1. **Request Rate** climbing as you all chat with Pedro
2. **Latency spikes** when vLLM gets backed up
3. **Queue depth** when messages arrive faster than Pedro can respond
4. **KV Cache** filling up (this is memory for conversation context)

**Current baseline**: Let's see what "normal" looks like before chaos

---

## The Alerts We Have Setup

**Critical Alerts (these mean Pedro is down):**
- 🔴 vLLM service offline
- 🔴 Discord/Twitch bots disconnected
- 🔴 LLM failure rate > 15%

**Warning Alerts (Pedro is struggling):**
- 🟡 P95 Time to First Token > 1 second
- 🟡 P95 End-to-End Latency > 3 seconds
- 🟡 Request queue depth > 10
- 🟡 KV Cache usage > 85%

**Let's see which ones we trigger...**

---

## 🎮 The 20 Questions Game

**Pedro also plays a game: 20 Questions**

**How it works:**
- Pedro thinks of something (object, person, place, etc.)
- You have 20 yes/no questions to guess it
- This is a good stress test for conversation context

**Why this matters for monitoring:**
- Tests conversation memory (those 10 messages)
- Tests latency under sustained back-and-forth
- Good way to see if Pedro loses context under load

**Try it**: Ask Pedro to play 20 questions

---

## 🚨 Scenario #1: High Latency

**Let's say we see P95 latency spike above 3 seconds...**

**What could be happening:**
1. **vLLM queue backing up** - too many requests
2. **KV cache full** - model is evicting old context
3. **Long prompts** - someone sent a huge message
4. **Network issues** - Tailscale/homelab connectivity

**How to diagnose:**
- Check "Waiting Requests" metric in Grafana
- Look at KV Cache usage
- Check if it correlates with request rate spike

---

## 🛠️ Fixing High Latency

**What I would do in production:**

**Quick wins:**
1. **Rate limit per user** - Already implemented in Pedro
2. **Timeout long requests** - Kill requests > 30 seconds
3. **Reduce max tokens** - Limit response length

**Longer term:**
4. **Scale horizontally** - Add more vLLM instances
5. **Add caching** - Cache common responses
6. **Optimize prompts** - Shorter system prompts

**Let's implement a fix if we see this...**

---

## 🚨 Scenario #2: Bad Actors

**What if someone tries to abuse Pedro?**

**Things people try:**
- Spam the same message repeatedly
- Try to jailbreak the system prompt
- Send really long messages to DOS the queue
- Try to get Pedro to say inappropriate things

**Our defenses:**
- Per-user message history (only 10 messages)
- Rate limiting on the Discord/Twitch side
- System prompt with guardrails
- The "no Java" rule (just for fun, but shows prompt control)

---

## 🛠️ Handling Bad Actors

**If we see abuse patterns in Grafana:**

1. **Identify the pattern** - Look at empty response rate spiking
2. **Check the logs** - Who is sending what?
3. **Apply rate limits** - Discord/Twitch have built-in tools
4. **Update system prompt** - Add more guardrails if needed

**Pedro's design helps:**
- Stateless by design (10 message limit)
- Each platform (Discord/Twitch/YouTube) has its own rate limits
- Go's concurrency means one slow request doesn't block others

---

## 📈 What We Learned Today

**Key takeaways from this live experiment:**

**AI-Specific Metrics Matter:**
- Time to First Token (TTFT) is user-facing latency
- Queue depth tells you about capacity
- KV cache shows memory pressure
- These aren't normal web app metrics

**Go is Great for AI Infrastructure:**
- Handles concurrent requests across platforms easily
- Built-in observability with pprof
- Predictable performance and memory usage
- Fast enough for production API calls to vLLM

**Observability Stack:**
- Prometheus for metrics (latency, queue depth, memory)
- Grafana for visualization
- Alerts based on real user impact (not just server metrics)

---

## 🏗️ Pedro's Architecture

**Everything running in Docker on my homelab:**

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Discord   │    │     Pedro    │    │    vLLM     │
│   Twitch    │───▶│   Go Bot     │───▶│   Model     │
│   YouTube   │    │   Service    │    │   Server    │
└─────────────┘    └──────────────┘    └─────────────┘
                           │
                           ▼
                   ┌──────────────────────────┐
                   │   Observability Stack    │
                   │  Prometheus + Grafana    │
                   └──────────────────────────┘
```

**All behind Tailscale for secure access**

---

## 🔧 Self-Hosting Reality Check

**Running your own models means managing:**

1. **Model infrastructure** - GPU servers, vLLM configuration
2. **Networking** - Latency, bandwidth, security
3. **Observability** - Everything we've shown today
4. **Scaling** - Handling traffic spikes
5. **Security** - Access control, data privacy

**The hard part isn't the model or Go - it's the networking and ops**

---

## 🎓 Key Takeaways

**What it takes to run production AI in Go:**

1. **Observability is not optional** - Prometheus + Loki + custom alerts
2. **Monitor AI-specific metrics** - inference time, queue depth, token throughput
3. **Build safeguards into your code** - rate limits, circuit breakers, timeouts
4. **Use structured logging** - slog makes debugging production issues possible
5. **Test under realistic load** - AI workloads are different from HTTP APIs

**Go is excellent for AI infrastructure** - but the hard part is networking, not the language

---

## 💡 My Honest Recommendation

**Should you self-host your AI models?**

**Start with vendors:**
- [Cerebrus](https://cerebras.net/) - Fast inference at scale
- [OpenRouter](https://openrouter.ai/) - Multi-model API aggregator
- OpenAI, Anthropic, Cohere - The big players

**Self-host when:**
- You exceed vendor bandwidth limits
- You need specific model control
- You have the infrastructure team to support it

**Networking is the hard part**, not the models. Use vendors until you have to self-host.

---

## 📊 What Did We See Today?

**Recap of our live experiment:**

- Watched real metrics in Grafana as you interacted with Pedro
- Saw how latency, queue depth, and KV cache behave under load
- Observed what happens when multiple people chat with Pedro simultaneously
- (Hopefully) triggered some alerts!

**The stack:**
- Go + vLLM + Prometheus + Grafana
- All open source, all running in Docker on my homelab
- Behind Tailscale for secure access

**Pedro is still running** (probably): Try it at [discord.gg/ExTAH54KCE](https://discord.gg/ExTAH54KCE)

---

## 🔗 Resources & Code

**Check out the code:**
- Pedro: [github.com/soypetetech/IAM_pedro](https://github.com/soypetetech/IAM_pedro)
- Grafana dashboards: [grafana.soypetetech.dev](https://grafana.soypetetech.dev)
- This talk: [github.com/soypetetech/talks](https://github.com/soypetetech/talks)

**Follow the journey:**
- Stream: [twitch.tv/soypetetech](https://twitch.tv/soypetetech)
- Blog: [@soypetetech](https://substack.com/@soypetetech)
- Discord: [discord.gg/ExTAH54KCE](https://discord.gg/ExTAH54KCE)

**Want to learn Go?**
- I have a course on the O'Reilly Media platform!

---

# Q&A

Let's talk about:
- What alerts did we trigger today?
- Your production AI experiences
- When to self-host vs. use vendor APIs
- Observability strategies for Go + AI
- How to stress test Pedro more effectively next time

---

# Thank You

> "The goal isn't zero failures. The goal is to fail fast, learn quickly, and recover faster."

**Thanks for helping me stress test Pedro today!**

Watch me build and break things live: [twitch.tv/soypetetech](https://twitch.tv/soypetetech)

---

# Security & Privacy Note

**How Pedro handles your data:**

**Access Control:**
- All infrastructure behind Tailscale (zero-trust network)
- No public endpoints except the bot APIs
- Grafana requires authentication

**Data Privacy:**
- Self-hosted model = **no data sent to OpenAI/Anthropic**
- Conversation history limited to 10 messages in memory
- No persistent storage of chat logs
- No data used for model training (it's my model!)

**Why this matters:** If you're building AI products, data sovereignty and privacy are real concerns. Self-hosting gives you full control.