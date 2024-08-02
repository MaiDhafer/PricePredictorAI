# IMPORTING LIBRARIES
import pandas as pd

# LISTS OF ALL INPUT FILES
files = [
    '../Datasets/(8) August/Cleaned_AirBnB_Riyadh_(8)August_Bedroom(1).xlsx',
    '../Datasets/(8) August/Cleaned_AirBnB_Riyadh_(8)August_Bedroom(2).xlsx',
    '../Datasets/(8) August/Cleaned_AirBnB_Riyadh_(8)August_Bedroom(3).xlsx',

    '../Datasets/(9) September/Cleaned_AirBnB_Riyadh_(9)September_Bedroom(1).xlsx',
    '../Datasets/(9) September/Cleaned_AirBnB_Riyadh_(9)September_Bedroom(2).xlsx',
    '../Datasets/(9) September/Cleaned_AirBnB_Riyadh_(9)September_Bedroom(3).xlsx',

    '../Datasets/(10) October/Cleaned_AirBnB_Riyadh_(10)October_Bedroom(1).xlsx',
    '../Datasets/(10) October/Cleaned_AirBnB_Riyadh_(10)October_Bedroom(2).xlsx',
    '../Datasets/(10) October/Cleaned_AirBnB_Riyadh_(10)October_Bedroom(3).xlsx',

    '../Datasets/(11) November/Cleaned_AirBnB_Riyadh_(11)November_Bedroom(1).xlsx',
    '../Datasets/(11) November/Cleaned_AirBnB_Riyadh_(11)November_Bedroom(2).xlsx',
    '../Datasets/(11) November/Cleaned_AirBnB_Riyadh_(11)November_Bedroom(3).xlsx',

    '../Datasets/(12) December/Cleaned_AirBnB_Riyadh_(12)December_Bedroom(1).xlsx',
    '../Datasets/(12) December/Cleaned_AirBnB_Riyadh_(12)December_Bedroom(2).xlsx',
    '../Datasets/(12) December/Cleaned_AirBnB_Riyadh_(12)December_Bedroom(3).xlsx',

    '../../STAGE 1 - Data Collection/Datasets/External Datasets/External_Data.xlsx',
]

# LIST TO STORE ALL FILES
all_data = []

# LOOP IN FILES LIST
for file in files:
    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        all_data.append(df)

# STORE IN DATAFRAME
merged_data = pd.concat(all_data, ignore_index=True)

# CONVERT 'START_DATE' AND 'END_DATE' COLUMNS TO DATETIME FORMAT
merged_data['Start_Date'] = pd.to_datetime(merged_data['Start_Date'])
merged_data['End_Date'] = pd.to_datetime(merged_data['End_Date'])

# DISPLAY ONLY DATE
merged_data['Start_Date'] = merged_data['Start_Date'].dt.strftime('%Y-%m-%d')
merged_data['End_Date'] = merged_data['End_Date'].dt.strftime('%Y-%m-%d')

# OUTPUT FILE
output_file = '../Datasets/All Data Merged/All_Data_Merged.xlsx'
merged_data.to_excel(output_file, index=False)
print(f'MERGED DATA SAVED TO {output_file}')