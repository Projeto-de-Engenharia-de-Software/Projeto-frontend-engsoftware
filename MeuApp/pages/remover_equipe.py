# remover_equipe.py
import streamlit as st
from pages.util import API_BASE_URL, make_authenticated_request
from pages._login import cookie

st.set_page_config(page_title="Remover Equipe", layout="centered", initial_sidebar_state="collapsed")

# Oculta o sidebar
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

# Garante que o token esteja presente
token_cookie = cookie.get("auth_token")
if token_cookie and 'auth_token' not in st.session_state:
    st.session_state.auth_token = token_cookie

if 'auth_token' not in st.session_state:
    st.switch_page("pages/_login.py")

# Buscar equipes
response = make_authenticated_request("get", f"{API_BASE_URL}equipes/")


if response and response.status_code == 200:
    equipes = response.json()
    equipe_opcoes = {f"{eq['nome']} (ID {eq['id']})": eq['id'] for eq in equipes}
        
    st.title("Remover Equipe")

    equipe_selecionada = st.selectbox("Selecione a equipe para remover", list(equipe_opcoes.keys()))

    if st.button("Remover"):
        equipe_id = equipe_opcoes[equipe_selecionada]
        delete_url = f"{API_BASE_URL}equipes/{equipe_id}/"
        delete_response = make_authenticated_request("delete", delete_url)

        if delete_response and delete_response.status_code in [200, 204]:
            st.success(f"Equipe '{equipe_selecionada}' removida com sucesso!")
        else:
            st.error("Erro ao remover equipe.")
else:
    st.error("Erro ao carregar equipes.")

if st.button("Voltar"):
    st.switch_page("pages/quadro_geral.py")