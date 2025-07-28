import streamlit as st
from pages.util import API_BASE_URL, make_authenticated_request
from pages._login import cookie

st.set_page_config(page_title="Adicionar Membro")  # <- PRIMEIRO comando Streamlit

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

token_cookie = cookie.get("auth_token")
if token_cookie and 'auth_token' not in st.session_state:
    st.session_state.auth_token = token_cookie

if 'auth_token' not in st.session_state:
    st.switch_page("pages/_login.py")

response = make_authenticated_request("get", f"{API_BASE_URL}equipes/")
if response and response.status_code == 200:
    equipes = response.json()
    equipe_opcoes = {f"{eq['nome']} (ID {eq['id']})": eq['id'] for eq in equipes}

    st.title("Adicionar Membro a Equipe")

    equipe_selecionada = st.selectbox("Selecione a equipe", list(equipe_opcoes.keys()))
    username = st.text_input("Nome de usuário do profissional a adicionar")

    if st.button("Adicionar"):
        equipe_id = equipe_opcoes[equipe_selecionada]
        url = f"{API_BASE_URL}equipes/{equipe_id}/adicionar-profissional/"
        body = {"username": username}
        post_response = make_authenticated_request("post", url, json_data=body)

        if post_response and post_response.status_code in [200, 201]:
            st.success("Profissional adicionado com sucesso!")
            st.switch_page("pages/quadro_geral.py")

        elif post_response and post_response.status_code == 400:
            erro = post_response.get("erro")
            st.error(f"Erro ao adicionar membro: {erro}")

        else:
            st.error("Usuário não encontrado.")


else:
    st.error("Erro ao carregar equipes.")

if st.button("Voltar"):
    st.switch_page("pages/quadro_geral.py")