from .extract_features import extract_features
import os

def run_pipeline(file_path):
    print("API Pipeline running")
    print("File:", file_path)

    # Check file exists
    if not os.path.exists(file_path):
        print("File not found")
        return {"error": "File not found"}

    try:
        # Extract features directly
        features = extract_features(file_path)

        if not features:
            print("No features extracted")
            return {"error": "Feature extraction failed"}

        print("Features extracted:", len(features))

        return features

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}