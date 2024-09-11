import pandas as pd

xls = pd.ExcelFile(r"park_4_night.xls") # use r before absolute file path

df = xls.parse(0) #2 is the sheet number+1 thus if the file has only 1 sheet write 0 in paranthesis

# Approach with pivot/unpivot
df_melted = pd.melt(df[df.columns[0:25]], id_vars=['DATUM'], var_name='Variable', value_name='Value')

# Extract the part before and after the dot (.)
df_melted[['Variable', 'Group']] = df_melted['Variable'].str.split('.', n=1, expand=True)
# Fill NaN values in the 'Group' column with '0' to denote the first occurrence
df_melted['Group'] = df_melted['Group'].fillna('0')

# Pivot the DataFrame to get the desired structure
df_pivoted = df_melted.pivot_table(index=['DATUM', 'Group'], 
                                   columns='Variable', 
                                   values='Value', 
                                   aggfunc='first').reset_index()

# Clean up the DataFrame
df_final = df_pivoted.drop(columns=['Group']).sort_values('DATUM').reset_index(drop=True)
