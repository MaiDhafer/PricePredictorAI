# IMPORT LIBRARIES
import pandas as pd

# READ FILE
df = pd.read_csv('../Datasets/Encoding/All_Data_Encoded.csv')

# SUMMARY STATISTICS
print("\nSummary Statistics:")
print(df.describe())

# DATA TYPES OF EACH COLUMN
print("\nData Types:")
print(df.dtypes)

# MISSING VALUES
print("\nMissing Values Count:")
print(df.isnull().sum())