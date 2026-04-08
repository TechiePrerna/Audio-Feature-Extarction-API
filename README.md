# Mental Health Voice Feature Extraction Engine

Local, reusable pipeline for:
1. reading `.wav` files from `data/raw_audio/`
2. resampling them to 44100 Hz
3. extracting OpenSMILE ComParE 2016 functionals
4. saving features locally
5. clustering into 6 groups:
   - normal
   - depression_like
   - anxiety_like
   - stress_like
   - bipolar_like
   - suicidal_like

## Important note
The 6 output classes are **cluster interpretations**, not clinical diagnoses.
They are unsupervised groups inferred from acoustic patterns.

## Folder structure
```text
MentalHealthVoiceEngine/
├── data/
│   ├── raw_audio/
│   └── resampled/
├── logs/
├── models/
├── output/
├── src/
├── requirements.txt
└── run_pipeline.py
```

## Setup
1. Install Python 3.10 or 3.11
2. Open terminal in this project folder
3. Create venv (recommended)

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## How to use
1. Put all `.wav` files in `data/raw_audio/`
2. Run:
```bash
python run_pipeline.py
```

## Outputs
Saved in `output/`:
- `features_compare_2016.csv`
- `features_scaled.csv`
- `features_pca.csv`
- `clustered_results.csv`
- `cluster_summary.csv`
- `cluster_feature_scores.csv`
- `cluster_plot.png`

Saved in `models/`:
- `scaler.joblib`
- `pca.joblib`
- `kmeans.joblib`

Saved in `logs/`:
- `failed_files.csv`
