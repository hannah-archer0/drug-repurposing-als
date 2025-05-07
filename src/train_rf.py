import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# === Paths ===
DATA_DIR = "data/processed"
OUTPUT_DIR = "outputs/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

X_pos = np.load(os.path.join(DATA_DIR, "als_fingerprints.npy"))
X_neg = np.load(os.path.join(DATA_DIR, "non_als_fingerprints.npy"))
y = np.load(os.path.join(DATA_DIR, "labels.npy"))

X = np.vstack([X_pos, X_neg])
# y already combined

# === Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# === Train Classifier ===
clf = RandomForestClassifier(
    n_estimators=100, class_weight="balanced", random_state=42
)
clf.fit(X_train, y_train)

# === Evaluate ===
y_pred = clf.predict(X_test)
report = classification_report(y_test, y_pred, digits=4)
print(report)

# Save report
with open(os.path.join(OUTPUT_DIR, "rf_classification_report.txt"), "w") as f:
    f.write(report)

# === Feature Importance Plot ===
importances = clf.feature_importances_
top_indices = np.argsort(importances)[-20:][::-1]

plt.figure(figsize=(10, 6))
sns.barplot(x=top_indices, y=importances[top_indices])
plt.title("Top 20 Important Fingerprint Bits")
plt.xlabel("Fingerprint Bit Index")
plt.ylabel("Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "rf_feature_importance.png"))

print("✓ Random Forest trained and evaluated.")
print(f"✓ Feature importance plot saved to: {OUTPUT_DIR}/rf_feature_importance.png")
