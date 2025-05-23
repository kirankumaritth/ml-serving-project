from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response

REQUEST_COUNT = Counter("request_count", "App Request Count", ['app_name', 'endpoint'])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels('ml-serving', request.url.path).inc()
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import threading

app = FastAPI()

status = "NOT_DEPLOYED"
model_id = None
model_pipeline = None

class CompletionRequest(BaseModel):
    messages: list

@app.post("/model")
def deploy_model(data: dict):
    global model_id, model_pipeline, status

    try:
        requested_model = data.get("model_id", "")
        if not requested_model:
            raise ValueError("Model ID not provided.")

        status = "DEPLOYING"
        
        def load_model():
            global model_pipeline, status, model_id
            try:
                model_pipeline = pipeline("text-generation", model=requested_model)
                model_id = requested_model
                status = "RUNNING"
            except Exception as e:
                print(f"Model loading error: {e}")
                status = "NOT_DEPLOYED"
        
        thread = threading.Thread(target=load_model)
        thread.start()

        return {"status": "success", "model_id": requested_model}

    except Exception as e:
        status = "NOT_DEPLOYED"
        return {"status": "error", "message": str(e)}

@app.get("/status")
def get_status():
    return {"status": status}

@app.get("/model")
def get_model():
    return {"model_id": model_id or "None"}

@app.post("/completion")
def generate_completion(request: CompletionRequest):
    if status != "RUNNING":
        raise HTTPException(status_code=400, detail="Model is not running")
    
    user_msg = request.messages[0]["content"]
    result = model_pipeline(user_msg, max_length=50, num_return_sequences=1)
    
    return {
        "status": "success",
        "response": [{"role": "assistant", "message": result[0]['generated_text']}]
    }
