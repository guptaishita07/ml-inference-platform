# Performance Comparison

This document compares the performance of the ML Inference Platform across major optimization phases.

## Benchmark Summary

| Version | Requests/sec | Mean Latency | p50 | p95 | Failed Requests |
|---------|-------------:|-------------:|----:|----:|----------------:|
| **Direct Inference** | **31.59** | **316.58 ms** | **195 ms** | **428 ms** | **0 / 100** |
| **Dynamic Batching** | **54.04** | **148.00 ms** | **112 ms** | **292 ms** | **0 / 100** |
| **Redis Cache (Warm Cache)** | **1127.57** | **17.74 ms** | **15 ms** | **34 ms** | **0 / 1000** |

## Benchmark Configurations

### Direct Inference
- FastAPI + DistilBERT
- One inference per request
- No batching
- No caching

**ApacheBench Command**

```bash
ab -n 100 -c 10 \
-p request.json \
-T application/json \
http://127.0.0.1:8000/predict
```

---

### Dynamic Batching
- Batch size: 8
- Maximum wait time: 50 ms
- Requests grouped using an asynchronous queue
- No caching

**ApacheBench Command**

```bash
ab -n 100 -c 10 \
-p request.json \
-T application/json \
http://127.0.0.1:8000/predict
```

---

### Redis Cache (Warm Cache)
- Dynamic batching enabled
- Redis cache with SHA-256 request hashing
- Cache TTL: 3600 seconds
- Repeated requests served directly from Redis

**ApacheBench Command**

```bash
ab -n 1000 -c 20 \
-p request.json \
-T application/json \
http://127.0.0.1:8000/predict
```

## Key Observations

- Dynamic batching improved throughput under concurrent workloads while reducing average request latency compared with direct inference.
- Redis caching significantly reduced response latency for repeated requests by serving cached predictions instead of re-running model inference.
- Warm-cache performance exceeded **1,100 requests/sec** with a mean response latency below **20 ms**.
- All benchmark runs completed with **zero failed requests**.

## Notes

The Redis benchmark represents **warm-cache performance**. Since identical request payloads were used, only the first request required model inference; subsequent requests were served directly from Redis. This benchmark demonstrates the performance benefits of caching repeated inference requests rather than raw model throughput.