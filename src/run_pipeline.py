from src.extract_features import extract_features

def run_pipeline(file_path):
    print("✅ Pipeline is running")
    print("File received:", file_path)

    # Call real feature extraction
    features = extract_features(file_path)

    print("Extracted Features:", features)

    return features