## ApacheBench Failure Count — Explanation

When running the 1000-request load test:

\```bash
ab -n 1000 -c 20 -p request.json -T application/json http://127.0.0.1:8000/predict
\```

ApacheBench reported:

\```
Complete requests:      1000
Failed requests:        999
   (Connect: 0, Receive: 0, Length: 999, Exceptions: 0)
\```

This is **not** a server-side failure. All `Connect`, `Receive`, and `Exceptions` counts are `0`, confirming every request completed successfully with a `200 OK` response.

ApacheBench flags a request as "failed" if its response body length differs from the first response it received. Since `/predict` returns `"cached": true` or `"cached": false` depending on whether the result came from Redis, responses have slightly different byte lengths. This is expected behavior for a cache-aware endpoint and reflects a known limitation of ApacheBench with dynamic-content APIs, not an application defect.

## Prometheus Counter Reset Behavior

Prometheus `Counter` metrics (e.g. `inference_requests_total`, `inference_cache_hits_total`) are stored in-process and reset to zero whenever the FastAPI application restarts (e.g. via `docker compose down` / `docker compose up`, or a container crash and restart).

This means dashboard totals reflect activity **since the last process restart**, not lifetime totals across the project's history. This is expected default behavior for `prometheus-client` without a persistent backend, and is standard practice for counters — Prometheus itself is designed to handle counter resets gracefully when computing rates.