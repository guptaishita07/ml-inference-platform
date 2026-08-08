from transformers import pipeline

class SentimentModel:
    def __init__(self):
        self.pipe = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def predict(self, text: str) -> dict:
        result = self.pipe(text)[0]
        return {"label": result["label"], "score": result["score"]}

    def predict_batch(self, texts: list[str]) -> list[dict]:
        results = self.pipe(texts)
        return [
                {"label": r["label"], "score": r["score"]}
                for r in results
            ]