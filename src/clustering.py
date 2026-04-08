import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import joblib

from .config import N_CLUSTERS, PCA_COMPONENTS, RANDOM_STATE, MODELS_DIR

def fit_cluster_pipeline(feature_df):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feature_df)

    n_components = min(PCA_COMPONENTS, X_scaled.shape[0], X_scaled.shape[1])
    pca = PCA(n_components=n_components, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_scaled)

    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=RANDOM_STATE, n_init=10)
    clusters = kmeans.fit_predict(X_pca)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, MODELS_DIR / "scaler.joblib")
    joblib.dump(pca, MODELS_DIR / "pca.joblib")
    joblib.dump(kmeans, MODELS_DIR / "kmeans.joblib")

    pca_cols = [f"PC{i+1}" for i in range(X_pca.shape[1])]
    pca_df = pd.DataFrame(X_pca, columns=pca_cols)
    return clusters, pca_df

def infer_cluster_names(df, feature_cols):
    summary = df.groupby("cluster_id")[feature_cols].mean(numeric_only=True)

    f0_cols = [c for c in feature_cols if "F0" in c or "f0" in c]
    loud_cols = [c for c in feature_cols if "loudness" in c.lower()]
    jitter_cols = [c for c in feature_cols if "jitter" in c.lower()]
    shimmer_cols = [c for c in feature_cols if "shimmer" in c.lower()]
    hnr_cols = [c for c in feature_cols if "hnr" in c.lower()]

    scores = []
    for cid in summary.index:
        row = summary.loc[cid]
        f0 = row[f0_cols].mean() if f0_cols else 0
        loud = row[loud_cols].mean() if loud_cols else 0
        jitter = row[jitter_cols].mean() if jitter_cols else 0
        shimmer = row[shimmer_cols].mean() if shimmer_cols else 0
        hnr = row[hnr_cols].mean() if hnr_cols else 0
        scores.append({
            "cluster_id": cid, "f0": f0, "loudness": loud,
            "jitter": jitter, "shimmer": shimmer, "hnr": hnr
        })

    score_df = pd.DataFrame(scores).set_index("cluster_id") if scores else pd.DataFrame()

    name_map = {}
    if not score_df.empty:
        remaining = set(score_df.index)

        normal_id = score_df["hnr"].idxmax()
        name_map[normal_id] = "normal"
        remaining.discard(normal_id)

        if remaining:
            dep_id = score_df.loc[list(remaining), "loudness"].idxmin()
            name_map[dep_id] = "depression_like"
            remaining.discard(dep_id)

        if remaining:
            anx_id = score_df.loc[list(remaining), "jitter"].idxmax()
            name_map[anx_id] = "anxiety_like"
            remaining.discard(anx_id)

        if remaining:
            sui_id = score_df.loc[list(remaining), "hnr"].idxmin()
            name_map[sui_id] = "suicidal_like"
            remaining.discard(sui_id)

        if remaining:
            stress_id = score_df.loc[list(remaining), "shimmer"].idxmax()
            name_map[stress_id] = "stress_like"
            remaining.discard(stress_id)

        for cid in remaining:
            name_map[cid] = "bipolar_like"

    return name_map, score_df
