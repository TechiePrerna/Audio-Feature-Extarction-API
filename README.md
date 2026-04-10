# Mental Health Voice Feature Extraction Engine

A local, reusable pipeline and REST API for extracting acoustic features from voice audio and predicting mental health condition groups using unsupervised clustering.

> **Important:** The 6 output classes are **cluster interpretations**, not clinical diagnoses. They are unsupervised groups inferred from acoustic patterns only.

---

## Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Setup](#setup)
- [How to Run the Pipeline](#how-to-run-the-pipeline)
- [How to Run the API](#how-to-run-the-api)
- [API Endpoints](#api-endpoints)
  - [GET /](#get-)
  - [POST /extract](#post-extract)
  - [GET /features/{file_id}](#get-featuresfile_id)
- [Authentication](#authentication)
- [Testing with Curl](#testing-with-curl)
- [Testing with Python](#testing-with-python)
- [Outputs](#outputs)
- [Cluster Labels](#cluster-labels)

---

## Overview

This engine does the following:

1. Accepts `.wav` audio files via API or local folder
2. Resamples audio to 44100 Hz
3. Extracts OpenSMILE ComParE 2016 functionals (6000+ features per file)
4. Saves features as CSV and JSON
5. Applies scaling, PCA, and K-Means clustering
6. Assigns each audio file to a mental health condition group

---

## Folder Structure

```text
MentalHealthVoiceEngine/
├── data/
│   ├── raw_audio/          ← place your .wav files here
│   └── resampled/          ← auto-generated resampled files
├── logs/
│   └── failed_files.csv    ← files that failed during processing
├── models/
│   ├── scaler.joblib
│   ├── pca.joblib
│   └── kmeans.joblib
├── output/
│   ├── features_compare_2016.csv
│   ├── features_scaled.csv
│   ├── features_pca.csv
│   ├── clustered_results.csv
│   ├── cluster_summary.csv
│   ├── cluster_feature_scores.csv
│   └── cluster_plot.png
├── src/
│   ├── preprocess.py
│   ├── extract_features.py
│   └── config.py
├── api.py                  ← FastAPI server
├── run_pipeline.py         ← full batch pipeline
├── requirements.txt
└── .env                    ← API key (never push to GitHub)
```

---

## Setup

### Requirements
- Python 3.10 or 3.11
- Conda or virtualenv

### Install

```bash
# Step 1 - Clone the repo
git clone https://github.com/YOUR_USERNAME/MentalHealthVoiceEngine.git
cd MentalHealthVoiceEngine

# Step 2 - Create and activate environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Step 3 - Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root folder:

```env
API_KEY=your_secret_key_here
```

> Never push `.env` to GitHub. It is listed in `.gitignore`.

---

## How to Run the Pipeline

Place all `.wav` files in `data/raw_audio/` then run:

```bash
python run_pipeline.py
```

This will resample, extract features, cluster, and save all outputs automatically.

---

## How to Run the API

```bash
uvicorn api:app --reload --port 8013
```

Server will start at:
```
http://127.0.0.1:8013
```

Interactive Swagger docs available at:
```
http://127.0.0.1:8013/docs
```

---

## API Endpoints

### GET /

Health check — confirms the API is running.

**Authentication:** Not required

**Request:**
```
GET http://127.0.0.1:8013/
```

**Response:**
```json
{
  "message": "API is running successfully"
}
```

---

### POST /extract

Uploads a `.wav` audio file, extracts acoustic features, and saves them as CSV and JSON.

**Authentication:** Required — pass API key in header as `x-api-key`

**Input:**
| Field | Type | Required | Description |
|---|---|---|---|
| file | .wav file | Yes | Audio file to analyse |
| x-api-key | string (header) | Yes | Your API key from .env |

**Response:**
| Field | Type | Description |
|---|---|---|
| status | string | success or error |
| file_id | string | Unique ID for this upload |
| filename | string | Sanitised filename |
| sampling_rate | int | Target sample rate used |
| feature_count | int | Number of features extracted |
| csv_saved_to | string | Path to saved CSV file |
| json_saved_to | string | Path to saved JSON file |
| features | object | All extracted feature values |

**Example Response:**
```json
{
  "status": "success",
  "file_id": "6428c45b",
  "filename": "sample_audio.wav",
  "sampling_rate": 44100,
  "feature_count": 6373,
  "csv_saved_to": "output/6428c45b_features.csv",
  "json_saved_to": "output/6428c45b_features.json",
  "features": {
    "mfcc_1": -243.56,
    "mfcc_2": 87.34,
    "pitch_mean": 187.43,
    "energy_rms": 0.032,
    "zcr_mean": 0.085
  }
}
```

---

### GET /features/{file_id}

Retrieves previously extracted features for a given file ID.

**Authentication:** Required — pass API key in header as `x-api-key`

**Input:**
| Field | Type | Required | Description |
|---|---|---|---|
| file_id | string (path) | Yes | The file_id returned from POST /extract |
| x-api-key | string (header) | Yes | Your API key from .env |

**Response:**
```json
{
  "status": "success",
  "file_id": "6428c45b",
  "features": {
    "mfcc_1": -243.56,
    "mfcc_2": 87.34,
    "pitch_mean": 187.43,
    "energy_rms": 0.032,
    "zcr_mean": 0.085
  }
}
```

**Error Response (file not found):**
```json
{
  "detail": "Feature output not found"
}
```

---

## Authentication

All endpoints except `GET /` require an API key passed as a request header:

```
x-api-key: your_secret_key_here
```

If the key is missing or wrong, the API returns:
```json
{
  "detail": "Unauthorized"
}
```

---

## Testing with Curl

### Check API is running
```bash
curl -X GET "http://127.0.0.1:8013/"
```

### Extract features from audio file
```bash
curl -X POST "http://127.0.0.1:8013/extract" \
  -H "x-api-key: your_secret_key_here" \
  -F "file=@C:/path/to/your/audio.wav"
```

### Retrieve features by file ID
```bash
curl -X GET "http://127.0.0.1:8013/features/6428c45b" \
  -H "x-api-key: your_secret_key_here"
```

---

## Testing with Python

```python
import requests

API_URL = "http://127.0.0.1:8013"
API_KEY = "your_secret_key_here"
HEADERS = {"x-api-key": API_KEY}

# Step 1 - Extract features
with open("your_audio.wav", "rb") as f:
    files = {"file": ("audio.wav", f, "audio/wav")}
    response = requests.post(f"{API_URL}/extract", headers=HEADERS, files=files)

result = response.json()
print("Status :", result["status"])
print("File ID :", result["file_id"])
print("Features:", result["feature_count"])

# Step 2 - Retrieve features later using file_id
file_id = result["file_id"]
response2 = requests.get(f"{API_URL}/features/{file_id}", headers=HEADERS)
print(response2.json())
```

---

## Outputs

### Pipeline outputs saved in `output/`

| File | Description |
|---|---|
| features_compare_2016.csv | Raw extracted features for all audio files |
| features_scaled.csv | Normalised feature values |
| features_pca.csv | PCA-reduced features |
| clustered_results.csv | Each file with its assigned cluster label |
| cluster_summary.csv | Summary statistics per cluster |
| cluster_feature_scores.csv | Top features per cluster |
| cluster_plot.png | 2D PCA scatter plot of clusters |

### API outputs saved in `output/`

| File | Description |
|---|---|
| {file_id}_features.csv | Features for that specific uploaded file |
| {file_id}_features.json | Same features in JSON format for model input |

### Model artifacts saved in `models/`

| File | Description |
|---|---|
| scaler.joblib | Fitted StandardScaler |
| pca.joblib | Fitted PCA transformer |
| kmeans.joblib | Fitted K-Means clustering model |

---

## Cluster Labels

The pipeline groups audio into 6 clusters based on acoustic patterns:

| Cluster | Label | Acoustic Pattern |
|---|---|---|
| 0 | normal | Balanced pitch, energy, and speech rate |
| 1 | depression_like | Low energy, flat pitch, slow speech |
| 2 | anxiety_like | High pitch, fast speech, high ZCR |
| 3 | stress_like | High energy, irregular pitch, tense voice |
| 4 | bipolar_like | Highly variable pitch and energy |
| 5 | suicidal_like | Very low energy, monotone, long pauses |

> These labels are acoustic cluster interpretations only and should not be used for clinical assessment or diagnosis.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| OpenSMILE | Feature extraction (ComParE 2016) |
| Librosa | Audio loading and preprocessing |
| Scikit-learn | Scaling, PCA, K-Means clustering |
| Pandas | Data handling |
| Python-dotenv | API key management |

---

## Author

Built as part of a Voice-Based Mental Health Prediction System research project.


