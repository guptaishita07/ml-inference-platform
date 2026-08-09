from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    "inference_requests_total",
    "Total number of prediction requests"
)

REQUEST_LATENCY = Histogram(
    "inference_request_latency_seconds",
    "Latency of prediction requests"
)

CACHE_HITS = Counter(
    "inference_cache_hits_total",
    "Total cache hits"
)

CACHE_MISSES = Counter(
    "inference_cache_misses_total",
    "Total cache misses"
)

BATCH_SIZE = Histogram(
    "inference_batch_size",
    "Size of processed batches",
    buckets=[1, 2, 4, 8, 16, 32]
)

QUEUE_DEPTH = Gauge(
    "inference_queue_depth",
    "Current queue depth"
)