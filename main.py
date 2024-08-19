import pandas as pd

xls = pd.ExcelFile(r"park_4_night.xls") # use r before absolute file path

sheetX = xls.parse(0) #2 is the sheet number+1 thus if the file has only 1 sheet write 0 in paranthesis
df = sheetX.copy(deep=True)
# extract relevant columns
col_names = [col_name for i, col_name in zip(range(27), sheetX.columns)]
col_names.pop(0)
col_names.pop(-1)
col_names.pop(-1)

# custom melt i guess
data = {'DATUM': [], 'DRŽAVA': [], 'ODRASLI': [], 'OTROCI': [], 'KOLESARJI': []}

for i in range(len(sheetX['DATUM'])):
    k = 0
    for j in range(0, len(col_names), 4):
        if not str(sheetX[col_names[j]][i]) == 'nan':
            k += 1
            print(i, k)
    for j in range(k*4):
        data[col_names[j].split('.')[0]].append(sheetX[col_names[j]][i])
    for j in range(k):
        data['DATUM'].append(sheetX['DATUM'][i])
# to excel
new_df = pd.DataFrame(data)
new_df.to_excel('transformed.xlsx')

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

# compare to see if we get same results
df_final = df_final[new_df.columns]
print((df_final.fillna(0).sort_values(['DRŽAVA', 'ODRASLI', 'OTROCI']).reset_index() != new_df.fillna(0).sort_values(['DRŽAVA', 'ODRASLI', 'OTROCI']).reset_index()).sum())