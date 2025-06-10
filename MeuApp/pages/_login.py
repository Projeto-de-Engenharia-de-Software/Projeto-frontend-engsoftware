# C:\Users\ruang\Documents\aplicativos\NexusFrontEnd\MeuApp\pages\1_Login.py
import streamlit as st
# Remova esta linha se você não a estiver usando mais: from streamlit_extras.switch_page_button import switch_page


# Oculta a barra lateral e menu padrão (isso pode ser sobrescrito pelo Home.py se ele definir algo)
st.set_page_config(page_title="Nexus - Login", layout="centered") # Ajustei o título para ser mais específico


# Aplica estilo customizado (CSS) - Mantenha este bloco ou mova-o para tema.py
st.markdown("""
    <style>
    body {
        font-family: 'sans-serif';
    }

    .title {
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        margin-top: -30px;
        margin-bottom: 0;
    }

    .login-box {
        max-width: 400px;
        margin: auto;
        padding: 30px;
        background-color: white;
        border-radius: 10px;
        text-align: center;
    }


            section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Remove o botão de recolher/expandir a sidebar (☰) */
    div[data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

st.image("pages/image.png", use_container_width=True) 
# Título principal
st.markdown('<div class="title">Nexus</div>', unsafe_allow_html=True)
st.subheader("Login")

# Caixa de login
with st.container():
    email = st.text_input("E-mail", placeholder="Digite seu e-mail")
    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

col1, col2, col3 = st.columns([1,2,4])
with col1:
    if st.button("Entrar", key="btn_entrar_login"): # Adicionei key
        # Lógica de autenticação aqui
        # Se o login for bem-sucedido, redirecionar para uma página pós-login, ex: Home
        st.switch_page("pages/quadro_geral.py") # Redireciona para a página principal Home.py
with col2:
    if st.button("Esqueci minha senha", key="btn_esqueci_login"): # Adicionei key
        st.warning("Redirecionar para recuperação de senha")
        # lógica de recuperação...

with col3:
    if st.button("Não possui cadastro?", key="btn_cadastro_login"): # Adicionei key
        # AQUI É A MUDANÇA PRINCIPAL: PASSE APENAS O NOME DO ARQUIVO SEM O ".py"
        st.switch_page("2_Cadastrar") # Correto! Redireciona para pages/2_Cadastrar.py