from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import make_asgi_app
import time

from app.model import SentimentModel
from app.batcher import DynamicBatcher
from app.cache import PredictionCache

from app.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    CACHE_HITS,
    CACHE_MISSES,
)

# Create FastAPI app
app = FastAPI()

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Shared components
model = SentimentModel()
batcher = DynamicBatcher(
    model=model,
    batch_size=8,
    max_wait_ms=50,
)

cache = PredictionCache()


class PredictRequest(BaseModel):
    text: str


@app.on_event("startup")
async def startup():
    batcher.start()


@app.get("/")
def root():
    return {
        "message": "ML Inference Platform is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True
    }


@app.post("/predict")
async def predict(request: PredictRequest):
    start = time.perf_counter()

    REQUEST_COUNT.inc()

    # Check Redis cache
    cached_result = cache.get(request.text)

    if cached_result is not None:
        CACHE_HITS.inc()

        REQUEST_LATENCY.observe(
            time.perf_counter() - start
        )

        return {
            **cached_result,
            "cached": True
        }

    # Cache miss
    CACHE_MISSES.inc()

    result = await batcher.predict(request.text)

    # Store prediction in Redis
    cache.set(request.text, result)

    REQUEST_LATENCY.observe(
        time.perf_counter() - start
    )

    return {
        **result,
        "cached": False
    }