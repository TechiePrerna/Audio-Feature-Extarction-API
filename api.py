from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import pandas as pd
import uuid
import os
import json
from dotenv import load_dotenv

# Import your engine modules
from src.preprocess import resample_audio
from src.extract_features import extract_features
from src.config import RAW_AUDIO_DIR, RESAMPLED_DIR, TARGET_SR

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Mental Health Voice Feature Extraction API")

# Ensure folders exist
RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
RESAMPLED_DIR.mkdir(parents=True, exist_ok=True)
Path("output").mkdir(parents=True, exist_ok=True)

# 🔐 API Key verification
def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Home route
@app.get("/")
def home():
    return {"message": "API is running successfully 🚀"}

# Feature extraction endpoint
@app.post("/extract")
async def extract_audio(
    file: UploadFile = File(...),
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)

    try:
        # Validate file type
        if not file.filename.endswith(".wav"):
            raise HTTPException(status_code=400, detail="Only .wav files allowed")

        # Unique file name
        file_id = str(uuid.uuid4())[:8]
        safe_name = file.filename.replace(" ", "_")

        raw_path = RAW_AUDIO_DIR / f"{file_id}_{safe_name}"
        resampled_path = RESAMPLED_DIR / f"{file_id}_{safe_name}"

        # Save uploaded file
        with open(raw_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Preprocess (resample)
        resample_audio(raw_path, resampled_path, target_sr=TARGET_SR)

        # Extract features
        features = extract_features(resampled_path)
        feature_dict = features.to_dict()

        # Save CSV (existing behavior)
        csv_path = Path("output") / f"{file_id}_features.csv"
        pd.DataFrame([feature_dict]).to_csv(csv_path, index=False)

        # Save JSON output for model-ready retrieval
        json_path = Path("output") / f"{file_id}_features.json"
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(feature_dict, jf)

        return JSONResponse({
            "status": "success",
            "file_id": file_id,
            "filename": safe_name,
            "sampling_rate": TARGET_SR,
            "feature_count": len(feature_dict),
            "csv_saved_to": str(csv_path),
            "json_saved_to": str(json_path),
            "features": feature_dict
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)


# Feature retrieval endpoint (JSON output for model input)
@app.get("/features/{file_id}")
def get_features(file_id: str, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    json_path = Path("output") / f"{file_id}_features.json"
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Feature output not found")

    with open(json_path, "r", encoding="utf-8") as jf:
        feature_json = json.load(jf)
    return JSONResponse({
        "status": "success",
        "file_id": file_id,
        "features": feature_json
    })


if __name__ == "__main__":
    import uvicorn

    # Helpful for starting the server directly with `python Api.py`
    uvicorn.run("Api:app", host="0.0.0.0", port=8013, reload=True)
