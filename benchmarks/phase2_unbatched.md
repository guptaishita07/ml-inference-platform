# Phase 2 – Baseline (Without Dynamic Batching)

## Configuration

**Server**
- FastAPI
- DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`)
- Direct inference (`model.predict()`)
- No request batching

**Benchmark Tool**
- ApacheBench (ab)

**Command**

```bash
ab -n 100 -c 10 \
-p request.json \
-T application/json \
http://127.0.0.1:8000/predict
```

## Results

| Metric | Value |
|--------|------:|
| Requests/sec | **31.59** |
| Mean latency | **316.58 ms** |
| Median latency (p50) | **195 ms** |
| p95 latency | **428 ms** |
| p99 latency | **959 ms** |
| Failed requests | **0 / 100** |

## Notes

- Each request performs inference immediately.
- No queueing or request aggregation.
- Used as the baseline for comparison with the dynamic batching implementation.