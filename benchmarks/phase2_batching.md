# Phase 2 – Dynamic Request Batching

## Configuration

**Server**
- FastAPI
- DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`)
- Dynamic batching (`batch_size=8`)
- Maximum wait time: **50 ms**

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
| Requests/sec | **54.04** |
| Mean latency | **148 ms** |
| Median latency (p50) | **112 ms** |
| p95 latency | **292 ms** |
| p99 latency | **345 ms** |
| Failed requests | **0 / 100** |

## Notes

- Requests are queued and processed in batches of up to **8**.
- Maximum batching delay: **50 ms**.
- ApacheBench logs confirmed that requests were grouped into batches during execution.