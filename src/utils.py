from pathlib import Path
import pandas as pd

def ensure_dirs(paths):
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)

def save_failed_files(failed_rows, path):
    df = pd.DataFrame(failed_rows, columns=["filename", "error"])
    df.to_csv(path, index=False)

def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
