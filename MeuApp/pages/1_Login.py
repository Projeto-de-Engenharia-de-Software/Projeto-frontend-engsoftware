# C:\Users\ruang\Documents\aplicativos\NexusFrontEnd\MeuApp\pages\1_Login.py
import streamlit as st
# Remova esta linha se você não a estiver usando mais: from streamlit_extras.switch_page_button import switch_page
from tema import aplicar_tema

# Oculta a barra lateral e menu padrão (isso pode ser sobrescrito pelo Home.py se ele definir algo)
st.set_page_config(page_title="Nexus - Login", layout="centered") # Ajustei o título para ser mais específico
aplicar_tema()

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

    /* As cores dos botões e placeholders seriam definidas no tema.py, mas aqui está como você os tinha originalmente, se ainda não estiverem no tema.py */
    .btn-login {
        background-color: black;
        color: white;
        padding: 10px 30px;
        margin: 10px 5px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
    }

    .btn-login:hover {
        background-color: #333;
    }
    </style>
""", unsafe_allow_html=True)


# Exibe a imagem no topo (ondas vermelhas/azuis)
# IMPORTANTE: O caminho da imagem agora é relativo ao Home.py (o script principal)
# OU, se a imagem está na pasta 'pages', você pode precisar de um caminho relativo específico
# ao script atual, mas o ideal é que assets estejam fora de 'pages'.
# Para a sua estrutura, se 'image.png' está dentro de 'pages', você pode tentar:
st.image("image.png", use_container_width=True) # ou apenas "image.png" se Streamlit mapeia dentro de pages

# Título principal
st.markdown('<div class="title">Nexus</div>', unsafe_allow_html=True)
st.subheader("Login")

# Caixa de login
with st.container():
    email = st.text_input("E-mail", placeholder="Digite seu e-mail")
    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Entrar", key="btn_entrar_login"): # Adicionei key
        # Lógica de autenticação aqui
        # Se o login for bem-sucedido, redirecionar para uma página pós-login, ex: Home
        st.switch_page("Home") # Redireciona para a página principal Home.py
with col2:
    if st.button("Esqueci minha senha", key="btn_esqueci_login"): # Adicionei key
        st.warning("Redirecionar para recuperação de senha")
        # lógica de recuperação...

with col3:
    if st.button("Não possuí cadastro?", key="btn_cadastro_login"): # Adicionei key
        # AQUI É A MUDANÇA PRINCIPAL: PASSE APENAS O NOME DO ARQUIVO SEM O ".py"
        st.switch_page("2_Cadastrar") # Correto! Redireciona para pages/2_Cadastrar.py