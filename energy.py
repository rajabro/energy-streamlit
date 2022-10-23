from operator import index
from optparse import Values
from pickletools import float8
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
st.subheader("Streamlit App by " + "[**Ruba'i Amin Jaya**](https://www.linkedin.com/in/aminjaya/)")
st.write('Capstone Project, Tetris PROA')

st.markdown('---')
# ---- READ EXCEL ----
@st.cache

def get_data_irena():
    df_irena = pd.read_excel('irena_data.xlsx')
    return df_irena

df_irena = get_data_irena()
df_irena = df_irena.rename({'RE or Non-RE' : 'Jenis_Energi',
                            'Group Technology' : 'Group_Technology'
                            }, axis=1)

st.subheader('Summary Executive')
st.write('Hingga tahun 2021 kontribusi energi terbarukan dalam bauran energi di Indonesia hanya mencapai 11.7% dari target 23% pada tahun 2025 dan direncanakan tahun 2030 pemerintah akan stop PLTU Batu Bara dan tahun 2060 seluruh pembangkit listrik di Indonesia dari energi terbarukan (NET Zero Emission).')
st.write('potensi energi terbarukan Indonesia mencapai 434 Giga Watt (GW), tetapi Kapasitas Energi Terbarukan tahun 2021 baru mencapai 11 GW (Data Irena 2021) atau 2.5% dari potensi yang dimiliki Indonesia. Energi surya di Indonesia memiliki potensi yang paling besar yakni 207 GW namun sampai dengan saat ini pemanfaatannya baru 10 Mega Watt (MW).')
st.write('Pembangungan pembangkit listrik energi terbarukan tersebar di wilayah Sumatera, Kalimantan, Sulawesi, Maluku, Papua dan Nusa Tenggara, serta Jawa Madura Bali. Namun, saat ini pembangunan masih di dominasi di wilayah Sumatera dan Jawa.')
st.write('Melihat belum meratanya pembangungan energi terbarukan di Indonesia, ini merupakan tantangan untuk pemerintah bagaimana mengoptimalkan pemanfaatan energi terbarukan di Indonesia untuk menuju net zero emission dan peluang bagi para investor atau pengusaha dalam industri energi terbarukan')

st.markdown('---')
st.subheader('Gambaran Energi Terbarukan Dunia, Bagaimana Posisi Indonesia?')
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
        default=list_teknologi[2]
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
    st.caption("Sumber: International Renewable Energy Agency (IRENA)" )
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
    st.caption("Sumber: International Renewable Energy Agency (IRENA)" )
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
    st.caption("Sumber: International Renewable Energy Agency (IRENA)" )
st.markdown('---')

st.header("Berapa Besar Potensi Energi Terbarukan di Indonesia")
st.write("Indonesia kaya dengan potensi energi terbarukan(antara lain energi surya, air, bayu, biomassa, laut, dan panas bumi) yang belum dimanfaatkan secara optimal. Menurut data ESDM, dengan teknologi saat ini, potensi listrik dari energi terbarukan mencapai 434 GW atau 7-8 kali dari total kapasitas pembangkit terpasang saat ini.")
st.write("Berikut gambaran Potensi, Rencana, dan Kapasitas Terpasang energi Terbarukan di Indonesia")

@st.cache

def get_data_indonesia():
    df_indo = pd.read_excel('renewable_energy_indonesia.xlsx')
    return df_indo

df_indo = get_data_indonesia().astype({'MW' : int, 'LUAS WILAYAH': int})

col1_3, col2_3 = st.columns(2)
with col1_3:  
    df_indo_teknologi = df_indo[['NAMA ENERGI', 'VAR', 'MW']].groupby(['NAMA ENERGI','VAR']).sum().sort_values(by='NAMA ENERGI', ascending=False).reset_index()

    df_indo_teknologi = pd.pivot_table(
        df_indo,
        values='MW',
        index='NAMA ENERGI',
        columns= 'VAR',
        aggfunc=np.sum,
        fill_value=0
    )

    df_indo_teknologi = df_indo_teknologi[['POTENSI (MW)','KAPASITAS TERPASANG (MW)', 'RENCANA 2019-2028 (MW)']].sort_values(by='POTENSI (MW)', ascending=False)
    df_indo_teknologi['PEMANFAATAN (%)'] = df_indo_teknologi['KAPASITAS TERPASANG (MW)'] / df_indo_teknologi['POTENSI (MW)'] *100
    df_indo_teknologi['PEMANFAATAN (%)'] = np.round(df_indo_teknologi['PEMANFAATAN (%)'], decimals = 4)
    st.table(df_indo_teknologi)
    st.caption("Sumber: Institute for Essential Services Reform (IESR) 2019" )
    df_indo_teknologi = df_indo_teknologi.reset_index()

    
with col2_3:
    st.write('Pada tahun 2019 jumlah potensi energi terbarukan Indonesia mencapai 434 GW, tetapi Kapasitas Energi Terbarukan tahun 2021 baru mencapai 11 GW (Data Irena 2021) atau 2.5% dari potensi yang dimiliki Indonesia.')
    st.write('Energi surya di Indonesia memiliki potensi yang paling besar yakni 207 GW namun sampai dengan saat ini pemanfaatannya baru 10 MW. Hal ini menjadikan peluang bagi investor atau pengusaha untuk ikut serta dalam pembangunan energi terbarukan di sektor energi surya.')
    st.write('Dalam hal perencanaan pembangunan energi terbarukan, Pemerintah merencakanan sampai dengan Tahun 2028 akan membangung energi terbarukan sebesar 28 GW atau . Perencanaan terbesar di energi tenaga air sebesar 14 GW atau 3 kali lipat dibanting pemanfaatan saat ini.')

st.write('Dari sisi teknologi energi terbarukan, kapasitas terpasang dan perencanaan masih lebih berfokus pada energi air dan panas bumi, padahal ada beberapa energi yang seharusnya lebih bisa dimanfaatkan yaitu energi surya dan bayu (angin) yang memiliki potensi lebih dari 50 GW')

st.write('Berdasarkan potensi dan rencana pemerintah dalam pembangunan energi terbarukan diatas, ini merupakan peluang investasi dan usaha yang sangat potensial, karena dengan rencana pemerintah yang sangat besar, anak ada dukungan kebijakan-kebijakan yang menguntungkan untuk industri energi terbarukan')


# df_indo_provinsi = df_indo[['PROVINSI','VAR','MW']].groupby(['PROVINSI','VAR']).sum().sort_values(by='MW', ascending=False).reset_index()

col1_4, col2_4 = st.columns(2)
with col1_4:
    df_indo_provinsi = pd.pivot_table(
        df_indo,
        values='MW',
        index='PROVINSI',
        columns= 'VAR',
        aggfunc=np.sum,
        fill_value=0
    )
    df_indo_provinsi = df_indo_provinsi[['POTENSI (MW)','KAPASITAS TERPASANG (MW)', 'RENCANA 2019-2028 (MW)']].sort_values(by='POTENSI (MW)', ascending=False)
    st.write("**Data Energi Terbarukan Per Provinsi di Indonesia**")
    df_indo_provinsi_top10 = df_indo_provinsi.head(10)
    st.table(df_indo_provinsi_top10)
    st.caption("Sumber: Institute for Essential Services Reform (IESR) 2019" )
with col2_4:
    df_indo_pulau = pd.pivot_table(
        df_indo,
        values='MW',
        index='PULAU',
        columns= 'VAR',
        aggfunc=np.sum,
        fill_value=0
    )
    df_indo_pulau = df_indo_pulau[['POTENSI (MW)','KAPASITAS TERPASANG (MW)', 'RENCANA 2019-2028 (MW)']].sort_values(by='POTENSI (MW)', ascending=False)
    df_indo_pulau_top10 = df_indo_pulau.head(10)
    st.write("**Data Energi Terbarukan Per Pulau di Indonesia**")
    st.table(df_indo_pulau_top10)
    st.caption("Sumber: Institute for Essential Services Reform (IESR) 2019" )
st.write("Beberapa provinsi di luar Jawa dan Sumatera memiliki potensi energi terbarukan yang besar. Provinsi Kalimantan Barat, Kalimantan Timur, Kalimantan Tengah, Nusa Tenggara Barat, dan Papua memiliki potensi energi terbarukan masing-masing diatas 20 GW. Karena itu, perencanaan penyediaan listrik di daerah tersebut seharusnya dapat memprioritaskan pemanfaatan energi terbarukan setempat. Di sisi lain, kapasitas terpasang energi terbarukan di daerah-daerah tersebut masih sangat rendah (kecuali di Kalimantan Barat), yakni di bawah 100 MW.")
st.write("Jika di breakdown berdasarkan Pulau, potensi energi terbarukan di luar pulau Jawa dan Sumatera sangat besar, terutama Kalimantan yang memiliki potensi 90 GW, namun perencanaan pembangunan energi terbarukan masih berfokus di wilayah Pulau Jawa dan Sumatera.")

st.markdown('---')

st.subheader("Kesimpulan dan Rekomendasi")
st.write('Untuk pemerataan energi di Indonesia dengan pemanfaatan energi terbarukan, IESR memberikan rekomendasi sebagai berikut: ')
st.write('1. Pemerintah perlu menerapkan kebijakan energi nasional secara konsisten melalui penyusunan Rencana Pengembangan Energi Terbarukan. Sumber: IESR')
st.write('2. Pemerintah pusat perlu melibatkan pemerintah daerah dalam perencanaan,pembangunan, dan evaluasi dalam program pengembangan energi terbarukan sehingga proyek-proyek energi terbarukan mampu dikelola oleh pemerintah daerah secara berkelanjutan. Sumber: IESR')
st.write('3. Dalam pembuatan perencanaan perlu diperhatikan besaran potensi energi terbarukan')
st.write('4. Pemerintah perlu segera menerapkan Standar Energi Terbarukan yang mewajibkan pembangit listrik tenaga fosil untuk membangun pembangkit energi terbarukan dengan persentase yang disesuaikan dengan target energi terbarukan dalam bauran energi. Sumber: The 9th Indonesia EBTKE Virtual Conference and Exhibition 2020')
st.write('Pemerintah perlu memberikan berbagai insentif atau kebijakan kepada pada investor dan pengusaha supaya tertarik untuk berinvestasi di dalam industri energi terbarukan Indonesia')

