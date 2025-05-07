# 📁 data/raw/

This folder holds the raw input datasets required for the drug repurposing pipeline.

⚠️ **Note:** These files are **not included** in the repository due to licensing restrictions.

---

## Required Files

### `ALS_genes.csv`
- **Source**: [DisGeNET Downloads](https://www.disgenet.org/downloads)
- **Dataset**: All gene-disease associations (or filtered for ALS)
- **Purpose**: Contains ALS-associated gene information
- **Save as**: `data/raw/ALS_genes.csv`

### `full_database.xml`
- **Source**: [DrugBank](https://go.drugbank.com/releases/latest)  
  *(requires free academic registration)*
- **Dataset**: Full drug-target XML
- **Purpose**: Used to extract drug-to-target mappings
- **Save as**: `data/raw/full_database.xml`

---

Once downloaded, run:

```bash
python src/data_prep.py
