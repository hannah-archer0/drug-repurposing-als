This folder should contain the raw input datasets required for the dara preprocessing pipeline.

**⚠️ Raw data is NOT included in this repository due to licensing restrictions.**

---

## Required Files

### 1. `ALS_genes.csv`
- **Source**: DisGeNET  
- **Download**: https://www.disgenet.org/downloads  
- **Description**: Gene-disease associations including ALS-associated genes  
- **Put here**: `data/raw/ALS_genes.csv`

### 2. `full_database.xml`
- **Source**: DrugBank (requires free academic registration)  
- **Download**: https://go.drugbank.com/releases/latest  
- **Description**: Full XML file of drug-target interactions  
- **Put here**: `data/raw/full_database.xml`

---

## Notes
- These files are used as inputs for the script: `src/data_prep.py`
- SMILES strings are later retrieved via the PubChemPy API, so no manual download of those is required.
