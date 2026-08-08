# Dynamic Batching Performance Comparison

| Metric | Without Batching | With Batching |
|--------|-----------------:|--------------:|
| Requests/sec | **31.59** | **54.04** |
| Mean latency | **316.58 ms** | **148 ms** |
| p50 latency | **195 ms** | **112 ms** |
| p95 latency | **428 ms** | **292 ms** |
| Failed requests | **0** | **0** |

## Observation

Under an ApacheBench workload of 100 requests with a concurrency level of 10, the dynamic batching implementation increased throughput while reducing average and tail latency compared with direct inference.