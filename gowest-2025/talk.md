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
### Let's Break Pedro Together (And Learn How to Monitor AI Apps)
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

## Today's Experiment

**We're doing a LIVE post-mortem**

This isn't a story about what went wrong last year.
This is happening RIGHT NOW.

**Your mission**: Try to break Pedro, my production AI bot.

---

## Meet Pedro: Production AI Bot

**Pedro is a 100% open source AI assistant built in Go**

- GitHub: [github.com/soypetetech/IAM_pedro](https://github.com/soypetetech/IAM_pedro)
- Running in production for SoypeteTech community
- Self-hosted using vLLM for model serving
- Integrates with Discord & Twitch in real-time

![bg right](../images/pedro.gif)

---

## How to Break Pedro (Please Try!)

**Join the stress test:**

1. **Discord**: Join the SoypeteTech Discord and spam Pedro
   - Link: [discord.gg/soypetetech](https://discord.gg/soypetetech)
   - Mention `@Pedro` in messages

2. **YouTube Live Stream**: Chat in the GoWest conference livestream
   - Pedro monitors the livestream chat
   - Just start chatting!

**Goal**: Generate enough traffic to trigger alerts

---

## Pedro's Production Architecture

**What you're actually hitting:**

- **Bot Service**: Go application with Discord/Twitch integrations
- **Model Backend**: vLLM serving Llama model
- **Infrastructure**: Single server (it's easy to DDoS, trust me)
- **Observability Stack**:
  - Prometheus for metrics
  - Grafana for dashboards
  - Loki for log aggregation
  - Custom alerts in Go using `envar` package

---

## The Observability Stack

**Three layers of monitoring:**

1. **Prometheus Alerts** - Infrastructure metrics (CPU, memory, latency)
2. **Application Logs** - Loki aggregates structured logs from Go
3. **Custom Application Alerts** - Go code using `envar` package for business logic alerts

**We'll walk through all three as alerts fire...**

---

## 🚨 Alert #1: Latency Spike (Prometheus)

**This is what you'll likely trigger first:**

```yaml
Alert: HighResponseLatency
Expr: histogram_quantile(0.95, rate(http_request_duration_seconds[5m])) > 2
Severity: WARNING
```

**What this means:**
- 95th percentile response time > 2 seconds
- Pedro is struggling to keep up with requests
- vLLM model inference is getting backed up

**Let's open Grafana and watch it happen...**

---

## 📊 Grafana Dashboard Walkthrough

**Key metrics we're watching:**

1. **Request Rate**: Requests per second hitting Pedro
2. **Response Latency**: P50, P95, P99 latencies
3. **Model Inference Time**: vLLM processing time
4. **Go Runtime Metrics**: Goroutines, GC pauses, heap usage
5. **System Resources**: CPU, memory, network

**Demo**: Live dashboard at `grafana.soypetetech.dev`

---

## 📊 Loki Logs: Structured Logging in Go

**Pedro uses structured logging with slog:**

```go
logger.Info("processing message",
    slog.String("user_id", userID),
    slog.String("platform", "discord"),
    slog.Duration("inference_time", duration),
)
```

**In Loki we can query:**
```logql
{job="pedro"} | json | inference_time > 5s
```

**Let's look at the logs as traffic increases...**

---

## 🚨 Alert #2: Custom Application Alerts

**Pedro has custom alerts using the `envar` package:**

```go
// In github.com/Soypete/iam_pedro
if queueDepth > maxQueueDepth {
    alert.Send("Queue depth exceeded",
        alert.WithSeverity("critical"),
        alert.WithMetric("queue_depth", queueDepth),
    )
}
```

**Business logic alerts:**
- Queue depth > 50 pending requests
- Model error rate > 10%
- Token rate limiting triggered

---

## 🔍 Investigation: What's Happening?

**As alerts fire, let's investigate:**

1. **Check Prometheus metrics** - Is it infrastructure or application?
2. **Query Loki logs** - What errors are we seeing?
3. **Look at custom alerts** - What business logic is breaking?

**Common issues we'll likely see:**
- Model inference bottleneck (vLLM can't keep up)
- Go goroutine buildup (async message processing)
- Network latency (Discord/Twitch API rate limits)

---

## 🛠️ Mitigation Strategies

**When things go wrong, here's how I respond:**

1. **Check the alerts** - Which layer is failing?
2. **Query the logs** - What's the error pattern?
3. **Scale back** - Reduce traffic or disable features
4. **Fix and monitor** - Deploy fix, watch metrics

**Built-in safeguards in Pedro:**
- Rate limiting per user
- Circuit breaker for vLLM
- Request timeout (30s max)
- Graceful degradation (fallback responses)

---

## 🔧 How Pedro Uses the `envar` Package

**Custom alerting in Go code:**

```go
import "github.com/Soypete/iam_pedro/pkg/envar"

// Load config with alert thresholds
cfg := envar.MustLoad()

// Monitor and alert
if metrics.QueueDepth > cfg.AlertThreshold {
    envar.SendAlert("queue_overload", metrics)
}
```

**Why custom alerts matter:**
- Prometheus doesn't know your business logic
- Application-level insights (queue depth, user behavior)
- Flexible alerting channels (Discord, Slack, PagerDuty)

---

## 📈 Observability Lessons Learned

**What makes production AI different:**

1. **AI-specific metrics**: Model inference time, token throughput, queue depth
2. **Long-tail latencies**: P99 matters more than average
3. **Cascading failures**: Model slowdown → goroutine buildup → memory pressure
4. **Unpredictable load**: Viral moments can 10x your traffic instantly

**Go makes this manageable** - but you need the right observability

---

## 🎯 The Observability Stack Breakdown

**Three complementary tools working together:**

| Tool | Purpose | What It Monitors |
|------|---------|------------------|
| **Prometheus** | Infrastructure metrics | CPU, memory, latency, throughput |
| **Loki** | Log aggregation | Application errors, request traces |
| **envar (Go)** | Business logic alerts | Queue depth, model errors, user patterns |

**Together they give you the full picture**

---

## 🏗️ Pedro's Architecture

**Current production setup:**

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
                   │  Loki + Custom Alerts    │
                   └──────────────────────────┘
```

**It's simple, but it works (mostly)**

---

## 🔧 What Self-Hosting AI Actually Takes

**Running your own models means managing:**

1. **Model infrastructure** - GPU servers, vLLM configuration
2. **Networking** - Latency, bandwidth, DDoS protection
3. **Observability** - Everything we've talked about today
4. **Scaling** - Handling viral moments, traffic spikes
5. **Maintenance** - Model updates, security patches, cost optimization

**Networking is HARD. It's not just about the model.**

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

## 📊 Post-Mortem: What We Learned Today

**Hopefully you saw:**
- Real alerts firing in Grafana
- Logs streaming through Loki
- Custom alerts from Go code
- How I investigate and mitigate issues

**The stack:**
- Go + vLLM + Prometheus + Grafana + Loki + Custom Alerts
- All open source, all running in production
- Monitoring multiple platforms (Discord, Twitch, YouTube)

**Pedro is still running** (probably): Try it at [discord.gg/soypetetech](https://discord.gg/soypetetech)

---

## 🔗 Resources & Code

**Check out the code:**
- Pedro: [github.com/soypetetech/IAM_pedro](https://github.com/soypetetech/IAM_pedro)
- Grafana dashboards: [grafana.soypetetech.dev](https://grafana.soypetetech.dev)
- This talk: [github.com/soypetetech/talks](https://github.com/soypetetech/talks)

**Follow the journey:**
- Stream: [twitch.tv/soypetetech](https://twitch.tv/soypetetech)
- Blog: [@soypetetech](https://substack.com/@soypetetech)

---

# Q&A

Let's talk about:
- What alerts did we trigger?
- Your production AI horror stories
- When to self-host vs. use vendor APIs
- Observability strategies for Go + AI
- How to DDoS Pedro more effectively

---

# Thank You

> "Systems that never break are fragile. We should optimize for low MTTR, not zero alerts."
> — Database Reliability Engineering

**Keep breaking things (in production)** - that's how we learn to recover faster.

Watch me fix things live at [twitch.tv/soypetetech](https://twitch.tv/soypetetech)
Read the post-mortem series at [@soypetetech](https://substack.com/@soypetetech)