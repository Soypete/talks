# Pedro AI Bot - PromQL Queries Reference

This document contains all PromQL queries used for monitoring Pedro in production. These queries power both alerts and Grafana dashboards.

## Table of Contents
- [Alert Queries](#alert-queries)
- [Dashboard Queries](#dashboard-queries)
  - [Latency Metrics](#latency-metrics)
  - [Request Rate & Traffic](#request-rate--traffic)
  - [Go Runtime Metrics](#go-runtime-metrics)
  - [Error Rate Metrics](#error-rate-metrics)
  - [System Resources](#system-resources)
- [Alert Rules Configuration](#alert-rules-configuration)

---

## Alert Queries

These are the core queries used for triggering alerts in production.

### 1. High Response Latency (P95)
**Purpose**: Alert when 95th percentile response time exceeds 2 seconds

```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="pedro"}[5m])) > 2
```

**Alert Configuration**:
- **Threshold**: 2 seconds
- **Duration**: 2 minutes
- **Severity**: Warning

---

### 2. Critical Response Latency (P99)
**Purpose**: Alert when 99th percentile response time exceeds 5 seconds (long-tail detection)

```promql
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{job="pedro"}[5m])) > 5
```

**Alert Configuration**:
- **Threshold**: 5 seconds
- **Duration**: 1 minute
- **Severity**: Critical

---

### 3. Model Inference Time Spike
**Purpose**: Alert when vLLM model inference P95 exceeds 3 seconds

```promql
histogram_quantile(0.95, rate(pedro_model_inference_duration_seconds_bucket[5m])) > 3
```

**Alert Configuration**:
- **Threshold**: 3 seconds
- **Duration**: 2 minutes
- **Severity**: Warning

---

### 4. High Average Latency
**Purpose**: Simple metric for when average request duration exceeds 1 second

```promql
rate(http_request_duration_seconds_sum{job="pedro"}[5m]) / rate(http_request_duration_seconds_count{job="pedro"}[5m]) > 1
```

**Alert Configuration**:
- **Threshold**: 1 second
- **Duration**: 5 minutes
- **Severity**: Warning

---

### 5. Queue Depth Critical
**Purpose**: Alert when request queue backs up beyond capacity

```promql
pedro_queue_depth > 50
```

**Alert Configuration**:
- **Threshold**: 50 pending requests
- **Duration**: 1 minute
- **Severity**: Critical

---

### 6. Model Error Rate High
**Purpose**: Alert when model error rate exceeds 10%

```promql
rate(pedro_model_errors_total[5m]) / rate(pedro_model_requests_total[5m]) > 0.1
```

**Alert Configuration**:
- **Threshold**: 10% (0.1)
- **Duration**: 2 minutes
- **Severity**: Warning

---

## Dashboard Queries

### Latency Metrics

#### HTTP Request Duration (P50, P95, P99)
Monitor response time percentiles to catch both typical and long-tail latency.

```promql
# P50 (median)
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{job="pedro"}[5m]))

# P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="pedro"}[5m]))

# P99
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{job="pedro"}[5m]))
```

**Why these percentiles?**
- **P50**: Typical user experience
- **P95**: Most users' worst-case experience
- **P99**: Long-tail detection (AI inference can have high variance)

---

#### Model Inference Duration (P50, P95, P99)
Track vLLM model processing time separately from overall request latency.

```promql
# P50 inference time
histogram_quantile(0.50, rate(pedro_model_inference_duration_seconds_bucket[5m]))

# P95 inference time
histogram_quantile(0.95, rate(pedro_model_inference_duration_seconds_bucket[5m]))

# P99 inference time
histogram_quantile(0.99, rate(pedro_model_inference_duration_seconds_bucket[5m]))
```

---

#### Average Response Time
Simpler metric for quick overview.

```promql
rate(http_request_duration_seconds_sum{job="pedro"}[5m]) / rate(http_request_duration_seconds_count{job="pedro"}[5m])
```

---

### Request Rate & Traffic

#### Overall Request Rate
Requests per second hitting Pedro.

```promql
rate(http_requests_total{job="pedro"}[5m])
```

---

#### Request Rate by Platform
Break down traffic by source (Discord, Twitch, YouTube).

```promql
# Discord
rate(http_requests_total{job="pedro",platform="discord"}[5m])

# Twitch
rate(http_requests_total{job="pedro",platform="twitch"}[5m])

# YouTube
rate(http_requests_total{job="pedro",platform="youtube"}[5m])
```

**Use Case**: Identify which platform is driving load during spikes.

---

#### Queue Depth
Monitor request backlog to detect processing bottlenecks.

```promql
# Current queue depth
pedro_queue_depth

# 5-minute average
avg_over_time(pedro_queue_depth[5m])
```

**Alert Threshold**: Queue depth > 50 indicates vLLM can't keep up.

---

### Go Runtime Metrics

#### Goroutine Count
Track concurrent goroutines to detect leaks or buildup.

```promql
go_goroutines{job="pedro"}
```

**What to watch for**: Steady increase indicates goroutine leak or unprocessed work.

---

#### Heap Memory Usage
Monitor Go heap allocation and usage.

```promql
# Heap allocated bytes
go_memstats_heap_alloc_bytes{job="pedro"}

# Heap in use bytes
go_memstats_heap_inuse_bytes{job="pedro"}
```

---

#### GC Pause Duration (P95)
Track garbage collection pause times.

```promql
histogram_quantile(0.95, rate(go_gc_duration_seconds_bucket{job="pedro"}[5m]))
```

**Why it matters**: Long GC pauses contribute to latency spikes.

---

### Error Rate Metrics

#### HTTP 5xx Error Rate
Monitor server-side errors as a percentage of total requests.

```promql
rate(http_requests_total{job="pedro",status=~"5.."}[5m]) / rate(http_requests_total{job="pedro"}[5m])
```

**Alert Threshold**: > 5% indicates systemic issues.

---

#### Model Error Rate
Track errors specifically from the vLLM model backend.

```promql
rate(pedro_model_errors_total[5m]) / rate(pedro_model_requests_total[5m])
```

**Alert Threshold**: > 10% indicates model backend issues.

---

### System Resources

#### CPU Usage
Monitor CPU utilization percentage.

```promql
rate(process_cpu_seconds_total{job="pedro"}[5m]) * 100
```

---

#### Memory Usage Percentage
Track memory consumption relative to system total.

```promql
(process_resident_memory_bytes{job="pedro"} / node_memory_MemTotal_bytes) * 100
```

---

#### Network I/O
Monitor network throughput (requires node_exporter).

```promql
# Receive rate
rate(node_network_receive_bytes_total[5m])

# Transmit rate
rate(node_network_transmit_bytes_total[5m])
```

---

## Alert Rules Configuration

Complete Prometheus alert rules file for Pedro monitoring.

```yaml
groups:
  - name: pedro_alerts
    interval: 30s
    rules:
      # Latency Alerts
      - alert: HighResponseLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="pedro"}[5m])) > 2
        for: 2m
        labels:
          severity: warning
          component: pedro
        annotations:
          summary: "High P95 response latency on Pedro"
          description: "P95 latency is {{ $value }}s (threshold: 2s)"
          dashboard: "https://grafana.soypetetech.dev/d/pedro-monitoring"

      - alert: CriticalResponseLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{job="pedro"}[5m])) > 5
        for: 1m
        labels:
          severity: critical
          component: pedro
        annotations:
          summary: "Critical P99 response latency on Pedro"
          description: "P99 latency is {{ $value }}s (threshold: 5s)"
          dashboard: "https://grafana.soypetetech.dev/d/pedro-monitoring"

      - alert: ModelInferenceSlow
        expr: histogram_quantile(0.95, rate(pedro_model_inference_duration_seconds_bucket[5m])) > 3
        for: 2m
        labels:
          severity: warning
          component: vllm
        annotations:
          summary: "vLLM model inference is slow"
          description: "P95 inference time is {{ $value }}s (threshold: 3s)"
          runbook: "Check vLLM server logs and GPU utilization"

      # Queue and Capacity Alerts
      - alert: QueueDepthHigh
        expr: pedro_queue_depth > 50
        for: 1m
        labels:
          severity: critical
          component: pedro
        annotations:
          summary: "Pedro request queue is backing up"
          description: "Queue depth is {{ $value }} (threshold: 50)"
          runbook: "Model backend may be overwhelmed. Consider scaling or rate limiting."

      # Error Rate Alerts
      - alert: ModelErrorRateHigh
        expr: rate(pedro_model_errors_total[5m]) / rate(pedro_model_requests_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
          component: vllm
        annotations:
          summary: "Model error rate exceeds 10%"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook: "Check vLLM server health and model availability"

      - alert: HTTPErrorRateHigh
        expr: rate(http_requests_total{job="pedro",status=~"5.."}[5m]) / rate(http_requests_total{job="pedro"}[5m]) > 0.05
        for: 2m
        labels:
          severity: warning
          component: pedro
        annotations:
          summary: "HTTP 5xx error rate exceeds 5%"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # Resource Alerts
      - alert: GoroutineLeakSuspected
        expr: go_goroutines{job="pedro"} > 1000
        for: 5m
        labels:
          severity: warning
          component: pedro
        annotations:
          summary: "High goroutine count detected"
          description: "{{ $value }} goroutines running (threshold: 1000)"
          runbook: "Possible goroutine leak. Check for stuck async handlers."

      - alert: HighMemoryUsage
        expr: (process_resident_memory_bytes{job="pedro"} / node_memory_MemTotal_bytes) * 100 > 80
        for: 5m
        labels:
          severity: warning
          component: pedro
        annotations:
          summary: "High memory usage on Pedro"
          description: "Memory usage is {{ $value }}% (threshold: 80%)"
```

---

## Query Customization Tips

### Adjusting Time Windows
All queries use `[5m]` time windows by default. Adjust based on your traffic:

- **High traffic**: Use `[1m]` or `[2m]` for faster detection
- **Low traffic**: Use `[10m]` or `[15m]` for smoother graphs

```promql
# Fast detection (high traffic)
rate(http_requests_total{job="pedro"}[1m])

# Smoother graphs (low traffic)
rate(http_requests_total{job="pedro"}[15m])
```

---

### Filtering by Labels
Add label filters to narrow queries:

```promql
# Filter by platform
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="pedro",platform="discord"}[5m]))

# Filter by endpoint
rate(http_requests_total{job="pedro",endpoint="/api/chat"}[5m])

# Filter by status code
rate(http_requests_total{job="pedro",status="200"}[5m])
```

---

### Aggregation
Combine metrics across labels:

```promql
# Sum across all platforms
sum(rate(http_requests_total{job="pedro"}[5m]))

# Average latency across instances
avg(histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="pedro"}[5m])))

# Max queue depth across replicas
max(pedro_queue_depth)
```

---

## Metric Naming Conventions

Pedro uses standard Prometheus metric naming:

| Metric Type | Suffix | Example |
|-------------|--------|---------|
| Counter | `_total` | `http_requests_total` |
| Gauge | none | `pedro_queue_depth` |
| Histogram | `_bucket`, `_sum`, `_count` | `http_request_duration_seconds_bucket` |
| Summary | `_sum`, `_count` | `pedro_model_inference_duration_seconds_sum` |

---

## Loki Log Queries

For structured log queries in Loki (mentioned in talk):

```logql
# Find slow inference times
{job="pedro"} | json | inference_time > 5s

# Filter by platform
{job="pedro"} | json | platform="discord"

# Find errors
{job="pedro"} | json | level="error"

# Count errors over time
sum(rate({job="pedro"} | json | level="error" [5m]))
```

---

## Related Resources

- **Pedro Source Code**: [github.com/soypetetech/IAM_pedro](https://github.com/soypetetech/IAM_pedro)
- **Grafana Dashboard**: Import `pedro-dashboard.json` from this directory
- **GoWest 2025 Talk**: See `talk.md` for full presentation
- **Prometheus Docs**: [prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)

---

## Notes

- All metric names assume default Prometheus Go client library naming
- Adjust `job="pedro"` label based on your Prometheus configuration
- Some queries require `node_exporter` for system-level metrics
- Dashboard panels are optimized for 5-second refresh rate
