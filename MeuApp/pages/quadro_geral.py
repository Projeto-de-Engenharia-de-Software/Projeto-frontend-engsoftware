import folium
import numpy as np
import pandas as pd
import streamlit as st
from datetime import date, datetime
from datetime import timedelta
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import altair as alt
from pages.configuracoes import config
from pages.equipes import equipes, get_equipes
from pages.util import API_BASE_URL, make_authenticated_request
import extra_streamlit_components as stx
from pages._login import cookie

st.set_page_config(
    page_title="Nexus - Quadro Geral",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Recupera token salvo no cookie
token_cookie = cookie.get("auth_token")
if token_cookie and 'auth_token' not in st.session_state:
    st.session_state.auth_token = token_cookie

# Se não houver token válido, redireciona para login
if 'auth_token' not in st.session_state:
    st.switch_page("pages/_login.py")

@st.cache_data
def get_quadro():
    token_cookie = cookie.get("auth_token")
    if token_cookie and 'auth_token' not in st.session_state:
        st.session_state.auth_token = token_cookie

    if 'auth_token' not in st.session_state:
        st.switch_page("pages/_login.py")

    url = f"{API_BASE_URL}registro-violencia/"
    response = make_authenticated_request('get', url)

    if response and response.status_code == 200:
        df_equipe = pd.DataFrame(response.json())
        df_equipe.drop(columns=['id'], inplace=True)

        return df_equipe
    else:
        st.error("Erro ao carregar equipes")
        return pd.DataFrame()

@st.cache_data
def carregar_dados_pernambuco():
    """
    Carrega a lista de municípios de Pernambuco com suas coordenadas.
    A função agora retorna um DataFrame limpo, pronto para receber os dados de casos.
    """
    try:
        url = "pages/municipios.csv"
        df_brasil = pd.read_csv(url)
        df_pe = df_brasil[df_brasil['codigo_uf'] == 26].copy()
        
        # Seleciona e renomeia as colunas. A coluna 'nome' se tornará 'cidade'.
        df_final = df_pe[['nome', 'latitude', 'longitude']].rename(columns={
            'nome': 'cidade'
        })
        df_final["Casos"] = None
        return df_final

    except Exception as e:
        st.error(f"Não foi possível carregar a lista de municípios. Erro: {e}")
        return pd.DataFrame()

st.markdown("""
    <style>
        /* Oculta a navegação padrão de páginas do Streamlit */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

st.image("pages/image.png", use_container_width=True) 



if 'page' not in st.session_state:

    st.session_state.page = '📊 Quadro Geral'

with st.sidebar:

    st.markdown("### 🧭 Navegação")
    escolha = st.radio("Escolha a página:", ["📊 Quadro Geral", "🗺️ Mapa Interativo", "🤝 Equipes", "⚙️ Configurações"], label_visibility="collapsed")
    st.session_state.page = escolha


if st.session_state.page == "📊 Quadro Geral":

    st.markdown("<h1 style='text-align: center;'>Quadro Geral de Casos</h1>", unsafe_allow_html=True)

    dados = get_quadro()
    dados["DT_NOTIFIC"] = pd.to_datetime(dados["DT_NOTIFIC"])

    ano = st.sidebar.selectbox(
        "Selecione o ano de análise", 
        [2024, 2023, 2022, 2021, 2020]
    )

    dados_ano = dados[dados["DT_NOTIFIC"].dt.year == ano]


    data1 = dados_ano["DT_NOTIFIC"].min().date()
    data2 = dados_ano["DT_NOTIFIC"].max().date()


    slider = st.sidebar.slider(
        "Selecione o intervalo",
        min_value=data1,
        max_value=data2,
        value=(data1, data2),
        format="YYYY-MM-DD",
        step=timedelta(days=1)
    )


    dados_filtrados = dados_ano[
        (dados_ano["DT_NOTIFIC"].dt.date >= slider[0]) & 
        (dados_ano["DT_NOTIFIC"].dt.date <= slider[1])
    ]

    raca = st.sidebar.selectbox(
        "Selecione a cor ou raça",
        ["Nenhum", "Branca", "Preta", "Parda", "Amarela", "Indígena", "Ignorado"])
    
    dados_raca = dados_filtrados[dados_filtrados["CS_RACA"] == raca ]


    if raca == "Nenhum":

        st.dataframe(dados_filtrados) 
    
    else:
        st.dataframe(dados_raca)
    


elif st.session_state.page == "🗺️ Mapa Interativo":

    st.markdown("<h1 style='text-align: center;'>Mapa Interativo</h1>", unsafe_allow_html=True)
    st.title("🌡️ Mapa de Calor - Notificações na RMR")

    casos = get_quadro()

    dados_geo = carregar_dados_pernambuco()

    contagem_de_casos = casos["MUNICIPIO"].value_counts()
    dados_geo["Casos"] = dados_geo["cidade"].map(contagem_de_casos).fillna(0).astype(int)
        

    heat_data = []

    for _, row in dados_geo.iterrows():

        heat_data.extend([[row['latitude'], row['longitude']]] * row['Casos'])

 
    m = folium.Map(location=[-8.05, -34.9], zoom_start=10)


    HeatMap(heat_data, radius=20, blur=15, min_opacity=0.3).add_to(m)


    for _, row in dados_geo.iterrows():

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['cidade']}<br>Casos: {row['Casos']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)


    folium_static(m)

elif st.session_state.page == "🤝 Equipes":
    eqp = get_equipes()
    equipes(eqp)
    #st.switch_page("pages/equipes.py")

elif st.session_state.page == "⚙️ Configurações":

    config()




        


  

