from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import make_asgi_app
import time

from app.model import SentimentModel
from app.batcher import DynamicBatcher
from app.cache import PredictionCache
from app.model_registry import VersionedModel

from app.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    CACHE_HITS,
    CACHE_MISSES,
)


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# Prometheus metrics
# --------------------------------------------------

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# --------------------------------------------------
# Existing inference components
# --------------------------------------------------

model = SentimentModel()

batcher = DynamicBatcher(
    model=model,
    batch_size=8,
    max_wait_ms=50,
)

cache = PredictionCache()


# --------------------------------------------------
# MLflow model registry
# --------------------------------------------------

versioned_model = VersionedModel()


# --------------------------------------------------
# Request schema
# --------------------------------------------------

class PredictRequest(BaseModel):
    text: str


# --------------------------------------------------
# Startup
# --------------------------------------------------

@app.on_event("startup")
async def startup():
    batcher.start()


# --------------------------------------------------
# Health / root endpoints
# --------------------------------------------------

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


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.post("/predict")
async def predict(
    request: PredictRequest,
    version: str = "1",
):
    start = time.perf_counter()

    REQUEST_COUNT.inc()

    # --------------------------------------------------
    # Version-aware cache key
    # --------------------------------------------------

    cache_key = f"{version}:{request.text}"

    # --------------------------------------------------
    # Check Redis cache
    # --------------------------------------------------

    cached_result = cache.get(cache_key)

    if cached_result is not None:

        CACHE_HITS.inc()

        REQUEST_LATENCY.observe(
            time.perf_counter() - start
        )

        return {
            **cached_result,
            "version": version,
            "cached": True
        }

    # --------------------------------------------------
    # Cache miss
    # --------------------------------------------------

    CACHE_MISSES.inc()

    # --------------------------------------------------
    # Run MLflow versioned model
    # --------------------------------------------------

    result = versioned_model.predict(
        version,
        request.text
    )

    # --------------------------------------------------
    # Store result in Redis
    # --------------------------------------------------

    cache.set(
        cache_key,
        result
    )

    # --------------------------------------------------
    # Record latency
    # --------------------------------------------------

    REQUEST_LATENCY.observe(
        time.perf_counter() - start
    )

    return {
        **result,
        "version": version,
        "cached": False
    }