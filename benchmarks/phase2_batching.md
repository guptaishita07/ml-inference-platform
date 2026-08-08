# Phase 2 – Dynamic Batching

## ApacheBench

Command:

ab -n 100 -c 10 \
-p request.json \
-T application/json \
http://127.0.0.1:8000/predict

Results

Requests/sec: 54.04

Mean latency: 148 ms

p50: 112 ms

p95: 292 ms

p99: 345 ms

Failed requests: 0