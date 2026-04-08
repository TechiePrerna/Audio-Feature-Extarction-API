import matplotlib.pyplot as plt

def save_cluster_plot(pca_df, clusters, out_path):
    if pca_df.shape[1] < 2:
        return
    plt.figure(figsize=(10, 6))
    plt.scatter(pca_df.iloc[:, 0], pca_df.iloc[:, 1], c=clusters, s=20)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("Cluster Visualization (PCA)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
