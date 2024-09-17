import pandas as pd
import streamlit as st
import plotly.express as px

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
new_df = df_pivoted.drop(columns=['Group']).sort_values('DATUM').reset_index(drop=True)

## data visualization

# date selector - show min and max date and enable selecting time range
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start:', value=new_df.DATUM.min(), min_value=new_df.DATUM.min(), max_value=new_df.DATUM.max())
with col2:    
    end_date = st.date_input('End:', value=new_df.DATUM.max(), min_value=new_df.DATUM.min(), max_value=new_df.DATUM.max())

# plotting data
df = new_df.query(f'DATUM >= "{start_date}" and DATUM <= "{end_date}"')
df['UNITS'] = 1
color_map = {'D': 'yellow', 'F': 'royalblue', 'IE': 'saddlebrown', 'CH': 'darkred', 'NL': 'darkorange', 'B': 'limegreen', 'GB': 'teal'}

st.write(f'Stevilo vozil: {len(df)}')
col1, col2 = st.columns(2)
with col1:
    st.write(f'Stevilo odraslih: {df.ODRASLI.sum()}')
    fig = px.pie(df, values='ODRASLI', names='DRŽAVA', color='DRŽAVA', title='Odrasli na drŽavo.', color_discrete_map=color_map)
    st.plotly_chart(fig)
with col2:
    st.write(f'Stevilo otrok: {df.OTROCI.sum()}')
    fig = px.pie(df, values='OTROCI', names='DRŽAVA', color='DRŽAVA', title='Otroci na drŽavo.', color_discrete_map=color_map)
    st.plotly_chart(fig)

fig = px.bar(df, x='DATUM', y='UNITS', color='DRŽAVA', color_discrete_map=color_map, title='Stevilo vozil skozi cas')
st.plotly_chart(fig)