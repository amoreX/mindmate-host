from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers.pipelines import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

app = FastAPI();



# Request body structure
class Prompt(BaseModel):
    prompt: str

#mood label map
label_map = {
    0: "normal",
    1: "bipolar",
    2: "anxiety",
    3: "suicidal",
    4: "depression"
}

# Load model and tokenizer
model_path = "./mental_health_bud"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Create pipeline
device = 0 if torch.cuda.is_available() else -1
pipe_budy = pipeline("text-classification", model=model, tokenizer=tokenizer, device=device)


# Helper to interpret output
def interpret_output(output):
    label_str = output[0]['label']
    label_index = int(label_str.replace("LABEL_", ""))
    return {
        "label": label_map.get(label_index, "Unknown"),
        "score": round(output[0]['score'], 4)
    }


# Root endpoint
@app.get("/")
def index():
    return {"message": "Mental Health Inference API"}

# Prediction endpoint
@app.post("/predict")
def predict(data: Prompt):
    try:
        raw_output = pipe_budy(data.prompt)
        result = interpret_output(raw_output)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
