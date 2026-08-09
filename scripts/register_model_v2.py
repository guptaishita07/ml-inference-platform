import mlflow
import mlflow.transformers
from transformers import pipeline

mlflow.set_tracking_uri("http://localhost:5001")
mlflow.set_experiment("sentiment-classifier")

with mlflow.start_run(run_name="sentiment-classifier-v2"):
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    mlflow.transformers.log_model(
        transformers_model=classifier,
        artifact_path="model",
        registered_model_name="sentiment-classifier"
    )

    print("Model v2 registered successfully")