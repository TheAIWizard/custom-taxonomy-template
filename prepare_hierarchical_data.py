import pandas as pd
from lxml import etree

# Chemin vers le fichier Excel (.xls)
excel_file_path = "custom-taxonomy-template/table_NAF2-NA.xls"

# Ouvrir le fichier Excel avec xlrd
# import xlrd
# workbook = xlrd.open_workbook(excel_file_path).sheet_names()[0]

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
intitule_ape.rename(columns={'SOUS CLASSE': 'Sous-classe', 'INTITULE DE LA NAF rév. 2': 'Intitulé de la sous-classe', 'CLASSE': 'Classe', 'DIVISION': 'Division', 'SECTION': 'Section', }, inplace=True)

print(intitule_ape.columns)
print(intitule_ape)
print(intitule_section_division)

# Jointure à gauche sur la colonne 'ID'
data_naf = pd.merge(intitule_ape, intitule_section_division, on='Division', how='left')

print(data_naf[["Sous-classe", "Section", "Division"]])

# Forward fill NaN values in the 'Section' column
#df['Section'] = df['Section'].ffill()

data_naf.to_json("hierarchical_nace.json", orient ='index')

# Create XML structure
root = etree.Element("View")
text_element = etree.SubElement(root, "Text", name="text", value="$text")
taxonomy_element = etree.SubElement(root, "Taxonomy", name="taxonomy", toName="text")

# Iterate over each branch and write to XML
for section, section_df in data_naf.groupby('Section'):
    section_label = section_df['Libellé des sections'].iloc[0]  # Assuming the label is the same for all rows in the section
    
    section_choice = etree.SubElement(taxonomy_element, "Choice", value=f"{section} - {section_label}", alias=section)
    
    for division, division_df in section_df.groupby('Division'):
        division_label = division_df['Intitulé des divisions'].iloc[0]  # Assuming the label is the same for all rows in the division
        
        division_choice = etree.SubElement(section_choice, "Choice", value=f"{division} - {division_label}", alias=division)
        
        for sous_classe, sous_classe_label in zip(division_df['Sous-classe'], division_df['Intitulé de la sous-classe']):
            sous_classe_choice = etree.SubElement(division_choice, "Choice", value=f"{sous_classe} - {sous_classe_label}", alias=sous_classe)

# Create ElementTree and write to file
tree = etree.ElementTree(root)
tree.write("taxonomy.xml", pretty_print=True)