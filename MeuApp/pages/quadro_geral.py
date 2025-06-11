import folium
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
from datetime import timedelta
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import altair as alt

@st.cache_data
def carregar_dados():
    caminho = r"C:\Users\pabol\Desktop\Front_End_Nexus\Projeto-frontend-engsoftware\MeuApp\pages\sinannet_cnv_violepe231354143_208_128_99.csv"
    return pd.read_csv(caminho, sep=";", encoding="iso-8859-1", skiprows=3)



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
st.image("pages/image.png", use_container_width=True) 
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
    # Carrega os dados
    dados = carregar_dados()

# Renomear primeira coluna para 'Macrorregião'
    dados.rename(columns={dados.columns[0]: "Macrorregião"}, inplace=True)

    # Remove a coluna 'Total', se existir
    if 'Total' in dados.columns:
        dados.drop(columns=['Total'], inplace=True)

    # Converte para formato longo
    df_meltado = dados.melt(id_vars=["Macrorregião"], var_name="Mês", value_name="Casos")

    # Remove espaços em branco da coluna 'Mês' e converte os valores para numérico
    df_meltado["Mês"] = df_meltado["Mês"].str.strip()
    df_meltado["Casos"] = pd.to_numeric(df_meltado["Casos"], errors='coerce')

    # Mapeia os nomes dos meses para números e cria uma coluna de datas
    mes_para_numero = {
        "Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4, "Mai": 5, "Jun": 6,
        "Jul": 7, "Ago": 8, "Set": 9, "Out": 10, "Nov": 11, "Dez": 12
    }
    df_meltado["Data"] = df_meltado["Mês"].astype(str).map(lambda m: datetime(2024, mes_para_numero[m], 1))

    # Ordena os meses corretamente e deixa a coluna categórica para o gráfico
    ordem_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    df_meltado["Mês"] = pd.Categorical(df_meltado["Mês"], categories=ordem_meses, ordered=True)

    # Sidebar - Filtros
    st.sidebar.header("Filtros")
    regioes_disponiveis = df_meltado["Macrorregião"].unique().tolist()
    regioes_selecionadas = st.sidebar.multiselect("Selecione as macrorregiões", regioes_disponiveis, default=regioes_disponiveis)

    # Lista de datas mensais para slider
    meses_2024 = [datetime(2024, m, 1) for m in range(1, 13)]

    # Slider de intervalo de meses
    intervalo_meses = st.sidebar.slider(
        "Selecione o intervalo de meses",
        min_value=meses_2024[0],
        max_value=meses_2024[-1],
        value=(meses_2024[0], meses_2024[-1]),
        format="MMM",
        step=timedelta(days=31)
    )

    # Filtra os dados pela região e intervalo de datas
    df_filtrado = df_meltado[
        (df_meltado["Macrorregião"].isin(regioes_selecionadas)) &
        (df_meltado["Data"] >= intervalo_meses[0]) &
        (df_meltado["Data"] <= intervalo_meses[1])
    ]

    # Título principal
    st.title("Quadro Geral de Casos de Violência")
    st.markdown("Este gráfico mostra a distribuição de casos por mês nas macrorregiões de Pernambuco em 2024.")

    # Gráfico interativo com meses em português no eixo X
    grafico = alt.Chart(df_filtrado).mark_line(point=True).encode(
        x=alt.X("Mês:N", sort=ordem_meses, title="Mês"),
        y=alt.Y("Casos:Q", title="Número de Casos"),
        color="Macrorregião:N",
        tooltip=["Macrorregião", "Mês", "Casos"]
    ).properties(
        width=800,
        height=500,
        title="Número de Casos por Mês e Macrorregião (2024)"
    )

    # Exibe o gráfico
    st.altair_chart(grafico, use_container_width=True)

    # --- Cálculo da variação percentual ---

    # Função para calcular variação percentual entre primeiro e último mês do intervalo para cada região
    def calcular_variacao(df, inicio, fim):
        resultados = []
        for regiao in regioes_selecionadas:
            df_regiao = df[(df["Macrorregião"] == regiao) & (df["Data"] >= inicio) & (df["Data"] <= fim)]

            if df_regiao.empty:
                continue

            # Ordena por Data para pegar valores extremos
            df_regiao = df_regiao.sort_values("Data")

            valor_inicio = df_regiao.iloc[0]["Casos"]
            valor_fim = df_regiao.iloc[-1]["Casos"]

            # Tratar casos com zero para evitar divisão por zero
            if pd.isna(valor_inicio) or valor_inicio == 0:
                variacao = None
            else:
                variacao = ((valor_fim - valor_inicio) / valor_inicio) * 100

            resultados.append((regiao, variacao))
        return resultados

    variacoes = calcular_variacao(df_filtrado, intervalo_meses[0], intervalo_meses[1])

    # Exibe o texto com variação percentual
    st.markdown("### Variação percentual de casos entre o primeiro e último mês selecionados por macrorregião:")

    if not variacoes:
        st.write("Nenhum dado disponível para as regiões e período selecionados.")
    else:
        for regiao, variacao in variacoes:
            if variacao is None:
                texto = f"- **{regiao}**: dados insuficientes para calcular variação."
            else:
                if variacao > 0:
                    texto = f"- **{regiao}**: aumento de {variacao:.2f}% nos casos."
                elif variacao < 0:
                    texto = f"- **{regiao}**: redução de {abs(variacao):.2f}% nos casos."
                else:
                    texto = f"- **{regiao}**: sem variação nos casos."
            st.write(texto)

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

homepage_btn = st.button("Homepage")
if homepage_btn:
      st.switch_page("pages/_homepage.py")
        


  

