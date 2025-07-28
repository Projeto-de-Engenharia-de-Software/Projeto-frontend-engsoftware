# pages/adicionar_equipe.py
import streamlit as st
import requests
from pages.util import API_BASE_URL, make_authenticated_request

st.set_page_config(page_title="Adicionar Equipe", layout="centered", initial_sidebar_state="collapsed")

hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

st.title("Adicionar Nova Equipe")

nome = st.text_input("Nome da Equipe")

col1, col2 = st.columns(2)

with col1:
    if st.button("Criar Equipe"):
        if not nome:
            st.warning("Por favor, insira o nome da equipe.")
        else:
            response = make_authenticated_request(
                method="post",
                url=f"{API_BASE_URL}equipes/",
                json_data={"nome": nome}
            )

            if response and response.status_code in [200, 201]:
                st.success("Equipe criada com sucesso!")
                st.switch_page("pages/quadro_geral.py")
            else:
                st.error("Erro ao criar equipe. Verifique se o nome já existe ou tente novamente.")

with col2:
    if st.button("Voltar"):
        st.switch_page("pages/quadro_geral.py")