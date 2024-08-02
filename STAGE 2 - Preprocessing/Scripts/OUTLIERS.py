# IMPORT LIBRARIES
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# INPUT FILE
input_file = '../Datasets/All Data Merged/All_Data_Merged.xlsx'
df = pd.read_excel(input_file, sheet_name='Sheet1')

# CALCULATE Z-SCORES
df['Z-Score'] = stats.zscore(df['Price'])

# Z-SCORE METHOD
threshold = 3
outliers = df[abs(df['Z-Score']) > threshold]
non_outliers = df[abs(df['Z-Score']) <= threshold]

# SCATTER PLOT
plt.figure(figsize=(12, 8))
plt.scatter(df['Price'], [0] * len(df), color='cyan', alpha=0.5, label='Non-Outliers')
plt.scatter(outliers['Price'], [0] * len(outliers), color='red', label='Outliers', alpha=0.6)
plt.xscale('log')
plt.title('Scatter Plot of Price with Outliers Highlighted (Z-Score Method)')
plt.xlabel('Price')
plt.yticks([])
plt.legend()
plt.savefig('../Datasets/Outliers/Figure/Price_Scatter_Outliers.png')
plt.close()

# VIOLIN PLOT
plt.figure(figsize=(12, 8))
sns.violinplot(x='Price', data=df, color='cyan', inner=None)
plt.scatter(outliers['Price'], [0] * len(outliers), color='red', label='Outliers', alpha=0.6)
plt.xscale('log')
plt.title('Violin Plot of Price with Outliers Highlighted (Z-Score Method)')
plt.xlabel('Price')
plt.yticks([])
plt.legend()
plt.savefig('../Datasets/Outliers/Figure/Price_Violin_Outliers.png')
plt.close()

# OUTPUT FILES
output_file = '../Datasets/Outliers/All_Data_Non_Outliers.xlsx'
non_outliers.to_excel(output_file, index=False)
print(f'NON-OUTLIERS DATA SAVED TO {output_file}')
