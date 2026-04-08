import opensmile

smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.ComParE_2016,
    feature_level=opensmile.FeatureLevel.Functionals,
)

def extract_features(file_path):
    import os

    print("File path:", file_path)
    print("Exists:", os.path.exists(file_path))

    features = smile.process_file(str(file_path))

    print("Raw Features Shape:", features.shape)

    if features.empty:
        print("OpenSMILE returned EMPTY features")

    return features.iloc[0].to_dict() if not features.empty else {}