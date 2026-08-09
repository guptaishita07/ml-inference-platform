import mlflow
from transformers import pipeline

MLFLOW_URI = "http://localhost:5001"

mlflow.set_tracking_uri(MLFLOW_URI)

mlflow.set_experiment("sentiment-classifier")

with mlflow.start_run() as run:

    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    mlflow.transformers.log_model(
        transformers_model=classifier,
        name="model",
        registered_model_name="sentiment-classifier",
        input_example=["This is a great product!"]
    )

    print("Model registered successfully")
    print(f"Run ID: {run.info.run_id}")