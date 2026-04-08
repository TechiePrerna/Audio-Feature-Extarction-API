from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_AUDIO_DIR = BASE_DIR / "data" / "raw_audio"
RESAMPLED_DIR = BASE_DIR / "data" / "resampled"
OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

TARGET_SR = 44100
N_CLUSTERS = 6
PCA_COMPONENTS = 30
RANDOM_STATE = 42
