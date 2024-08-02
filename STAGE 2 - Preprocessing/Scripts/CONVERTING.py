# IMPORT LIBRARIES
import pandas as pd

# INPUT FILE
input_file = '../Datasets/Outliers/All_Data_Non_Outliers.xlsx'
df = pd.read_excel(input_file)

# OUTPUT FILE
output_file = '../Datasets/Outliers/All_Data_Non_Outliers.csv'
df.to_csv(output_file, index=False)
print(f'CONVERTED FILE SAVED TO {output_file}')