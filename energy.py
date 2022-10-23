import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import plotly.express as px

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Energi Terbarukan", 
    page_icon=":chart_with_upwards_trend:", 
    layout="wide"
    )

# --------MAIN PAGE--------
st.title('Optimalisasi Pemanfaatan Energi Terbarukan Indonesia')
# ---- READ EXCEL ----

@st.cache

def get_data_irena():
    df_irena = pd.read_excel('irena_data.xlsx')
    return df_irena

df_irena = get_data_irena()
df_irena = df_irena.rename({'RE or Non-RE' : 'Jenis_Energi',
                            'Group Technology' : 'Group_Technology'
                            }, axis=1)

col1, col2, col3 = st.columns([1,3,1])

with col1:
    jenis_energi = st.selectbox(
    'Jenis Energi',
    df_irena['Jenis_Energi'].sort_values(ascending=False).unique()
    )

    show_by = st.selectbox(
        'Jenis Data',
        ('Electricity Installed Capacity (MW)','Electricity Generation (GWh)')
    )
    df_irena_ranking = df_irena.query(
        "Jenis_Energi == @jenis_energi"
    )
    list_teknologi = df_irena['Group_Technology'].sort_values().unique()

    jenis_teknologi = st.multiselect(
        """Teknologi
        (Hapus semua teknologi untuk menampilkan semua data)""",
        options=list_teknologi,
        default=list_teknologi[0]
    )

    if jenis_teknologi == []:
        st.warning("Teknologi belum dipilih, data ditampilkan semua")
    else:
        df_irena_ranking = df_irena.query(
        "Group_Technology == @jenis_teknologi"
        )

    tahun = st.selectbox(
        'Tahun',
        df_irena_ranking['Year'].sort_values(ascending=False).unique(),
    )

    df_irena_ranking = df_irena_ranking.query(
        "Year == @tahun"
    )

    #st.dataframe(df_irena_selection)

with col2:
    df_irena_ranking = df_irena_ranking[["Country", show_by]].groupby("Country").sum().sort_values(by=show_by, ascending=False)
    df_irena_ranking = df_irena_ranking.astype({show_by: 'int'}).head(10).sort_values(by=show_by).reset_index()

    fig_ranking_dunia = px.bar(
        df_irena_ranking,
        x = show_by,
        y = 'Country',
        orientation = 'h',
        title = '<b>Peringkat Energi Terbarukan Dunia</b>',
        color_discrete_sequence=["#0083B8"] * len(df_irena_ranking),
        template='plotly_white',
        # text=show_by
    )
    fig_ranking_dunia.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=True))
    )

    fig_ranking_dunia.update_xaxes(visible=True, showticklabels=True)

    st.plotly_chart(fig_ranking_dunia)

with col3:
    st.write('Tahun 2021, Berdasarkan Data IRENA, Energi Terbarukan Dunia masih di dominasi oleh China dengan 1.020.234 MW atau 33.25% dari total energi terbarukan dunia dan Amerika Serikat di peringkat 2 dengan 325.391 MW atau 10.60% dari total energi terbarukan dunia. Indonesia sendiri menduduki peringkat **36** dengan Kapasitas EBT Terpasang sbesar **11.127 MW** atau **0.36%** dari total energi terbarukan dunia.')
    st.write('Indonesia memiliki **Energi Panas Bumi terbesar kedua di dunia** dengan **2.277 MW** atau **14.27%** dari total energi panas bumi dunia.')

st.markdown('---')

col1_2, col2_2 = st.columns([2,1])
with col1_2:
    # membuat list negara untuk filter
    list_negara = df_irena['Country'].sort_values().unique()
    df_list_negara = pd.DataFrame(list_negara, columns=['negara'])
    indonesia_terpilih = (df_list_negara['negara'] == 'Indonesia').idxmax() #mencari index negara indonesia untuk default

    negara = st.selectbox(
        "Pilih Negara",
        list_negara,
        index=indonesia_terpilih
    )
  
    df_irena_series = df_irena.query(
        "Jenis_Energi == @jenis_energi & Country == @negara"
    )
    df_irena_series = df_irena_series[['Year', 'Group_Technology', show_by]].groupby(['Year','Group_Technology']).sum().sort_values(by=show_by, ascending=False)
    df_irena_series = df_irena_series.astype({show_by: 'int'}).sort_values(by='Year').reset_index()

    fig_re_growth = px.bar(
        df_irena_series,
        x = 'Year',
        y = show_by,
        color = 'Group_Technology',
        title = 'Pertumbuhan Energi Terbarukan ' + negara
    )

    fig_re_growth.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=True))
        )
    st.plotly_chart(fig_re_growth)
    
with col2_2:
    st.write('Energi Terbarukan Indonesia dari dari Tahun ke Tahun selalu mengalami pertumbuhan.')
    st.write('Pada tahun 2021, Pertumbuhan Energi Terbarukan Indonesia sebesar 650 MW atau tumbuh 6,19%. Pertumbuhan ini lebih tinggi dari pada pertumbuhan tahun 2020 yaitu hanya mencapai 207 MW atau 2,01% dibanding tahun sebelumnya.')

    df_irena_growth = pd.pivot_table(
        df_irena_series,
        values=show_by,
        index='Year',
        columns='Group_Technology',
        aggfunc=np.sum,
        fill_value=0
    )

    df_irena_growth = df_irena_growth.diff().dropna().astype('int').reset_index()

    df_irena_growth1 = df_irena_growth[(df_irena_growth['Year'].isin([2019,2020,2021]))].reset_index()
    df_irena_growth1 = df_irena_growth1.iloc[:,1:]
    df_irena_growth1 = df_irena_growth1.set_index('Year')
    df_irena_growth1 = df_irena_growth1.transpose()
    st.caption('Penambahan Energi Terbarukan yang terpasang dari Tahun 2019-2021')
    st.write(df_irena_growth1)

st.markdown('---')

