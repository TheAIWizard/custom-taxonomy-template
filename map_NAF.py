import pandas as pd
from lxml import etree

""" Download data """
# File path (.xls)
excel_file_path = "Table de correspondances NAF rev.2"

# Import as dataframe
correspondance_NAF = pd.read_excel(excel_file_path, sheet_name='1) correspondance NAFNAF')

# Select columns
correspondance_NAF = correspondance_NAF[['NAFold-code', 'NAFold-intitulé', 'NAFnew-code', 'NAFnew-intitulé']]
# Drop the first row (index 0)
correspondance_NAF = correspondance_NAF.drop(0)

# Rename the column
correspondance_NAF.rename(columns={'NAFold-code': 'NAF2008', 'NAFold-intitulé': 'NAF2008_intitule', 'NAFnew-cod': 'NAF2025', 'NAFnew-intitulé': 'NAF2025_intitule'}, inplace=True)

print(correspondance_NAF.columns)
print(correspondance_NAF)


correspondance_NAF.to_parquet('correspondance_NAF.parquet.gzip', compression='gzip')
