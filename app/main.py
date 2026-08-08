from fastapi import FastAPI
from pydantic import BaseModel

from app.model import SentimentModel
from app.batcher import DynamicBatcher

app = FastAPI()

model = SentimentModel()
batcher = DynamicBatcher(model, batch_size=8, max_wait_ms=50)


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
    return {"status": "ok", "model_loaded": True}


@app.post("/predict")
async def predict(request: PredictRequest):
    return await batcher.predict(request.text)