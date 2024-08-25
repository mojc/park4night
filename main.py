import pandas as pd
import streamlit as st

xls = pd.ExcelFile(r"park_4_night.xls") # use r before absolute file path
sheetX = xls.parse(0) #2 is the sheet number+1 thus if the file has only 1 sheet write 0 in paranthesis

# define and extract relevant columns
data = {'DATUM': [], 'DRŽAVA': [], 'ODRASLI': [], 'OTROCI': [], 'KOLESARJI': []}
col_names = [col_name for col_name in sheetX.columns if col_name.startswith(tuple(data.keys()))]
col_names.pop(0) # removes DATUM

# custom melt i guess
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

## data visualization

# date selector - show min and max date and enable selecting time range
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start:', value=new_df.DATUM.min(), min_value=new_df.DATUM.min(), max_value=new_df.DATUM.max())
with col2:    
    end_date = st.date_input('End:', value=new_df.DATUM.max(), min_value=new_df.DATUM.min(), max_value=new_df.DATUM.max())

