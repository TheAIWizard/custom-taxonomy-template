import pandas as pd
from lxml import etree

# Sample DataFrame with additional columns
data = {'Sous-classe': ['01.11Z', '01.12Z', '01.13Z', '01.14Z', '01.15Z', '96.09Z', '97.00Z', '98.10Z', '98.20Z', '99.00Z'],
        'Section': ['A', 'A', 'A', 'A', 'A', 'S', 'T', 'T', 'T', 'U'],
        'Division': ['01', '01', '01', '01', '01', '96', '97', '98', '98', '99'],
        'Libellé des sections': ['AGRICULTURE, SYLVICULTURE ET PÊCHE'] * 5 + ['AUTRES ACTIVITÉS DE SERVICES'] * 3 + ['ACTIVITÉS DES MÉNAGES EN TANT QU\'EMPLOYEURS ; ACTIVITÉS INDIFFÉRENCIÉES DES MÉNAGES EN TANT QUE PRODUCTEURS DE BIENS ET SERVICES POUR USAGE PROPRE'] * 2,
        'Intitulé des divisions': ['Culture et production animale, chasse et services annexes'] * 5 + ['Réparation d\'ordinateurs et de biens personnels et domestiques'] + ['Activités des ménages en tant qu\'employeurs de personnel domestique'] * 2 + ['Activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre'],
        'Intitulé de la sous-classe': ['Culture de céréales (à l\'exception du riz), de légumineuses et de graines oléagineuses', 'Culture du riz', 'Culture de légumes, de melons, de racines et de tubercules', 'Culture de la canne à sucre', 'Culture du tabac', 'Autres services personnels n.c.a.', 'Activités des ménages en tant qu\'employeurs de personnel domestique', 'Activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre', 'Activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre', 'Activités des organisations et organismes extraterritoriaux']}
df = pd.DataFrame(data)

# Create XML structure
root = etree.Element("View")
text_element = etree.SubElement(root, "Text", name="text", value="$text")
taxonomy_element = etree.SubElement(root, "Taxonomy", name="taxonomy", toName="text")

# Iterate over each branch and write to XML
for section, section_df in df.groupby('Section'):
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
