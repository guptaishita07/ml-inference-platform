# Phase 1 Benchmark

## Setup

- FastAPI
- DistilBERT sentiment model
- Local CPU inference
- MacBook Air M1

## Benchmark

20 sequential requests

Average latency: ~81 ms

Notes:

- No batching
- No caching
- Single request per inference