---
title: Text Generator
emoji: memo
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: app.py
pinned: false
---

# Text Generator

FastAPI + Transformers text generation app for Hugging Face Spaces.
# Text Generator

A simple web application that generates text based on a user prompt using the `google/flan-t5-small` model from Hugging Face Transformers.

## Demo

Experience the live demo here: [https://huggingface.co/spaces/mr-sachin/TextGenerator](https://huggingface.co/spaces/mr-sachin/TextGenerator)

## Screenshot

![Text Generator Interface](image.png)

## Code Explanation

This project consists of the following key files:

### `app.py`
This is the main FastAPI application.
- **Model Loading**: It initializes a text generation pipeline using the `google/flan-t5-small` model. The `get_pipe()` function ensures the model is loaded only once (singleton pattern).
- **Frontend Serving**: The root endpoint (`/`) serves the `frontend.html` file.
- **Text Generation**: The `/generate` endpoint accepts a prompt via query parameter, runs it through the model pipeline, and returns the generated text in JSON format.
- **CORS**: Cross-Origin Resource Sharing (CORS) is enabled to allow requests from different origins if needed.

### `frontend.html`
This file contains the user interface for the application.
- **Structure**: It provides a simple form with a textarea for the prompt and a "Generate" button.
- **Styling**: Basic CSS is included to style the container, form elements, and result display.
- **Logic**: JavaScript handles the form submission. It sends an asynchronous fetch request to the `/generate` endpoint with the user's prompt and updates the result area with the generated text or any error messages.

### `Dockerfile`
The Dockerfile defines the environment for running the application.
- **Base Image**: Uses `python:3.10-slim` for a lightweight Python environment.
- **Dependencies**: Copies `requirements.txt` and installs the necessary Python packages.
- **Application Code**: Copies the source code into the container.
- **Execution**: Exposes port `7860` and starts the FastAPI app using Uvicorn (`uvicorn app:app --host 0.0.0.0 --port 7860`).

### `requirements.txt`
Lists the Python libraries required for the project, including:
- `fastapi` and `uvicorn`: For the web framework and server.
- `transformers` and `torch`: For loading and running the machine learning model.
- `requests`: For making HTTP requests (if needed).

## GitHub Actions

The project includes a GitHub Actions workflow to automate deployment to Hugging Face Spaces.

### `.github/workflows/deploy-to-huggingface.yml`
This workflow is triggered on every push to the `main` branch.

**Steps:**
1.  **Checkout repository**: Uses `actions/checkout@v4` to clone the code.
2.  **Set up Python**: Uses `actions/setup-python@v5` to install Python 3.10.
3.  **Install Hugging Face CLI**: Upgrades pip and installs the `huggingface_hub` library with CLI support.
4.  **Push to Hugging Face Spaces**:
    - Authenticates using the `HF_TOKEN` secret.
    - Creates the Space (if it doesn't exist) using the `HF_SPACE_NAME` secret.
    - Uploads the files to the Hugging Face Space using `hf upload`, excluding git and github metadata files.
