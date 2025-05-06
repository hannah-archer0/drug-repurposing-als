import os
import pandas as pd
import xml.etree.ElementTree as ET
import pubchempy as pcp

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

ALS_GENES_PATH = os.path.join(RAW_DIR, "ALS_genes.csv")
DRUGBANK_XML_PATH = os.path.join(RAW_DIR, "full_database.xml")
OUTPUT_PATH = os.path.join(PROCESSED_DIR, "ALS_Drugs_With_SMILES.csv")


def get_smiles(drug_name):
    try:
        compounds = pcp.get_compounds(drug_name, 'name')
        if compounds:
            return compounds[0].isomeric_smiles
    except Exception as e:
        print(f"[SMILES ERROR] {drug_name}: {e}")
    return None


def extract_drug_targets():
    print("🔍 Parsing DrugBank XML...")
    tree = ET.parse(DRUGBANK_XML_PATH)
    root = tree.getroot()
    ns = {"db": root.tag.split("}")[0].strip("{")}

    drug_data = []
    for drug in root.findall("db:drug", ns):
        drug_name_elem = drug.find("db:name", ns)
        drug_id_elem = drug.find("db:drugbank-id", ns)

        drug_name = drug_name_elem.text if drug_name_elem is not None else "Unknown"
        drug_id = drug_id_elem.text if drug_id_elem is not None else "Unknown"

        for target in drug.findall("db:targets/db:target", ns):
            polypeptide = target.find("db:polypeptide", ns)
            if polypeptide is not None:
                gene_elem = polypeptide.find("db:gene-name", ns)
                gene_id = gene_elem.text if gene_elem is not None else None
                uniprot_id = polypeptide.get("id")
                drug_data.append([drug_name, drug_id, gene_id, uniprot_id])
    return pd.DataFrame(drug_data, columns=["Drug Name", "DrugBank ID", "Gene ID", "UniProt ID"])


def main():
    print("📥 Loading ALS gene data...")
    als_genes = pd.read_csv(ALS_GENES_PATH)
    als_uniprots = als_genes[['unitProt']].dropna().copy()

    # Normalize UniProt IDs (some rows have comma-separated entries)
    als_uniprots['unitProt'] = als_uniprots['unitProt'].str.split(',')
    als_uniprots = als_uniprots.explode('unitProt')
    als_uniprots['unitProt'] = als_uniprots['unitProt'].str.strip()
    als_uniprot_set = set(als_uniprots['unitProt'])

    drugbank_df = extract_drug_targets()
    print(f"🧬 Extracted {len(drugbank_df)} drug-target interactions.")

    # Filter DrugBank by ALS UniProt matches
    matched = drugbank_df[drugbank_df['UniProt ID'].isin(als_uniprot_set)].drop_duplicates(subset=["DrugBank ID"])
    print(f"🔗 Found {len(matched)} drugs with ALS-matching targets.")

    print("🧪 Fetching SMILES strings...")
    matched['SMILES'] = matched['Drug Name'].apply(get_smiles)
    matched = matched.dropna(subset=['SMILES'])

    print(f"✅ Retrieved SMILES for {len(matched)} ALS-related drugs.")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    matched.to_csv(OUTPUT_PATH, index=False)
    print(f"💾 Saved processed data to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
