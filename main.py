from fastapi import FastAPI, UploadFile, File
import shutil
import os
import pandas as pd

from src.run_pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Voice Feature Engine API Running"}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):

    # Save uploaded file
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run pipeline
    result = run_pipeline(file_path)

  
    if "error" in result:
        return {
            "status": "failed",
            "output": result
        }

    # Convert to DataFrame
    df = pd.DataFrame([result])

    # Save features to CSV
    output_file = "output_features.csv"

    
    if os.path.exists(output_file):
        df.to_csv(output_file, mode='a', header=False, index=False)
    else:
        df.to_csv(output_file, index=False)

    # Optional: delete temp file
    os.remove(file_path)

    return {
        "status": "success",
        "message": "Features extracted & saved",
        "output": result
    }