from fastapi import FastAPI, Response
from transformers import pipeline

app = FastAPI()

pipe = pipeline("text-generation", model="google/flan-t5-small")


# Serve the frontend.html file at the root endpoint
@app.get("/", response_class=Response)
def home():
    with open("frontend.html", "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

@app.get("/generate")
def generate_text(prompt: str):
    result = pipe(prompt, max_length=64, temperature=1.0, num_return_sequences=1)
    # For text-generation pipeline, the output key is usually 'generated_text'
    return {"generated_text": result[0].get("generated_text", result[0])}