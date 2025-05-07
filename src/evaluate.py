import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from rdkit import DataStructs
from rdkit.DataStructs import ExplicitBitVect
import os

# === Paths ===
DATA_DIR = "data/processed"
OUTPUT_DIR = "outputs/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

als_fp = np.load(os.path.join(DATA_DIR, "als_fingerprints.npy"))
nonals_fp = np.load(os.path.join(DATA_DIR, "non_als_fingerprints.npy"))
labels = np.load(os.path.join(DATA_DIR, "labels.npy"))

# === Load GAN-generated fingerprints ===
df_gen = pd.read_csv(os.path.join(DATA_DIR, "GAN_Generated_Fingerprints.csv"))
gan_fp = df_gen.values.astype(int)

# === Re-train Random Forest for prediction ===
X_all = np.vstack([als_fp, nonals_fp])
clf = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
clf.fit(X_all, labels)

# === Predict Synthetic Fingerprints ===
preds = clf.predict(gan_fp)
print(f"✓ RF predicted {np.sum(preds)} out of {len(preds)} GAN compounds as ALS-targeting")

# === Tanimoto Similarity (ALS Drugs) ===
def to_rdkit_fp(array):
    fp = ExplicitBitVect(len(array))
    for i, bit in enumerate(array):
        if bit == 1:
            fp.SetBit(i)
    return fp

gan_rdk = [to_rdkit_fp(fp) for fp in gan_fp]
als_rdk = [to_rdkit_fp(fp) for fp in als_fp]

results = []
for i, gan_fp in enumerate(gan_rdk):
    sims = [DataStructs.TanimotoSimilarity(gan_fp, real_fp) for real_fp in als_rdk]
    top_idx = np.argmax(sims)
    results.append((i, top_idx, sims[top_idx]))

# Save similarity results
df_sim = pd.DataFrame(results, columns=["GAN Index", "Closest ALS Index", "Tanimoto Similarity"])
df_sim.to_csv(os.path.join(DATA_DIR, "GAN_ALS_Similarity.csv"), index=False)
print("✓ Saved GAN-ALS similarity results")

# === Dimensionality Reduction ===
all_fps = np.vstack((als_fp, gan_fp))
labels_plot = ["ALS (Real)"] * len(als_fp) + ["Synthetic (GAN)"] * len(gan_fp)

# PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(all_fps)
plt.figure(figsize=(8,6))
sns.scatterplot(x=pca_result[:,0], y=pca_result[:,1], hue=labels_plot, palette="Set2")
plt.title("PCA: Real ALS vs GAN-Generated Fingerprints")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "pca_real_vs_gan.png"))

# t-SNE
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
tsne_result = tsne.fit_transform(all_fps)
plt.figure(figsize=(8,6))
sns.scatterplot(x=tsne_result[:,0], y=tsne_result[:,1], hue=labels_plot, palette="Set1")
plt.title("t-SNE: Real ALS vs GAN-Generated Fingerprints")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "tsne_real_vs_gan.png"))

print("✓ Saved PCA and t-SNE plots")
