import streamlit as st

st.set_page_config(
    page_title="Nexus - Homepage",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.image("pages/image.png", use_container_width=True) 
col1, col2, col3 = st.columns([2, 3, 2])
col2.title("Bem Vindo!")


st.markdown("""
    <style>
        .centered-box {
            background-color: #f0f2f6;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .select-label {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# Layout com colunas para centralizar
col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    
    st.markdown('<label class="select-label">🌐 Escolha uma página:</label>', unsafe_allow_html=True)
    pagina = st.selectbox("", ["📊 Quadro Geral", "🗺️ Mapa Interativo" , "⚙️ Configurações"])
    st.markdown('</div>', unsafe_allow_html=True)

selecionar_pag = col2.button('Selecionar Página')

if selecionar_pag and pagina=="📊 Quadro Geral":
    st.switch_page("pages/quadro_geral.py")

if selecionar_pag and pagina=="🗺️ Mapa Interativo":
    st.switch_page("pages/mapa_interativo.py")   

if selecionar_pag and pagina=="⚙️ Configurações":
    st.switch_page("pages/configuracoes.py")  
    