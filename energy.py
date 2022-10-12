import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Energi Terbarukan", 
    page_icon=":chart_with_upwards_trend:", 
    layout="wide"
    )

st.title('Optimalisasi Energi Terbarukan Indonesia')
# ---- READ EXCEL ----

# @st.cache

def get_data_from_excel():
    df = pd.read_excel('renewable_energy_world.xlsx')
    return df

df = get_data_from_excel()
df = df[(df.REGION=='ASIA') & 
        (df.ENERGY=='Total renewable energy') &
        (df.COUNTRY!='China')]
df = df.drop(['AREA','REGION','ENERGY'], axis=1).sort_values(by=['2021'], ascending=False).head(10)
st.dataframe(df)

df_unpivot = pd.melt(df, id_vars=['COUNTRY'], 
                 var_name='TAHUN',
                 value_name='KAPASITAS ENERGY')


df = pd.DataFrame(df_unpivot)

line_chart = alt.Chart(df).mark_line(interpolate='basis').encode(
    alt.X('TAHUN:N', title='Tahun'),
    alt.Y('KAPASITAS ENERGY:Q', title='Kapasitas Energi Terpasang'),
    color=alt.Color('COUNTRY:N')
).properties(
    title='Perbandingan Energi Terbarukan Indonesia dengan Negara di Asia Selain China'
)

st.altair_chart(line_chart)

st.caption("Data Source: IRENA (2022), Renewable energy statistics 2022, International Renewable Energy Agency (IRENA), Abu Dhabi")



