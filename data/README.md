# 📂 Data Directory

This folder contains the raw and processed datasets used in the project:  
**Cheminformatics-Based Drug Repurposing for ALS using Random Forest Classifier and GAN Model**

Due to licensing restrictions, raw files from DisGeNET, DrugBank, and PubChem are **not included** in this repository. This README provides instructions for how to manually download and preprocess the data.

---

## 📁 Folder Structure
data/
├── raw/            # Original downloaded data (NOT committed to GitHub)
├── processed/      # Cleaned data used for ML models
└── README.md       # This file

---

## 🔗 Data Sources and Download Instructions

### 1. **DisGeNET** – ALS-Associated Genes

- **Source**: [https://www.disgenet.org/](https://www.disgenet.org/)
- **File to download**: `all_gene_disease_associations.tsv`
- **Steps**:
  1. Register/login to DisGeNET.
  2. Navigate to the downloads page.
  3. Download `all_gene_disease_associations.tsv`.
  4. Place it in: `data/raw/`.

### 2. **DrugBank** – Drug-Target Interactions

- **Source**: [https://www.drugbank.ca/releases/latest](https://www.drugbank.ca/releases/latest)
- **File to download**: `full database XML` (requires free academic registration)
- **Steps**:
  1. Create a free academic account on DrugBank.
  2. Download the XML version of the full database.
  3. Place the file in: `data/raw/`.

### 3. **PubChem** – Molecular Structures

- **Source**: [https://pubchem.ncbi.nlm.nih.gov/](https://pubchem.ncbi.nlm.nih.gov/)
- **Accessed via**: Python library [`PubChemPy`](https://pubchempy.readthedocs.io/en/latest/)
- **Notes**: You do not need to manually download SMILES strings; the `src/data_prep.py` script queries PubChem directly using PubChemPy based on DrugBank IDs.

---

## 🧪 Processed Data

Once you’ve downloaded the raw data and run the preprocessing scripts (`data_prep.py` and `encode_fps.py`), the following files will be created in `data/processed/`:

- `als_fingerprints.csv` – Morgan fingerprints of known ALS drugs
- `non_als_fingerprints.csv` – Morgan fingerprints of negative (random) drug samples
- `labels.csv` – Binary classification labels (1 = ALS, 0 = non-ALS)

These files serve as input to the classifier and GAN training steps.

---

## 🔁 Reproducibility

After placing the downloaded raw files in `data/raw/`, run the following scripts to reproduce the processed dataset:

```bash
python src/data_prep.py       # Filters ALS drugs and fetches SMILES
python src/encode_fps.py      # Generates Morgan fingerprints
