# Phase 3 – Redis Caching

## Configuration

**Server**
- FastAPI
- DistilBERT sentiment classifier
- Dynamic batching enabled
- Redis cache (TTL = 3600 seconds)

**Benchmark Tool**
- ApacheBench (ab)

**Command**

```bash
ab -n 1000 -c 20 \
-p request.json \
-T application/json \
http://127.0.0.1:8000/predict
```

## Results

| Metric | Value |
|--------|------:|
| Requests/sec | **1127.57** |
| Mean latency | **17.74 ms** |
| Median latency (p50) | **15 ms** |
| p95 latency | **34 ms** |
| p99 latency | **44 ms** |
| Failed requests | **0 / 1000** |

## Notes

- The benchmark used identical request payloads.
- The first request populated the Redis cache.
- Subsequent requests were served directly from the cache.
- This benchmark measures warm-cache performance.

## Notes

This benchmark measures warm-cache performance using repeated requests for the same input text.

The first request populates Redis, while subsequent requests are served directly from the cache.

Real-world performance depends on the cache hit rate and will typically fall between the batching benchmark (0% cache hits) and the warm-cache benchmark (≈100% cache hits).