# IMPORT LIBRARIES
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# INPUT FILE
input_file = '../Datasets/Outliers/All_Data_Non_Outliers.csv'
df = pd.read_csv(input_file)

# DROP NAME COLUMN
df = df.drop('Name', axis=1)

# ONE-HOT ENCODING DISTRICT USING SKLEARN
encoder = OneHotEncoder(sparse_output=False, drop='first')
encoded_districts = encoder.fit_transform(df[['District']])
encoded_districts_df = pd.DataFrame(encoded_districts, columns=encoder.get_feature_names_out(['District']))


# CONCATENATE ENCODED DATA WITH ORIGINAL DATAFRAME
df = pd.concat([df.drop('District', axis=1), encoded_districts_df], axis=1)

# CONVERT BOOLEAN TO INTEGER
boolean_columns = df.select_dtypes(include=['bool']).columns
df[boolean_columns] = df[boolean_columns].astype(int)

# OUTPUT FILE
output_file = '../Datasets/Encoding/All_Data_Encoded.csv'
df.to_csv(output_file, index=False)
print(f'ENCODED FILE SAVED TO {output_file}')