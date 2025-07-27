# pages/remover_equipe.py
import streamlit as st
from pages.util import make_authenticated_request, API_BASE_URL
from pages._login import cookie

# Recupera token do cookie, se necessário
token_cookie = cookie.get("auth_token")
if token_cookie and 'auth_token' not in st.session_state:
    st.session_state.auth_token = token_cookie

# Redireciona se não autenticado
if 'auth_token' not in st.session_state:
    st.switch_page("pages/_login.py")

st.set_page_config(page_title="Remover Equipe", layout="centered", initial_sidebar_state="collapsed")
st.title("Remover Equipe")

nome = st.text_input("Nome da equipe que deseja remover")

col1, col2= st.columns(2)
payload = {"nome": nome}

with col1:
    if st.button("Remover Equipe"):
        if not nome:
            st.warning("Digite o nome da equipe.")
        else:
            response = make_authenticated_request(method="delete", url=f"{API_BASE_URL}equipes/", json_data=payload)

            if response and response.status_code in [200, 204]:
                st.success("Equipe removida com sucesso!")
                st.switch_page("pages/quadro_geral.py")
            elif response is not None:
                st.error("Erro ao remover equipe.")
                try:
                    st.json(response.json())
                except Exception as e:
                    st.write(str(e))
            else:
                st.error("Erro de conexão com o servidor.")

with col2:
    if st.button("Voltar"):
        st.switch_page("pages/quadro_geral.py")
