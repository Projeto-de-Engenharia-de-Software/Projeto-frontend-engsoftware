import streamlit as st
from pages.util import API_BASE_URL, make_authenticated_request
import requests



def adicionar_profissional(username):

    adicionar_url = f"{API_BASE_URL}equipes/2/adicionar-profissional/"
    login_url = f"{API_BASE_URL}auth/token/"

    try:
        
        dados = {"username": username}


        response = make_authenticated_request('post', adicionar_url, json_data=dados)



        if response and response.status_code in [200,201]:

            st.success("Profissional adicionado com sucesso!")
            st.switch_page("pages/quadro_geral.py")
            st.rerun()  

        else:

            st.error("Token não recebido. Verifique a resposta da API.")

        return True
    
    except requests.exceptions.RequestException as e:

        try:

            error = response.json()
            st.error(f"Erro ao adicionar: {error.get('non_field_errors', ['Verifique nome de usuário.'])[0]}")

        except:

            st.error("Erro ao tentar se conectar. Verifique seu backend.")

        return False


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

st.title("Adicionar Membro para a Equipe")

adicionar_url = f"{API_BASE_URL}/equipes/1/adicionar-profissional/"

col1, col2 = st.columns([2,2])

with col1:
    usuario = st.text_input("Nome de Usuário")
    
    

cl1, cl2, cl3, cl4 = st.columns([2,6,2,2])

with cl1:
    if st.button("Adicionar"):
        adicionar_profissional(usuario)

    
with cl2:
    if st.button("Voltar"):
        st.switch_page("pages/equipes.py")