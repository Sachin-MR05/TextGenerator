from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipe = None


def get_pipe():
    global pipe
    if pipe is None:
        last_error = None
        for task in ("text2text-generation", "text-generation"):
            try:
                pipe = pipeline(task, model="google/flan-t5-small")
                break
            except Exception as exc:
                last_error = exc
        if pipe is None:
            raise RuntimeError(f"Could not initialize pipeline: {last_error}")
    return pipe


# Serve the frontend.html file at the root endpoint
@app.get("/", response_class=Response)
def home():
    with open("frontend.html", "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")


@app.get("/generate")
def generate_text(prompt: str):
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    try:
        result = get_pipe()(prompt, max_new_tokens=64, num_return_sequences=1)
        text = result[0].get("generated_text") or result[0].get("summary_text") or str(result[0])
        return {"generated_text": text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Text generation failed: {exc}")
