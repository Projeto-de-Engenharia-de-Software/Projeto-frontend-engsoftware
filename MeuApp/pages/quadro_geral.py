import folium
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
from datetime import timedelta
from folium.plugins import HeatMap
from streamlit_folium import folium_static

@st.cache_data
def carregar_dados_ficticios():
    datas = pd.date_range(start="2021-01-01", end="2022-12-31", freq="M")
    estados = [
        "Sergipe", "Minas Gerais", "Alagoas", "Piauí", "Bahia",
        "Pará", "Goiás", "São Paulo", "Rio de Janeiro", "Pernambuco",
        "Mato Grosso", "Santa Catarina", "Paraná", "Ceará"
    ]
    dados = {
        "Data": [],
        "Estado": [],
        "Casos": []
    }

    for estado in estados:
        for data in datas:
            casos = np.random.randint(100, 1000)
            dados["Data"].append(data)
            dados["Estado"].append(estado)
            dados["Casos"].append(casos)

    df = pd.DataFrame(dados)
    return df


# Configuração da página
st.set_page_config(
    page_title="Nexus - Quadro Geral",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Remove toda a navegação automática da sidebar com CSS
st.markdown("""
    <style>
        /* Oculta a navegação padrão de páginas do Streamlit */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Inicializa o estado da página
if 'page' not in st.session_state:
    st.session_state.page = '📊 Quadro Geral'

# Sidebar personalizada
with st.sidebar:
    st.markdown("### 🧭 Navegação")
    escolha = st.radio("Escolha a página:", ["📊 Quadro Geral", "🗺️ Mapa Interativo"], label_visibility="collapsed")
    st.session_state.page = escolha

# Exibe a página selecionada
if st.session_state.page == "📊 Quadro Geral":
    st.markdown("<h1 style='text-align: center;'>Quadro Geral de Casos</h1>", unsafe_allow_html=True)
    # Aqui vai o conteúdo do Quadro Geral
    dados = carregar_dados_ficticios()

    # Título

    st.write("O gráfico abaixo representa a evolução dos casos ao longo do tempo.")

    # Filtros laterais
    st.sidebar.header("Filtros")

    # Filtro de estados
    estados = dados["Estado"].unique()
    estados_selecionados = st.sidebar.multiselect("Selecione os estados", estados, default=["São Paulo", "Bahia"])

    # Filtro de período
    datas = dados["Data"]
    data_inicial = datas.min().to_pydatetime()
    data_final = datas.max().to_pydatetime()
    intervalo = st.slider("Período", min_value=data_inicial, max_value=data_final,
                                value=(data_inicial, data_final), step=timedelta(days=30))

    # Filtrar dados
    dados_filtrados = dados[
        (dados["Estado"].isin(estados_selecionados)) &
        (dados["Data"] >= intervalo[0]) &
        (dados["Data"] <= intervalo[1])
    ]

    # Pivotar dados para gráfico de linhas
    df_pivot = dados_filtrados.pivot(index="Data", columns="Estado", values="Casos")

    # Gráfico de linha
    st.line_chart(df_pivot)

    # Performance de crescimento por estado
    st.write("### Variação no número de casos")

    for estado in estados_selecionados:
        serie = df_pivot[estado].dropna()
        if len(serie) > 1:
            crescimento = (serie.iloc[-1] / serie.iloc[0] - 1) * 100
            st.write(f"**{estado}**: {crescimento:.2f}% de variação no período")
        

elif st.session_state.page == "🗺️ Mapa Interativo":
    st.markdown("<h1 style='text-align: center;'>Mapa Interativo</h1>", unsafe_allow_html=True)
    st.title("🌡️ Mapa de Calor - Notificações na RMR")

# 📍 Dados fictícios de municípios da RMR com número de notificações
    dados = pd.DataFrame({
        'Município': [
            'Recife', 'Olinda', 'Jaboatão dos Guararapes',
            'Paulista', 'Camaragibe', 'São Lourenço da Mata',
            'Igarassu', 'Abreu e Lima', 'Cabo de Santo Agostinho',
            'Moreno', 'Itapissuma', 'Araçoiaba', 'Itamaracá'
        ],
        'Latitude': [
            -8.0476, -7.9986, -8.1127,
            -7.9408, -8.0237, -7.9907,
            -7.8286, -7.9111, -8.2822,
            -8.1082, -7.7758, -7.7883, -7.7425
        ],
        'Longitude': [
            -34.8770, -34.8450, -34.9286,
            -34.8731, -34.9787, -35.0133,
            -34.9012, -34.8983, -35.0255,
            -35.0831, -34.9564, -35.0906, -34.8298
        ],
        'Casos': [
            320, 150, 290,
            80, 70, 60,
            50, 45, 110,
            40, 25, 15, 30
        ]
    })

    # 🔥 Preparar dados para HeatMap (repetindo coordenadas por número de casos)
    heat_data = []

    for _, row in dados.iterrows():
        heat_data.extend([[row['Latitude'], row['Longitude']]] * row['Casos'])

    # 🗺️ Criar o mapa
    m = folium.Map(location=[-8.05, -34.9], zoom_start=10)

    # ➕ Adicionar camada de calor
    HeatMap(heat_data, radius=20, blur=15, min_opacity=0.3).add_to(m)

    # 📍 Opcional: adicionar marcadores com popups
    for _, row in dados.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Município']}<br>Casos: {row['Casos']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # 📌 Exibir no Streamlit
    folium_static(m)
        
        


    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Gerar dados fictícios


