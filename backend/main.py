import os
import shutil
import tempfile
import time
from typing import Any, Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils import predict_image

app = FastAPI(title="Farm Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}")


@app.on_event("startup")
async def startup_event():
    log("Backend starting up... Model will be loaded lazily from utils.py")
    log("Backend ready to receive requests.")


@app.get("/")
async def root():
    return {"status": "ok", "service": "Farm Advisor API"}


@app.post("/analyze")
async def analyze_field(file: UploadFile = File(...)) -> List[Dict[str, Any]]:
    start_time = time.time()
    original_name = file.filename or "upload"
    log(f"Received file: {original_name}")

    if not (file.content_type or "").startswith("image/"):
        log(f"Rejected non-image upload: {file.content_type}")
        raise HTTPException(status_code=400, detail="Only image uploads are supported.")

    suffix = os.path.splitext(original_name)[1]
    temp_file_path = None

    try:
        # Save upload to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            temp_file_path = tmp.name
            shutil.copyfileobj(file.file, tmp)

        log(f"File saved as {temp_file_path}")
        log("🔥 Calling predict_image()")

        results = predict_image(temp_file_path)

        log(
            f"🔥 Prediction returned: {results} "
            f"in {time.time() - start_time:.2f} seconds"
        )

    except Exception as e:
        log(f"Prediction error: {e}")
        results = [
            {
                "label": "Error",
                "score": 0.0,
                "box": [],
                "nutrition": "Unknown",
                "advice": "An error occurred while analyzing the image. "
                          "Please try another image.",
            }
        ]
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                log(f"Temporary file {temp_file_path} removed")
            except Exception as e:
                log(f"Error removing temp file: {e}")

    return results
