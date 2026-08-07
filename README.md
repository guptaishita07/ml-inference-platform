# ML Inference Platform

A production-inspired machine learning inference platform built with FastAPI, Docker, Redis, Prometheus, and MLflow.

## Features (Planned)

- FastAPI inference API
- Dynamic request batching
- Redis caching
- Prometheus metrics
- Grafana dashboards
- MLflow model versioning
- Docker deployment
- Kubernetes autoscaling

## Tech Stack

- Python
- FastAPI
- Hugging Face Transformers
- Docker
- Redis
- Prometheus
- Grafana
- MLflow

## Project Roadmap

- [x] Repository setup
- [ ] Phase 1 – Inference Server
- [ ] Phase 2 – Dynamic Batching
- [ ] Phase 3 – Redis Cache
- [ ] Phase 4 – Monitoring
- [ ] Phase 5 – Model Versioning
- [ ] Phase 6 – Load Testing
- [ ] Phase 7 – Kubernetes Deployment

## Local Setup
\```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
\```

## Example
\```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"I love this"}'

# {"label":"POSITIVE","score":0.9998}
\```

## Run with Docker
\```bash
docker build -t ml-inference-platform .
docker run -p 8000:8000 ml-inference-platform
\```