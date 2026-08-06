from fastapi import FastAPI
from pydantic import BaseModel
from app.model import SentimentModel

app = FastAPI()

# Load model once at startup, not per-request
model = SentimentModel()

class PredictRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "ML Inference Platform is running!"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}

@app.post("/predict")
def predict(request: PredictRequest):
    result = model.predict(request.text)
    return result