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
        df_equipe = df_equipe[df_equipe["CS_SEXO"] == 'F']
        if 'DT_NOTIFIC' in df_equipe.columns:
            df_equipe['DT_NOTIFIC'] = pd.to_datetime(df_equipe['DT_NOTIFIC'], errors='coerce')
        if 'DT_OCOR' in df_equipe.columns:
            # errors='coerce' vai colocar NaT para valores que não puderem ser convertidos
            df_equipe['DT_OCOR'] = pd.to_datetime(df_equipe['DT_OCOR'], errors='coerce')
        return df_equipe
    else:
        st.error("Erro ao carregar dados")
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
    
def grafico(dados, ano):
    st.markdown("---")
    

    # --- Lógica para o Gráfico de Linhas por Mês e MUNICÍPIO ---
    if not dados.empty and 'DT_OCOR' in dados.columns and 'MUNICIPIO' in dados.columns and 'NU_ANO' in dados.columns:
        # 1. Filtrar os dados para o ano selecionado no selectbox do gráfico
        dados_grafico_ano = dados[dados["NU_ANO"] == ano].copy()

        # 2. Extrair o mês da coluna de data (DT_OCOR)
        dados_grafico_ano['MES'] = dados_grafico_ano['DT_OCOR'].dt.month
        
        # Mapear número do mês para nome do mês (para o eixo X)
        mes_nomes = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }
        dados_grafico_ano['MES_NOME'] = dados_grafico_ano['MES'].map(mes_nomes)

        # 3. Agrupar por Mês e MUNICÍPIO e contar os casos
        # Remove linhas onde MUNICIPIO é None ou vazio antes de agrupar, se aplicável
        dados_grafico_ano_limpo = dados_grafico_ano.dropna(subset=['MUNICIPIO'])
        
        # Contar ocorrências para cada MUNICIPIO por MÊS
        contagem_por_mes_municipio = dados_grafico_ano_limpo.groupby(['MES', 'MES_NOME', 'MUNICIPIO']).size().reset_index(name='Numero de Casos')
        
        # 4. Preencher meses faltantes para linhas contínuas
        # Pega todos os municípios únicos e todos os meses possíveis
        todos_municipios_unicos = contagem_por_mes_municipio['MUNICIPIO'].unique()
        todos_meses_numeros = range(1, 13)
        
        # Cria um DataFrame de todos os meses/municípios possíveis
        full_index = pd.MultiIndex.from_product([todos_meses_numeros, todos_municipios_unicos], names=['MES', 'MUNICIPIO'])
        full_df = pd.DataFrame(index=full_index).reset_index()
        
        # Faz um merge com a contagem real e preenche NaNs com 0
        contagem_por_mes_municipio = pd.merge(
            full_df, contagem_por_mes_municipio, 
            on=['MES', 'MUNICIPIO'], how='left'
        ).fillna(0)
        contagem_por_mes_municipio['Numero de Casos'] = contagem_por_mes_municipio['Numero de Casos'].astype(int)
        
        # Adiciona o nome do mês novamente após o merge
        contagem_por_mes_municipio['MES_NOME'] = contagem_por_mes_municipio['MES'].map(mes_nomes)

         # --- NOVO: Gráfico de Barras por Município ---
    st.subheader(f"Total de Casos por Município (Ano {ano})")

    # Reutilize 'dados_grafico_ano' que já está filtrado pelo ano selecionado
    # Agrupe por MUNICPIO e conte o número de ocorrências
    if not dados_grafico_ano.empty and 'MUNICIPIO' in dados_grafico_ano.columns:
        contagem_por_municipio = dados_grafico_ano['MUNICIPIO'].value_counts().reset_index()
        contagem_por_municipio.columns = ['Município', 'Total de Casos']
        
        # Opcional: Ordenar barras para melhor visualização (ex: do maior para o menor)
        contagem_por_municipio = contagem_por_municipio.sort_values('Total de Casos', ascending=False)

        bar_chart = alt.Chart(contagem_por_municipio).mark_bar().encode(
            x=alt.X('Total de Casos:Q', title='Número de Casos'),
            y=alt.Y('Município:N', sort='-x', title='Município'), # Ordena Y pelo valor do X (descendente)
            tooltip=['Município', 'Total de Casos']
        ).properties(
            title=f'Total de Casos por Município em {ano}'
        ).interactive() # Permite zoom

        st.altair_chart(bar_chart, use_container_width=True)

    else:
        st.info(f"Dados insuficientes ou colunas 'DT_OCOR'/'MUNICIPIO' ausentes para gerar o gráfico para o ano {ano}.")
    
    st.subheader("📍 Variação de Casos entre as datas selecionadas:")

    # Garante que DT_OCOR está em datetime
    dados['DT_NOTIFIC'] = pd.to_datetime(dados['DT_NOTIFIC'], errors='coerce')

    # Cria colunas auxiliares de ano e mês
    dados['ANO'] = dados['DT_NOTIFIC'].dt.year
    dados['MES'] = dados['DT_NOTIFIC'].dt.month

    # Agrupa os dados por ANO e MES
    dados_ano = dados[dados['ANO'] == ano]

    # Conta casos por mês
    casos_por_mes = dados_ano.groupby('MES').size().sort_index()


    primeiro_mes = casos_por_mes.iloc[0]
    ultimo_mes = casos_por_mes.iloc[-1]

    # Calcula a variação percentual entre o primeiro e o último mês
    if primeiro_mes > 0:
        variacao_percentual = ((ultimo_mes - primeiro_mes) / primeiro_mes) * 100
    else:
        variacao_percentual = 0.0

    total_ano = casos_por_mes.sum()
    variancia_mensal = casos_por_mes.var()

    # Formata texto no estilo da imagem
    tipo_variacao = "aumento" if variacao_percentual > 0 else "redução"
    variacao_formatada = abs(variacao_percentual)

    st.markdown(f"""
    - **{ano}**: {tipo_variacao} de **{variacao_formatada:.2f}%** nos casos entre o primeiro e o último mês.
    • Total de casos no ano: **{total_ano}**  
    
    """)

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
        "Selecione o intervalo de notificação",
        min_value=data1,
        max_value=data2,
        value=(data1, data2),
        format="DD/MM/YYYY",
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
        grafico(dados_filtrados, ano)
    
    else:
        st.dataframe(dados_raca)
        grafico(dados_raca, ano)

    
elif st.session_state.page == "🗺️ Mapa Interativo":

    st.markdown("<h1 style='text-align: center;'>Mapa Interativo</h1>", unsafe_allow_html=True)
    st.title("🌡️ Mapa de Calor - Notificações na RMR")

    casos = get_quadro()

    casos["DT_NOTIFIC"] = pd.to_datetime(casos["DT_NOTIFIC"])

    ano = st.sidebar.selectbox(
        "Selecione o ano de análise", 
        [2024, 2023, 2022, 2021, 2020]
    )

    dados_ano = casos[casos["DT_NOTIFIC"].dt.year == ano]


    data1 = dados_ano["DT_NOTIFIC"].min().date()
    data2 = dados_ano["DT_NOTIFIC"].max().date()


    slider = st.sidebar.slider(
        "Selecione o intervalo",
        min_value=data1,
        max_value=data2,
        value=(data1, data2),
        format="DD/MM/YYYY",
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

    dados_geo = carregar_dados_pernambuco()

    contagem_de_casos = None

    if raca == "Nenhum":

        contagem_de_casos = dados_filtrados["MUNICIPIO"].value_counts()
        dados_geo["Casos"] = dados_geo["cidade"].map(contagem_de_casos).fillna(0).astype(int)
    
    else:
        contagem_de_casos = dados_raca["MUNICIPIO"].value_counts()
        dados_geo["Casos"] = dados_geo["cidade"].map(contagem_de_casos).fillna(0).astype(int)

    contagem_de_casos = dados_filtrados["MUNICIPIO"].value_counts()
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
    

elif st.session_state.page == "⚙️ Configurações":

    config()




        


  

