import os
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
import pubchempy as pcp
import random

# === Paths ===
INPUT_PATH = "data/processed/ALS_Drugs_With_SMILES.csv"
OUT_DIR = "data/processed"

ALS_FP_FILE = os.path.join(OUT_DIR, "als_fingerprints.npy")
NONALS_FP_FILE = os.path.join(OUT_DIR, "non_als_fingerprints.npy")
LABELS_FILE = os.path.join(OUT_DIR, "labels.npy")

# === Helper Functions ===
def smiles_to_morgan_fp(smiles, radius=2, n_bits=2048):
    try:
        mol = Chem.MolFromSmiles(smiles)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        return np.array(fp)
    except:
        return None

def get_random_nonals_smiles(n=300):
    smiles_list = []
    random_cids = random.sample(range(10000, 500000), n * 2)  # oversample to account for failures
    for cid in random_cids:
        try:
            compound = pcp.Compound.from_cid(cid)
            smiles = compound.isomeric_smiles
            if smiles:
                smiles_list.append(smiles)
            if len(smiles_list) >= n:
                break
        except:
            continue
    return smiles_list

# === Load ALS SMILES ===
print("Loading ALS drugs with SMILES...")
als_df = pd.read_csv(INPUT_PATH)
als_df = als_df.dropna(subset=["SMILES"])
als_fps = als_df["SMILES"].apply(smiles_to_morgan_fp)
als_fps = als_fps.dropna()

X_pos = np.stack(als_fps.values)
y_pos = np.ones(len(X_pos))

print(f"✓ Encoded {len(X_pos)} ALS drugs into fingerprints")

# === Fetch & Encode Non-ALS SMILES ===
print("Fetching non-ALS drug SMILES from PubChem...")
nonals_smiles = get_random_nonals_smiles(n=300)
nonals_fps = [smiles_to_morgan_fp(smi) for smi in nonals_smiles]
nonals_fps = [fp for fp in nonals_fps if fp is not None]

X_neg = np.stack(nonals_fps)
y_neg = np.zeros(len(X_neg))

print(f"✓ Encoded {len(X_neg)} non-ALS drugs into fingerprints")

# === Combine & Save ===
X_all = np.vstack([X_pos, X_neg])
y_all = np.concatenate([y_pos, y_neg])

np.save(ALS_FP_FILE, X_pos)
np.save(NONALS_FP_FILE, X_neg)
np.save(LABELS_FILE, y_all)

print(f"\n✓ Saved:")
print(f"- ALS fingerprints: {ALS_FP_FILE}")
print(f"- Non-ALS fingerprints: {NONALS_FP_FILE}")
print(f"- Labels: {LABELS_FILE}")
