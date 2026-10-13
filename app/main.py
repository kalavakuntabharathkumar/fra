import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import redis
from .model import load_or_train, features
from .schemas import Transaction, ScoreResponse
from .storage import initialize, save_score

MODEL_VERSION = "demo-rf-v1"
MODEL_PATH = os.getenv("MODEL_PATH", "models/fraud_model.joblib")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
model = None
cache = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, cache
    model = load_or_train(MODEL_PATH)
    try:
        cache = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)
        cache.ping()
    except Exception:
        cache = None
    initialize()
    yield

app = FastAPI(title="ML Fraud Scoring API", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None, "cache_enabled": cache is not None}

@app.post("/v1/score", response_model=ScoreResponse)
def score(tx: Transaction):
    if model is None:
        raise HTTPException(status_code=503, detail="model is not ready")
    key = f"fraud-score:{tx.transaction_id}"
    if cache:
        try:
            cached = cache.get(key)
            if cached:
                data = json.loads(cached)
                data["cached"] = True
                return data
        except Exception:
            pass
    probability = float(model.predict_proba(features(tx))[0][1])
    decision = "review" if probability >= 0.35 else "approve"
    result = {
        "transaction_id": tx.transaction_id,
        "fraud_probability": round(probability, 6),
        "decision": decision,
        "model_version": MODEL_VERSION,
        "cached": False,
    }
    if cache:
        try:
            cache.setex(key, 300, json.dumps(result))
        except Exception:
            pass
    save_score(tx, result["fraud_probability"], decision, MODEL_VERSION)
    return result
