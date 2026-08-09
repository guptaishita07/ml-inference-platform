import mlflow
import mlflow.pyfunc

mlflow.set_tracking_uri("http://localhost:5001")

class VersionedModel:
    def __init__(self):
        self._cache = {}  # version -> loaded model, avoid reloading every request

    def get(self, version: str):
        if version not in self._cache:
            model_uri = f"models:/sentiment-classifier/{version}"
            self._cache[version] = mlflow.pyfunc.load_model(model_uri)
        return self._cache[version]

    def predict(self, version: str, text: str) -> dict:
        model = self.get(version)
        result = model.predict([text])
        row = result.iloc[0]
        return {"label": row["label"], "score": float(row["score"])}