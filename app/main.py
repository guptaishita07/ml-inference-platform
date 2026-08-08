from fastapi import FastAPI
from pydantic import BaseModel

from app.model import SentimentModel
from app.batcher import DynamicBatcher
from app.cache import PredictionCache

# Create FastAPI app
app = FastAPI()

# Initialize shared components
model = SentimentModel()
batcher = DynamicBatcher(model, batch_size=8, max_wait_ms=50)
cache = PredictionCache()


class PredictRequest(BaseModel):
    text: str


@app.on_event("startup")
async def startup():
    batcher.start()


@app.get("/")
def root():
    return {"message": "ML Inference Platform is running!"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True
    }


@app.post("/predict")
async def predict(request: PredictRequest):

    # Check Redis cache first
    cached_result = cache.get(request.text)

    if cached_result is not None:
        return {
            **cached_result,
            "cached": True
        }

    # Cache miss -> use dynamic batcher
    result = await batcher.predict(request.text)

    # Store result in Redis
    cache.set(request.text, result)

    return {
        **result,
        "cached": False
    }