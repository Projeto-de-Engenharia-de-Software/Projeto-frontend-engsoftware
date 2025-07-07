import streamlit as st
import requests, json

st.set_page_config(page_title="Nexus - Login", layout="centered", initial_sidebar_state="collapsed")

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

st.markdown('<div class="title">Nexus</div>', unsafe_allow_html=True)
st.subheader("Login")


with st.container():

    username = st.text_input("Usuário", placeholder="Digite seu Usuário")
    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

col1, col2, col3 = st.columns([1,2,4])



if col1.button("Entrar", key="btn_entrar_login"):
    st.success("Login realizado com sucesso!")
    st.switch_page("pages/quadro_geral.py")

   

with col2:

    if st.button("Esqueci minha senha", key="btn_esqueci_login"):

        st.switch_page("pages/_recuperacao_senha.py")

with col3:
    
    if st.button("Não possui cadastro?", key="btn_cadastro_login"): 
     
        st.switch_page("pages/_cadastrar.py") 