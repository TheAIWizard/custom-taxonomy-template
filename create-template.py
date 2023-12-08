import pandas as pd
import xlrd

# Chemin vers le fichier Excel (.xls)
excel_file_path = "custom-taxonomy-template/table_NAF2-NA.xls"

# Ouvrir le fichier Excel avec xlrd
#workbook = xlrd.open_workbook(excel_file_path).sheet_names()[0]

intitule_ape = pd.read_excel("https://www.insee.fr/fr/statistiques/fichier/2028155/table_NAF2-NA.xls", sheet_name='Version avec niveau A 21')
intitule_section_division = pd.read_excel("https://www.insee.fr/fr/statistiques/fichier/2028155/niv_agreg_naf_rev_2.xls ", sheet_name='A 88')

# Select columns
intitule_ape = intitule_ape[['SOUS CLASSE', 'INTITULE DE LA NAF rév. 2', 'CLASSE', 'DIVISION','SECTION']]
# Drop the first row (index 0)
intitule_ape = intitule_ape.drop(0)

# Forward fill NaN values in the 'Section' and 'Libellé des sections' columns
intitule_section_division['Section '] = intitule_section_division['Section '].ffill()
intitule_section_division['Libellé des sections'] = intitule_section_division['Libellé des sections'].ffill()
intitule_section_division['Code\nDivision'] = intitule_section_division['Code\nDivision'].astype(str).str.zfill(2)

# Rename the column
intitule_section_division.rename(columns={'Code\nDivision': 'Division', 'Intitulé ': 'Intitulé des divisions'}, inplace=True)
intitule_ape.rename(columns={'SOUS CLASSE': 'Sous-classe','INTITULE DE LA NAF rév. 2': 'Intitulé de la sous-classe','CLASSE': 'Classe','DIVISION': 'Division','SECTION': 'Section',}, inplace=True)

print(intitule_ape.columns)
print(intitule_ape)
print(intitule_section_division)

# Jointure à gauche sur la colonne 'ID'
data_naf = pd.merge(intitule_ape, intitule_section_division, on='Division', how='left')

print(data_naf[["Sous-classe","Section","Division"]])

# Forward fill NaN values in the 'Section' column
#df['Section'] = df['Section'].ffill()
