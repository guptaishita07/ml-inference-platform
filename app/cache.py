import redis
import hashlib
import json

class PredictionCache:
    def __init__(self, host="localhost", port=6379, ttl_seconds=3600):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.ttl = ttl_seconds

    def _make_key(self, text: str) -> str:
        hashed = hashlib.sha256(text.encode()).hexdigest()
        return f"prediction:{hashed}"

    def get(self, text: str) -> dict | None:
        key = self._make_key(text)
        cached = self.client.get(key)
        if cached:
            return json.loads(cached)
        return None

    def set(self, text: str, result: dict):
        key = self._make_key(text)
        self.client.set(key, json.dumps(result), ex=self.ttl)